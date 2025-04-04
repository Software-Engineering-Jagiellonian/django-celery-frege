import axios, { AxiosRequestConfig } from 'axios';
import React, { useState, useEffect } from 'react';
import styles from '../Flower.module.scss';
import Sublist from './Sublist';
import { targetFlower, portFlower } from '../../../logs/Flower/Flower';

type FlowerAPIDataI = any;

export const getFlowerApiData = async (endpoint: string): Promise<FlowerAPIDataI> => {
  const baseUrl = `http://${targetFlower}:${portFlower}/api`;
  const url = baseUrl + endpoint;
  let apiData: FlowerAPIDataI = {};

  await axios
    .get(url)
    .then(async (response: any) => {
      apiData = response.data;
    })
    .catch(function (error) {
      throw Error(error);
    });

  return apiData;
};

const FlowerAPIBrowser = () => {
  const [data, setData] = useState<FlowerAPIDataI>({});
  const [error, setError] = useState<string>('');

  const getData = async (request: string) => {
    getFlowerApiData(request)
      .then((r) => {
        setData(r);
        setError('');
      })
      .catch((err) => setError(err.message));
  };

  const baseRequests = ['/workers', '/tasks', '/task/types', '/queues/length'];

  return (
    <div>
      <h4>Basic Requests</h4>
      <ul>
        {baseRequests.map((request: string) => (
          <li key={request} onClick={() => getData(request)} className={styles.subLink}>
            {request}
          </li>
        ))}
      </ul>

      <hr />

      {error !== '' && <div className={styles.errorMessage}>{error}</div>}

      <div className={styles.list}>
        {Object.entries(data).map(([key, value]: [string, any]) => (
          <Sublist key={key} property={key} obj={value} />
        ))}
      </div>
    </div>
  );
};

export default FlowerAPIBrowser;
