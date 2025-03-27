import { ReactNode } from 'react';

export type SideMenuItemDTO = {
  label: string;
  href?: string;
  subNodes?: SideMenuItemDTO[];
  icon?: ReactNode;
  structOptions?: Array<ReactNode>;
};
