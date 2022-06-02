import React, { FC, useEffect, useState } from 'react';
import { SideMenuItemDTO } from './SideMenuStruct';
import styles from './SideMenu.module.scss';
import { MenuItem } from '../menuItem/MenuItem';
import axios from "axios";
import {Folder} from "./Folder";
import {FolderDetails} from "./FolderDetails";

export const SideMenu: FC<{ className: string }> = ({ className }) => {
  const [structure, setStructure] = useState<SideMenuItemDTO[]>([]);
  useEffect(() => {

    axios.get("api/folders")
        .then(response => {
          const folders: Folder[] = response.data;
          axios.get(`api/search?${folders.map(folder => `folderIds=${folder.id}`).join("&")}`).then(res => {
                const folderDetails: FolderDetails[] = res.data;
                folderDetails.forEach(details => {
                    const folder = folders.find(folder => folder.id === details.folderId);
                    if (folder != null) {
                        if (folder.folderDetails == null) {
                            folder.folderDetails = []
                        }
                        folder.folderDetails.push(details);
                    }
                });

              const sideMenuItems: SideMenuItemDTO[] = folders.map(folder => {
                  if (folder.folderDetails) {
                      return {
                          label: folder.title,
                          href: `/${folder.title}`,
                          subNodes: folder.folderDetails.map(details => {
                              return {
                                  label: details.title,
                                  href: `/${details.title}`
                              }
                          })
                      } as SideMenuItemDTO
                  }
                  return {
                      label: folder.title,
                      href: `/${folder.title}`
                  }
              })

              setStructure(sideMenuItems)
          });
        });
  }, []);

  const [activeItem, setActiveItem] = useState<string>('/');
  const classNames = className ? `${styles.sideMenu} ${className}` : styles.sideMenu;
  return (
    <div className={classNames}>
      {structure.map((tier1, index) => (
        <MenuItem
          key={index}
          presentationProps={tier1}
          isActive={(e: string) => e === activeItem}
          handleClick={setActiveItem}
        />
      ))}
    </div>
  );
};
