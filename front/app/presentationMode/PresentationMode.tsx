'use client';

import React, { useEffect, useState } from 'react';
import styles from './PresentationMode.module.scss';
import { getGrafanaData, GrafanaCatalog } from '@/src/components/sideMenu/DashboardsClient';
import FullscreenDashboards from '@/src/components/FullScreenDashboards/FullscreenDashboards';
import { StyledButton } from '@/src/components/styledButton/StyledButton';
import { UnwrappedItemDTO } from './utils/UnwrappedItemDTO';
import { retrieveAutomaticDashboardsData } from './utils/retrieveAutomaticDashboardsData';
import { retrieveManualDashboardsData } from './utils/retrieveManualDashboardsData';
import { unwrapStructure } from './utils/unwrapStructure';
import WaitingForSelection from './WaitingForSelection';

export const savedFullscreenDashboardId = 'frege-fullscreen-dashboardId';

const PresentationMode = () => {
  const [structure, setStructure] = useState<UnwrappedItemDTO[]>([]);
  const [grafanaData, setGrafanaData] = useState<GrafanaCatalog[]>([]);
  const [dashboardId, setDashboardId] = useState<string>(
    localStorage.getItem(savedFullscreenDashboardId) || ''
  );
  const [chosenDashboard, setChosenDashboard] = useState<string>(dashboardId);
  const [selectAtLeastOne, setSelectAtLeastOne] = useState<boolean>(false);

  useEffect(() => {
    const automatic = unwrapStructure(retrieveAutomaticDashboardsData(grafanaData));
    const manual = unwrapStructure(retrieveManualDashboardsData());

    setStructure([...automatic, ...manual]);
  }, [grafanaData]);

  useEffect(() => {
    getGrafanaData().then((result: GrafanaCatalog[]) => setGrafanaData(result));
  }, []);

  const saveConfig = () => {
    if (chosenDashboard === '' || chosenDashboard === '---') {
      setSelectAtLeastOne(true);
      return;
    }
    setSelectAtLeastOne(false);
    localStorage.setItem(savedFullscreenDashboardId, chosenDashboard);
    setDashboardId(chosenDashboard);
  };

  return (
    <>
      <div className={styles.optionsRow}>
        <StyledButton className={styles.saveButton} onClick={saveConfig}>
          Save selection
        </StyledButton>

        <select
          className={styles.selectDropdown}
          onChange={(e) => setChosenDashboard(e.target.value)}
          value={chosenDashboard}>
          <option className={styles.selectOption} value={''}>
            ---
          </option>
          {structure
            .sort((x, y) => x.name.localeCompare(y.name))
            .map((el: UnwrappedItemDTO) => (
              <option key={el.id} className={styles.selectOption} value={el.id}>
                {el.name}
              </option>
            ))}
        </select>
      </div>

      {selectAtLeastOne && (
        <div className={styles.errorMsg}>You have to select at least one dashboard!</div>
      )}

      <h3>Preview</h3>
      <div id="fullscreen-view" className={styles.fullscreenWrapper}>
        {dashboardId ? <FullscreenDashboards dashboardId={dashboardId} /> : <WaitingForSelection />}
      </div>
    </>
  );
};

export default PresentationMode;
