'use client';

import React, { FC, useEffect, useState } from 'react';
import { useParams } from 'next/navigation';
import {
  fregeManualDashboardPrefix,
  ManualDashboardStorage
} from '@/src/components/sideMenu/DashboardsClient';
import { WidgetsHub } from '@/src/components/widgets/hub/WidgetsHub';
import { WidgetRetrieveData } from '@/src/components/widgets/hub/hubTypes';
import axios from 'axios';

export const ManualDashboard: FC = () => {
  const { dashboardId } = useParams();
  const [widgets, setWidgets] = useState<WidgetRetrieveData[] | undefined>([]);
  const [dashboardName, setDashboardName] = useState('');
  useEffect(() => {
    let tempWidgets: WidgetRetrieveData[] = [];
    let dashboardLabel = '';
    if (dashboardId) {
      setWidgets(undefined);
      const dashboardIdStr = Array.isArray(dashboardId) ? dashboardId.join('/') : dashboardId;
      const dashboardData = window.localStorage.getItem(
        `${fregeManualDashboardPrefix}${encodeURI(dashboardIdStr)}`
      );
      if (dashboardData) {
        const parsedDashboard: ManualDashboardStorage = JSON.parse(dashboardData);
        parsedDashboard.dashboardsIds.forEach((dashboardId) => {
          axios.get(`/grafana/api/dashboards/uid/${dashboardId}`).then((response) => {
            const widgetsTemp: WidgetRetrieveData[] = response.data.dashboard.panels.map(
              (panel: { id: string; title: string }) => {
                return {
                  dashboardId: `${dashboardId}`,
                  widgetId: `${panel.id}`,
                  dashboardName: response.data.dashboard.title,
                  widgetName: panel.title
                } as WidgetRetrieveData;
              }
            );

            tempWidgets = [...tempWidgets, ...widgetsTemp];

            setWidgets(tempWidgets);
            setDashboardName(dashboardLabel);
          });
        });
        dashboardLabel = parsedDashboard.label;
      }
    }
  }, [dashboardId]);

  if (widgets) {
    return (
      <div>
        <h1 className="text-center">{dashboardName}</h1>
        <WidgetsHub widgets={widgets} hubId={`${dashboardId}`} />
      </div>
    );
  }

  return <div>404 Not found</div>;
  // TODO: propper error state
};
