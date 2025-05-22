'use client';

import axios from 'axios';
import React, { useState, useEffect } from 'react';
import styles from './Django.module.scss';
import Sublist from './Sublist';

export const targetDjango = process.env.DOCKER_DJANGO_HOST || 'localhost';
export const portDjango = process.env.DOCKER_DJANGO_PORT || '8000';

interface DjangoAPIDataI {
  request: string;
  data: any;
}

export const getDjangoApiData = async (endpoint: string): Promise<DjangoAPIDataI> => {
  const url = endpoint !== '' ? endpoint : `http://${targetDjango}:${portDjango}/api/`;
  const apiData: DjangoAPIDataI = {
    request: url,
    data: {}
  };

  await axios
    .get(url, { withCredentials: true })
    .then(async (response: any) => {
      apiData.data = response.data;
    })
    .catch(function (error) {
      throw Error(error);
    });

  return apiData;
};

const Django = () => {
  const [data, setData] = useState<DjangoAPIDataI>({ request: '', data: {} });
  const [error, setError] = useState<string>('');

  const getData = async (request: string) => {
    getDjangoApiData(request)
      .then((r) => {
        setData(r);
        setError('');
      })
      .catch((err) => setError(err.message));
  };

  useEffect(() => {
    getData(data.request);
  }, [data.request]);

  return (
    <div>
      <h3>Django API Browser</h3>

      <hr />

      {error !== '' && (
        <div className={styles.errorMessage}>
          Please remember you need to be logged into Django to use this feature{' '}
          <a href={`http://${targetDjango}:${portDjango}`}>Log in</a>. {error}
        </div>
      )}
      <ul className={styles.list}>
        {Object.entries(data.data).map(([key, value]: [string, any]) => (
          <Sublist key={key} property={key} obj={value} setData={setData} />
        ))}
      </ul>
    </div>
  );
};

export default Django;
