import React, { useState } from 'react';
import { Box2Fill, Braces } from 'react-bootstrap-icons';
import { SideMenuItemDTO } from '../sideMenu/SideMenuStruct';
import { MenuItem } from './MenuItem';
import { ServicesItem, servicesComponents } from '../pages/services/Services';

const maplogsToSubnodes = (logs: ServicesItem[]) => {
  const result = []

  for (const el of logs){
    result.push({
      label: el.label, 
      href: `/services/${el.label.toLowerCase()}`,
      icon: <Braces />
    })
  }

  return result
}

export const logsSources: SideMenuItemDTO = {
  label: 'Services',
  icon: <Box2Fill />,
  subNodes: maplogsToSubnodes(servicesComponents),
}

const Services = () => {
  const [activeItem, setActiveItem] = useState<string>('/');

  return (
    <MenuItem
      presentationProps={logsSources}
      isActive={(e: string) => e === activeItem}
      handleClick={setActiveItem}
    />
  )
}

export default Services