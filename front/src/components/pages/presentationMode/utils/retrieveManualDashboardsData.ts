import {
  fregeManualDashboardPrefix,
  ManualDashboardStorage
} from '../../../sideMenu/DashboardsClient';
import { ItemDTO } from './ItemDTO';

export const retrieveManualDashboardsData = (): ItemDTO[] => {
  let dashboards: ItemDTO[] = [];
  for (let i = 0; i < window.localStorage.length; i++) {
    const key = window.localStorage.key(i);
    if (key && key.startsWith(fregeManualDashboardPrefix)) {
      const dashboardData = window.localStorage.getItem(key);
      if (dashboardData) {
        const parsedDashboardData = JSON.parse(dashboardData) as ManualDashboardStorage;
        dashboards = [
          ...dashboards,
          {
            name: parsedDashboardData.label,
            id: key.substring(fregeManualDashboardPrefix.length)
          }
        ];
      }
    }
  }
  return dashboards.sort((x, y) => x.name.localeCompare(y.name));
};
