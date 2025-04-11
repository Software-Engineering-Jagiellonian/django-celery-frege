import { Layout, Layouts } from 'react-grid-layout';
import { VisibleLayout, WidgetRetrieveData } from './hubTypes';
import { columnsAmount, getId, widgetWidth } from './WidgetsHub';

export const calculateInitialLayout = (widgets: WidgetRetrieveData[]): Layout[] => {
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
    i += widgetWidth;
    return layout;
  });
};

export const saveCurrentLayout = (hubId: string, layout: Layouts) => {
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

export const getInitialLayout = (hubId: string, widgets: WidgetRetrieveData[]): Layout[] => {
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
  } else return calculateInitialLayout(widgets);
};
