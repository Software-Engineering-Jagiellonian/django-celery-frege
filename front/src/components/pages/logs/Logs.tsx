import React, { ReactNode } from 'react';
// import { useParams } from 'react-router-dom';

import Flower from './Flower/Flower';

export type LogsItem = {
  label: string;
  component: ReactNode;
};

export const logsComponents: LogsItem[] = [
  {
    label: 'Flower',
    component: <Flower />
  }
];

const Logs = () => {
  // const { source } = useParams();
  // return (
  //   <>
  //     {logsComponents.find((el: LogsItem) => el.label.toLowerCase() === source)?.component || (
  //       <div>Unknown source</div>
  //     )}
  //   </>
  // );
};

export default Logs;
