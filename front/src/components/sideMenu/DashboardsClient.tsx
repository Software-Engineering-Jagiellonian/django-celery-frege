'use client';

import React from 'react';
import { SideMenuItemDTO } from './SideMenuStruct';
import axios from 'axios';
import { Folder } from './Folder';
import { FolderDetails } from './FolderDetails';
import { Clipboard2Data, Folder2 } from 'react-bootstrap-icons';
export const fregeManualDashboardPrefix = 'frege-manualDashboard-';

export type GrafanaDashboard = {
  label: string;
  id: number;
  uid: string;
};

export type GrafanaCatalog = {
  label: string;
  dashboards?: GrafanaDashboard[];
};

export const getGrafanaData = async (): Promise<GrafanaCatalog[]> => {
  let dashboardsData: GrafanaCatalog[] = [];
  return dashboardsData;

  await axios.get(`/grafana/api/folders`).then(async (response) => {
    const folders: Folder[] = response.data;
    const folderName = folders.reduce(
      (prev, curr) => {
        prev[curr.id] = curr.title;
        return prev;
      },
      {} as Record<string, string>
    );
    await axios
      .get(`/grafana/api/search?${folders.map((folder) => `folderIds=${folder.id}`).join('&')}`)
      .then((res) => {
        const folderDetails: FolderDetails[] = res.data;
        const catalogsStruct = folderDetails.reduce(
          (prev, curr) => {
            const currentDashboards: FolderDetails[] | undefined = prev[curr.folderId];
            prev[curr.folderId] = currentDashboards ? [...currentDashboards, curr] : [curr];
            return prev;
          },
          {} as Record<string, FolderDetails[]>
        );

        dashboardsData = Object.keys(catalogsStruct).map((catalogId) => ({
          label: folderName[catalogId],
          dashboards: catalogsStruct[catalogId].map((dashboardData) => ({
            label: dashboardData.title,
            id: dashboardData.id,
            uid: dashboardData.uid
          }))
        }));
      });
  });

  return dashboardsData;
};

export const retrieveAutomaticDashboards = (
  dashboardsData: GrafanaCatalog[]
): SideMenuItemDTO[] => {
  return dashboardsData.map(
    (catalog: GrafanaCatalog): SideMenuItemDTO => ({
      label: catalog.label,
      icon: <Folder2 />,
      subNodes: catalog.dashboards?.map((dashboard) => ({
        label: dashboard.label,
        href: `/dashboard/automatic/${dashboard.uid}`,
        icon: <Clipboard2Data />
      }))
    })
  );
};

export type ManualDashboardStorage = {
  label: string;
  dashboardsIds: string[];
};

export const retrieveManualDashboards = (): SideMenuItemDTO[] => {
  let dashboards: SideMenuItemDTO[] = [];
  for (let i = 0; i < window.localStorage.length; i++) {
    const key = window.localStorage.key(i);
    if (key && key.startsWith(fregeManualDashboardPrefix)) {
      const dashboardData = window.localStorage.getItem(key);
      if (dashboardData) {
        const parsedDashboardData = JSON.parse(dashboardData) as ManualDashboardStorage;
        dashboards = [
          ...dashboards,
          {
            icon: <Clipboard2Data />,
            label: parsedDashboardData.label,
            href: `/dashboard/manual/${key.substring(fregeManualDashboardPrefix.length)}`
          }
        ];
      }
    }
  }
  return dashboards.sort((x, y) => x.label.localeCompare(y.label));
};
