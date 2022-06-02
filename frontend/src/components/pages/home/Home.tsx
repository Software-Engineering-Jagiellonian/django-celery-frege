import React from 'react';
import { WidgetsHub } from '../../widgets/hub/WidgetsHub';

function Home() {
  return (
    <div>
      <h1>Home</h1>
      <WidgetsHub
        widgets={[
          {
            widgetId: '2',
            dashboardId: 'RRj1M49nz',
            widgetName: 'widget2',
            dashboardName: 'dashboard'
          },
          {
            widgetId: '4',
            dashboardId: 'RRj1M49nz',
            widgetName: 'widget2',
            dashboardName: 'dashboard'
          }
        ]}
        hubId={'general/RRj1M49nz'}
      />
    </div>
  );
}

export default Home;
