import React, { ReactNode } from 'react';
import { useParams } from 'next/navigation';

import Django from './django/Django';
import Flower from './flower/Flower';

export type ServicesItem = {
  label: string;
  component: ReactNode;
};

export const servicesComponents: ServicesItem[] = [
  {
    label: 'Django',
    component: <Django />
  },
  {
    label: 'Flower',
    component: <Flower />
  }
];

const Services = () => {
  const { source } = useParams();
  return (
    <>
      {servicesComponents.find((el: ServicesItem) => el.label.toLowerCase() === source)
        ?.component || <div>Unknown source</div>}
    </>
  );
};

export default Services;
