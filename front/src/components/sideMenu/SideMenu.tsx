import React, { FC, useEffect, useState } from 'react';
import { SideMenuItemDTO } from './SideMenuStruct';
import styles from './SideMenu.module.scss';
import { MenuItem } from '../menuItem/MenuItem';
import {
  fregeManualDashboardPrefix,
  getGrafanaData,
  GrafanaCatalog,
  retrieveAutomaticDashboards,
  retrieveManualDashboards
} from './DashboardsClient';
import { StyledButton } from '../styledButton/StyledButton';
import { StyledModal } from '../styledModal/StyledModal';
import { Box, Boxes, Plus } from 'react-bootstrap-icons';
import PresentationMode from '../menuItem/PresentationMode';
import DataTableView from '../menuItem/DataTableView';
import Logs from '../menuItem/Logs';
import Users from '../menuItem/Users';
import Services from '../menuItem/Services';

interface UnwrappedType {
  id: string;
  name: string;
}
const unwrapDashboards = (grafanaData: GrafanaCatalog[]): UnwrappedType[] => {
  return grafanaData.reduce((prev, curr) => {
    if (!curr.dashboards) return prev;

    const newLabels = curr.dashboards.map(
      (dashboard): UnwrappedType => ({
        name: `${curr.label} / ${dashboard.label}`,
        id: dashboard.uid
      })
    );

    return [...prev, ...newLabels];
  }, [] as UnwrappedType[]);
};

export const SideMenu: FC<{ className: string }> = ({ className }) => {
  const [structure, setStructure] = useState<SideMenuItemDTO[]>([]);
  const [grafanaData, setGrafanaData] = useState<GrafanaCatalog[]>([]);
  const [dashboardName, setDashboardName] = useState<string>('');

  useEffect(() => {
    setStructure([
      {
        label: 'Automatic',
        icon: <Box />,
        subNodes: retrieveAutomaticDashboards(grafanaData)
      },
      {
        label: 'Manual',
        icon: <Boxes />,
        subNodes: retrieveManualDashboards(),
        structOptions: [
          <Plus
            key={1}
            onClick={(e) => {
              e.stopPropagation();
              setDashboardName('');
              setChosenDashboard(new Set());
              setShowNameUsed(false);
              setShowAtLeastOne(false);
              setAddModalVisible(true);
            }}
          />
        ]
      }
    ]);
  }, [grafanaData]);

  useEffect(() => {
    getGrafanaData().then((result: GrafanaCatalog[]) => setGrafanaData(result));
  }, []);

  const [activeItem, setActiveItem] = useState<string>('/');
  const [addModalVisible, setAddModalVisible] = useState<boolean>(false);
  const [chosenDashboards, setChosenDashboard] = useState<Set<string>>(new Set<string>());
  const [showNameUsed, setShowNameUsed] = useState<boolean>(false);
  const [showAtLeastOne, setShowAtLeastOne] = useState<boolean>(false);
  const classNames = className ? `${styles.sideMenu} ${className}` : styles.sideMenu;
  return (
    <>
      <div className={classNames}>
        <div className={styles.menuContainer}>
          {structure.map((tier1, index) => (
            <MenuItem
              key={index}
              presentationProps={tier1}
              isActive={(e: string) => e === activeItem}
              handleClick={setActiveItem}
            />
          ))}
        </div>

        <hr />

        <div className={styles.menuContainer}>
          <PresentationMode />
          <DataTableView />
        </div>

        <hr />

        <div className={styles.menuContainer}>
          <Logs />
        </div>

        <hr />

        <div className={styles.menuContainer}>
          <Services />
        </div>

        <hr />

        <div className={styles.menuContainer}>
          <Users />
        </div>
      </div>
      <StyledModal
        show={addModalVisible}
        header={'Select dashboards'}
        onCancel={() => setAddModalVisible(false)}
        onSave={() => {
          if (!chosenDashboards || chosenDashboards.size === 0) setShowAtLeastOne(true);
          else {
            const key = `${fregeManualDashboardPrefix}${encodeURI(dashboardName)}`;
            if (dashboardName.length > 0 && !window.localStorage[key]) {
              window.localStorage[key] = JSON.stringify({
                label: dashboardName,
                dashboardsIds: Array.from(chosenDashboards)
              });
              setAddModalVisible(false);

              setStructure([
                structure[0],
                {
                  label: 'Manual',
                  subNodes: retrieveManualDashboards()
                }
              ]);
            } else setShowNameUsed(true);
          }
        }}>
        <input
          type="text"
          placeholder="Name"
          value={dashboardName}
          onChange={(e) => setDashboardName(e.target.value)}
          className={styles.textInput}
        />
        {showNameUsed && (
          <div className={styles.errorMsg}>
            The name has been used already and it should not be empty!
          </div>
        )}
        {showAtLeastOne && (
          <div className={styles.errorMsg}>You have to pin at least one dashboard!</div>
        )}
        {unwrapDashboards(grafanaData)
          .sort((x, y) => x.name.localeCompare(y.name))
          .map((node: UnwrappedType) => (
            <div key={node.id} className={styles.pinningListItem}>
              {node.name}
              <StyledButton
                className={styles.listStyledButton}
                onClick={() => {
                  const updatedDashboards = new Set<string>(chosenDashboards);
                  if (updatedDashboards.has(node.id)) updatedDashboards.delete(node.id);
                  else updatedDashboards.add(node.id);

                  setChosenDashboard(updatedDashboards);
                }}>
                {chosenDashboards.has(node.id) ? 'Unpin' : 'Pin'}
              </StyledButton>
            </div>
          ))}
      </StyledModal>
    </>
  );
};
