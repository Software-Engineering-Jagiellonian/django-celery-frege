import { GrafanaCatalog } from '@/src/components/sideMenu/DashboardsClient';
import { ItemDTO } from './ItemDTO';

export const retrieveAutomaticDashboardsData = (dashboardsData: GrafanaCatalog[]): ItemDTO[] => {
  return dashboardsData.map(
    (catalog: GrafanaCatalog): ItemDTO => ({
      name: catalog.label,
      subNodes: catalog.dashboards?.map((dashboard) => ({
        name: dashboard.label,
        id: dashboard.uid
      }))
    })
  );
};
