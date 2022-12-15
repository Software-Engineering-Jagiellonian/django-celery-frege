import React, { FC, useEffect, useState } from 'react';
import { Layouts, Responsive, WidthProvider } from 'react-grid-layout';
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
import { VisibleLayout, WidgetRetrieveData } from './hubTypes';
import { calculateInitialLayout, getInitialLayout, saveCurrentLayout } from './layoutClient';
import { PinningModal } from './PinningModal';

export const columnsAmount = 20;
export const widgetWidth = 4;
export const getId = (dashboardId: string, widgetId: string): string =>
  `${dashboardId}-${widgetId}`;
export const ResponsiveGridLayout = WidthProvider(Responsive);

export interface WidgetsHubProps {
  widgets: WidgetRetrieveData[];
  hubId: string;
}

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

  const [showSaveModal, setShowSaveModal] = useState<boolean>(false);
  const [showResetModal, setShowResetModal] = useState<boolean>(false);
  const [visibleWidgets, setVisibleWidgets] = useState<Record<string, WidgetRetrieveData>>({});
  const [showPinModal, setShowPinModal] = useState<boolean>(false);
  const [layout, setLayout] = useState<Layouts>({});

  useEffect(() => {
    setVisibleWidgets(getInitialVisibleWidgets());
    setLayout({
      md: getInitialLayout(hubId, widgets)
    });
  }, [widgets]);

  const resetLayout = () => {
    setLayout({
      md: calculateInitialLayout(widgets)
    });
  };

  const unpinHandler = (widget: WidgetRetrieveData) => {
    const widgetId = getId(widget.dashboardId, widget.widgetId);
    const widgets = { ...visibleWidgets };
    delete widgets[widgetId];
    setVisibleWidgets(widgets);

    const localLayout = { ...layout };
    setLayout({ md: localLayout.md.filter((layout) => layout.i !== widgetId) });
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
          }
        >
          {Object.values(visibleWidgets).map((widget: WidgetRetrieveData) => (
            <div key={getId(widget.dashboardId, widget.widgetId)} className={styles.widget}>
              <div className={styles.dragHeader}>
                <ArrowsMove />
              </div>
              <div className={styles.unpinButton} onClick={() => unpinHandler(widget)}>
                <Trash3 />
              </div>
              <div className={styles.widgetContent}>
                <iframe
                  src={`/grafana/d-solo/${widget.dashboardId}/dashboard-1?orgId=1&panelId=${widget.widgetId}`}
                  width="100%"
                  height="100%"
                  frameBorder="0"
                  className={styles.graphFrame}
                ></iframe>
              </div>
            </div>
          ))}
        </ResponsiveGridLayout>
      </div>
      <StyledModal
        show={showSaveModal}
        onSave={() => {
          saveCurrentLayout(hubId, layout);
          setShowSaveModal(false);
        }}
        onCancel={() => setShowSaveModal(false)}
        header={'Save'}
      >
        Are you sure, you want to override the layout?
      </StyledModal>
      <StyledModal
        show={showResetModal}
        onSave={() => {
          resetLayout();
          setShowResetModal(false);
        }}
        onCancel={() => setShowResetModal(false)}
        header={'Reset'}
      >
        Are you sure, you want to reset the layout? <br /> Remember to save changes, if you want
        them to take effect
      </StyledModal>
      <PinningModal
        setShowPinModal={setShowPinModal}
        showPinModal={showPinModal}
        layout={layout}
        setLayout={setLayout}
        setVisibleWidgets={setVisibleWidgets}
        visibleWidgets={visibleWidgets}
        widgets={widgets}
      />
    </>
  );
};
