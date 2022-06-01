import React, { FC, useState } from 'react';
import { Layout, Layouts, Responsive, WidthProvider } from 'react-grid-layout';
import 'bootstrap/dist/css/bootstrap.min.css';
import styles from './widgetsHub.module.scss';
import {
  ArrowsAngleExpand,
  ArrowsMove,
  Back,
  PlusSlashMinus,
  Save,
  Trash3
} from 'react-bootstrap-icons';
import { StyledButton } from '../../styledButton/StyledButton';
import { StyledModal } from '../../styledModal/StyledModal';

const ResponsiveGridLayout = WidthProvider(Responsive);
export interface WidgetRetrieveData {
  dashboardId: string;
  widgetId: string;
  dashboardName: string;
  widgetName: string;
}

export interface WidgetsHubProps {
  widgets: WidgetRetrieveData[];
  hubId: string;
}

type VisibleLayout = {
  x: number;
  y: number;
  w: number;
  h: number;
  i: string;
  d: string;
};

export const WidgetsHub: FC<WidgetsHubProps> = ({ widgets, hubId }) => {
  const getInitialVisibleWidgets = (): Record<string, WidgetRetrieveData> => {
    const layoutFromStorage = window.localStorage[`frege-${hubId}`];
    if (layoutFromStorage) {
      const parsedLayout = JSON.parse(layoutFromStorage) as VisibleLayout[];
      const visibleIds = new Set(parsedLayout.map((layout) => getId(layout.d, layout.i)));

      return widgets.reduce((prev, curr) => {
        const widgetId = getId(curr.dashboardId, curr.widgetId);
        if (visibleIds.has(widgetId)) {
          prev[widgetId] = curr;
        }

        return prev;
      }, {} as Record<string, WidgetRetrieveData>);
    }

    return widgets.reduce((prev, curr) => {
      prev[getId(curr.dashboardId, curr.widgetId)] = curr;
      return prev;
    }, {} as Record<string, WidgetRetrieveData>);
  };

  const columnsAmount = 20;
  const widgetWidth = 4;
  const getId = (dashboardId: string, widgetId: string): string => `${dashboardId}-${widgetId}`;
  const [showSaveModal, setShowSaveModal] = useState<boolean>(false);
  const [showResetModal, setShowResetModal] = useState<boolean>(false);
  const [visibleWidgets, setVisibleWidgets] = useState<Record<string, WidgetRetrieveData>>(
    getInitialVisibleWidgets()
  );
  const [showPinModal, setShowPinModal] = useState<boolean>(false);

  const countLayout = (): Layout[] => {
    let i = 0;
    return widgets.map((widget) => {
      const layout = {
        x: Math.floor((i % columnsAmount) / widgetWidth) * widgetWidth,
        y: Math.floor(i / columnsAmount),
        w: widgetWidth,
        h: widgetWidth,
        i: getId(widget.dashboardId, widget.widgetId),
        minH: widgetWidth,
        minW: widgetWidth
      };
      i += 4;
      return layout;
    });
  };

  const getInitialLayout = (): Layout[] => {
    const layoutFromStorage = window.localStorage[`frege-${hubId}`];

    if (layoutFromStorage) {
      const parsedLayout = JSON.parse(layoutFromStorage);

      return parsedLayout.map((layout: VisibleLayout) => ({
        x: layout.x,
        y: layout.y,
        w: layout.w,
        h: layout.h,
        i: getId(layout.d, layout.i),
        minH: widgetWidth,
        minW: widgetWidth
      }));
    } else return countLayout();
  };

  const [layout, setLayout] = useState<Layouts>({
    md: getInitialLayout()
  });

  const saveCurrentLayout = () => {
    window.localStorage[`frege-${hubId}`] = JSON.stringify(
      layout.md.map((layout) => ({
        x: layout.x,
        y: layout.y,
        w: layout.w,
        h: layout.h,
        i: layout.i.split('-')[1],
        d: layout.i.split('-')[0]
      }))
    );
  };

  const resetLayout = () => {
    setLayout({
      md: countLayout()
    });
  };

  return (
    <>
      <div className={styles.widgetsHub}>
        <div className={styles.actions}>
          <StyledButton onClick={() => setShowSaveModal(true)}>
            <Save />
          </StyledButton>
          <StyledButton onClick={() => setShowResetModal(true)}>
            <Back />
          </StyledButton>
          <StyledButton>
            <PlusSlashMinus onClick={() => setShowPinModal(true)} />
          </StyledButton>
        </div>
        <ResponsiveGridLayout
          compactType={null}
          className={styles.widgetsHubGrid}
          rowHeight={80}
          draggableHandle={`.${styles.dragHeader}`}
          breakpoints={{ md: 0 }}
          cols={{ md: 20 }}
          layouts={layout}
          onLayoutChange={(curr, all) => setLayout(all)}
          resizeHandle={
            <div className={styles.resizeHandler}>
              <ArrowsAngleExpand />
            </div>
          }>
          {Object.values(visibleWidgets).map((widget: WidgetRetrieveData) => (
            <div key={getId(widget.dashboardId, widget.widgetId)} className={styles.widget}>
              <div className={styles.dragHeader}>
                <ArrowsMove />
              </div>
              <div
                className={styles.unpinButton}
                onClick={() => {
                  const widgetId = getId(widget.dashboardId, widget.widgetId);
                  const widgets = { ...visibleWidgets };
                  delete widgets[widgetId];
                  setVisibleWidgets(widgets);

                  const localLayout = { ...layout };
                  setLayout({ md: localLayout.md.filter((layout) => layout.i !== widgetId) });
                }}>
                <Trash3 />
              </div>
              <div className={styles.widgetContent}>
                <iframe
                  src={`http://localhost:3000/d-solo/${widget.dashboardId}/dashboard-1?orgId=1&from=1653655032721&to=1653676632721&panelId=${widget.widgetId}`}
                  width="100%"
                  height="100%"
                  frameBorder="0"></iframe>
              </div>
            </div>
          ))}
        </ResponsiveGridLayout>
      </div>
      <StyledModal
        show={showSaveModal}
        onSave={() => {
          saveCurrentLayout();
          setShowSaveModal(false);
        }}
        onCancel={() => setShowSaveModal(false)}
        header={'Save'}>
        Are you sure, you want to override the layout?
      </StyledModal>
      <StyledModal
        show={showResetModal}
        onSave={() => {
          resetLayout();
          setShowResetModal(false);
        }}
        onCancel={() => setShowResetModal(false)}
        header={'Reset'}>
        Are you sure, you want to reset the layout? <br /> Remember to save changes, if you want
        them to take effect
      </StyledModal>
      <StyledModal show={showPinModal} header={'Pin/Unpin'} onCancel={() => setShowPinModal(false)}>
        <>
          {
            // TODO: in separated task
            widgets
              .sort((x, y) => {
                const dashboardsCmp = x.dashboardName.localeCompare(y.dashboardName);
                return dashboardsCmp !== 0
                  ? dashboardsCmp
                  : x.widgetName.localeCompare(y.dashboardName);
              })
              .map((widget) => {
                const widgetId = getId(widget.dashboardId, widget.widgetId);
                return (
                  <div key={widgetId}>{`${widget.dashboardName} / ${
                    widget.widgetName
                  }      ${!!visibleWidgets[widgetId]}`}</div>
                );
              })
          }
        </>
      </StyledModal>
    </>
  );
};
