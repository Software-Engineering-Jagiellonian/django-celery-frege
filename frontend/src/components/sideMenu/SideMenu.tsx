import React, { FC, useEffect, useState } from 'react';
import { SideMenuItemDTO } from './SideMenuStruct';
import styles from './SideMenu.module.scss';
import { MenuItem } from '../menuItem/MenuItem';
import { SlashCircleFill } from 'react-bootstrap-icons';

export const SideMenu: FC<{ className: string }> = ({ className }) => {
  const [structure, setStructure] = useState<SideMenuItemDTO[]>([]);
  useEffect(() => {
    // structure should be built from grafana response
    setStructure([
      {
        label: 'Home',
        href: '/',
        icon: <SlashCircleFill />,
        subNodes: [
          {
            label: 'Submenu',
            subNodes: [
              {
                label: 'About',
                href: '/about'
              },
              {
                label: 'L1 extra looooooonggggggggggggggggggggggggggg'
              }
            ]
          }
        ]
      }
    ]);
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
