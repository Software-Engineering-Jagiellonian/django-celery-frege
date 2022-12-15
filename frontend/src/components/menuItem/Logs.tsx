import React, { useState } from 'react';
import { CardList, BodyText } from 'react-bootstrap-icons';
import { logsComponents, LogsItem } from '../pages/logs/Logs';
import { SideMenuItemDTO } from '../sideMenu/SideMenuStruct';
import { MenuItem } from './MenuItem';

const maplogsToSubnodes = (logs: LogsItem[]) => {
  const result = []

  for (const el of logs){
    result.push({
      label: el.label, 
      href: `/logs/${el.label.toLowerCase()}`,
      icon: <BodyText />
    })
  }

  return result
}

export const logsSources: SideMenuItemDTO = {
  label: 'Logs',
  icon: <CardList />,
  subNodes: maplogsToSubnodes(logsComponents),
}

const Logs = () => {
  const [activeItem, setActiveItem] = useState<string>('/');

  return (
    <MenuItem
      presentationProps={logsSources}
      isActive={(e: string) => e === activeItem}
      handleClick={setActiveItem}
    />
  )
}

export default Logs