import React, { FC, useEffect, useState } from 'react';
import { fregeManualDashboardPrefix, ManualDashboardStorage } from '../sideMenu/DashboardsClient';
import { getId, ResponsiveGridLayout, WidgetsHubProps } from '../widgets/hub/WidgetsHub';
import { VisibleLayout, WidgetRetrieveData } from '../widgets/hub/hubTypes';
import axios from 'axios';
import NotFound from './NotFound';
import { Layouts } from 'react-grid-layout';
import { getInitialLayout } from '../widgets/hub/layoutClient';
import styles from './FullscreenDashboards.module.scss';
import Loading from '../Loading/Loading';

const ShowWidgets: FC<WidgetsHubProps> = ({ widgets, hubId }) => {
  const [visibleWidgets, setVisibleWidgets] = useState<Record<string, WidgetRetrieveData>>({});
  const [layout, setLayout] = useState<Layouts>({});

  const getInitialVisibleWidgets = (): Record<string, WidgetRetrieveData> => {
    const layoutFromStorage = window.localStorage[`frege-${hubId}`];
    if (layoutFromStorage) {
      const parsedLayout = JSON.parse(layoutFromStorage) as VisibleLayout[];
      const visibleIds = new Set(parsedLayout.map((layout) => getId(layout.d, layout.i)));

      return widgets.reduce(
        (prev, curr) => {
          const widgetId = getId(curr.dashboardId, curr.widgetId);
          if (visibleIds.has(widgetId)) {
            prev[widgetId] = curr;
          }

          return prev;
        },
        {} as Record<string, WidgetRetrieveData>
      );
    }

    return widgets.reduce(
      (prev, curr) => {
        prev[getId(curr.dashboardId, curr.widgetId)] = curr;
        return prev;
      },
      {} as Record<string, WidgetRetrieveData>
    );
  };

  useEffect(() => {
    setVisibleWidgets(getInitialVisibleWidgets());
    setLayout({
      md: getInitialLayout(hubId, widgets)
    });
  }, [widgets]);

  return (
    <div className={styles.widgetsGridWrapper}>
      <ResponsiveGridLayout
        compactType={null}
        className={styles.widgetsGrid}
        rowHeight={60}
        draggableHandle={`.${styles.dragHeader}`}
        breakpoints={{ md: 0 }}
        cols={{ md: 20 }}
        layouts={layout}
        onLayoutChange={(curr, all) => setLayout(all)}
        resizeHandle={<div className={styles.resizeHandler}></div>}>
        {Object.values(visibleWidgets).map((widget: WidgetRetrieveData) => (
          <div key={getId(widget.dashboardId, widget.widgetId)} className={styles.widget}>
            <div className={styles.widgetContent}>
              <iframe
                src={`/grafana/d-solo/${widget.dashboardId}/dashboard-1?orgId=1&panelId=${widget.widgetId}`}
                width="100%"
                height="100%"
                frameBorder="0"
                className={styles.graphFrame}></iframe>
            </div>
          </div>
        ))}
      </ResponsiveGridLayout>
    </div>
  );
};

const FullscreenDashboards: React.FC<{ dashboardId: string }> = ({ dashboardId }) => {
  const [widgets, setWidgets] = useState<WidgetRetrieveData[] | undefined>([]);

  useEffect(() => {
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

      setWidgets(widgetsTemp);
    });

    let tempWidgets: WidgetRetrieveData[] = [];
    let dashboardLabel = '';
    if (dashboardId) {
      setWidgets(undefined);
      const dashboardData = window.localStorage.getItem(
        `${fregeManualDashboardPrefix}${encodeURI(dashboardId)}`
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
          });
        });
        dashboardLabel = parsedDashboard.label;
      }
    }
  }, [dashboardId]);

  if (dashboardId === '') {
    return <NotFound />;
  }

  if (widgets) {
    return <ShowWidgets widgets={widgets} hubId={`${dashboardId}`} />;
  }

  return <Loading />;
};

export default FullscreenDashboards;
