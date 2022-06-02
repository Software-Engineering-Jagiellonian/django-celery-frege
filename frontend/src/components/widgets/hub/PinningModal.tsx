import styles from './widgetsHub.module.scss';
import { StyledButton } from '../../styledButton/StyledButton';
import { StyledModal } from '../../styledModal/StyledModal';
import React, { FC } from 'react';
import { getId, widgetWidth } from './WidgetsHub';
import { WidgetRetrieveData } from './hubTypes';
import { Layouts } from 'react-grid-layout';

export interface PinningModalProps {
  showPinModal: boolean;
  widgets: WidgetRetrieveData[];
  visibleWidgets: Record<string, WidgetRetrieveData>;
  setShowPinModal: (b: boolean) => void;
  layout: Layouts;
  setVisibleWidgets: (w: Record<string, WidgetRetrieveData>) => void;
  setLayout: (l: Layouts) => void;
}

export const PinningModal: FC<PinningModalProps> = ({
  showPinModal,
  widgets,
  visibleWidgets,
  setShowPinModal,
  layout,
  setVisibleWidgets,
  setLayout
}) => {
  return (
    <StyledModal show={showPinModal} header={'Pin/Unpin'} onSave={() => setShowPinModal(false)}>
      <>
        {widgets
          .sort((x, y) => {
            const dashboardsCmp = x.dashboardName.localeCompare(y.dashboardName);
            return dashboardsCmp !== 0
              ? dashboardsCmp
              : x.widgetName.localeCompare(y.dashboardName);
          })
          .map((widget) => {
            const widgetId = getId(widget.dashboardId, widget.widgetId);
            const onClickHandler = () => {
              const updatedVisibleWidgets = { ...visibleWidgets };
              if (visibleWidgets[widgetId]) delete updatedVisibleWidgets[widgetId];
              else updatedVisibleWidgets[widgetId] = widget;

              let updatedLayout;
              if (!visibleWidgets[widgetId]) {
                updatedLayout = [
                  ...layout.md,
                  {
                    w: widgetWidth,
                    h: widgetWidth,
                    i: widgetId,
                    minH: widgetWidth,
                    minW: widgetWidth,
                    x: 0,
                    y: 0
                  }
                ];
              } else {
                updatedLayout = layout.md.filter((layout) => layout.i !== widgetId);
              }
              setVisibleWidgets(updatedVisibleWidgets);
              setLayout({ md: updatedLayout });
            };
            return (
              <div key={widgetId} className={styles.pinningListItem}>
                {`${widget.dashboardName} / ${widget.widgetName}`}
                <StyledButton onClick={onClickHandler} className={styles.listStyledButton}>
                  {visibleWidgets[widgetId] ? 'Unpin' : 'Pin'}
                </StyledButton>
              </div>
            );
          })}
      </>
    </StyledModal>
  );
};
