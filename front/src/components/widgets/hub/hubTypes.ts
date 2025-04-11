export interface WidgetRetrieveData {
  dashboardId: string;
  widgetId: string;
  dashboardName: string;
  widgetName: string;
}

export type VisibleLayout = {
  x: number;
  y: number;
  w: number;
  h: number;
  i: string;
  d: string;
};
