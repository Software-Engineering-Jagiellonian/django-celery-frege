'use client';

import React, { useEffect, useState } from 'react';
import { useParams } from 'next/navigation';
import { WidgetsHub } from '../hub/WidgetsHub';
import axios from 'axios';
import { WidgetRetrieveData } from '../hub/hubTypes';

function WidgetsContainer() {
  const { uid } = useParams();
  const [widgets, setWidgets] = useState<WidgetRetrieveData[]>([]);
  const [dashboardName, setDashboardName] = useState('');

  useEffect(() => {
    axios.get(`/grafana/api/dashboards/uid/${uid}`).then((response) => {
      const widgetsTemp: WidgetRetrieveData[] = response.data.dashboard.panels.map(
        (panel: { id: string; title: string }) => {
          return {
            dashboardId: `${uid}`,
            widgetId: `${panel.id}`,
            dashboardName: response.data.dashboard.title,
            widgetName: panel.title
          } as WidgetRetrieveData;
        }
      );

      setDashboardName(response.data.dashboard.title);
      setWidgets(widgetsTemp);
    });
  }, [uid]);

  return (
    <div>
      <h1 className="text-center">{dashboardName}</h1>
      <WidgetsHub widgets={widgets} hubId={`${uid}`} />
    </div>
  );
}

export default WidgetsContainer;
