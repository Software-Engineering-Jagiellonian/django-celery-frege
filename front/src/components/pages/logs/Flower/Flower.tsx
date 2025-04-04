import axios, { AxiosRequestConfig } from 'axios';
import React, { useState, useEffect } from 'react';
import { ArrowRepeat } from 'react-bootstrap-icons';
import styles from './Flower.module.scss';
import { FlowerLog } from './utils/FlowerLog';

export const targetFlower = process.env.DOCKER_FLOWER_HOST || 'localhost';
export const portFlower = process.env.DOCKER_FLOWER_PORT || '5555';

export const getFlowerLogs = async (): Promise<FlowerLog[]> => {
  let logsData: FlowerLog[] = [];
  await axios.get(`http://${targetFlower}:${portFlower}/api/tasks`).then(async (response) => {
    logsData = Object.values(response.data);
    return response.data;
  });
  return logsData;
};

const getDateStringRepr = (timestamp: number) => {
  const d = new Date(timestamp * 1000);
  return d.toUTCString();
};

const filterByType = (e: FlowerLog, filterType: string) => {
  return filterType === '---' ? true : e.name === filterType;
};

const filterByState = (e: FlowerLog, filterState: string) => {
  return filterState === '---' ? true : e.state === filterState;
};

const Flower = () => {
  const [logs, setLogs] = useState<FlowerLog[]>([]);
  const [filterType, setFilterType] = useState<string>('---');
  const [filterState, setFilterState] = useState<string>('---');
  const [reloadTimer, setReloadTimer] = useState<number>(15);

  const typeSet = Array.from(new Set(logs.map((log) => log.name)).add('---')).filter(
    (el) => el !== undefined && el !== null
  );
  const stateSet = Array.from(new Set(logs.map((log) => log.state)).add('---')).filter(
    (el) => el !== undefined && el !== null
  );

  const getLogs = async () => {
    const flowerLogs = await Promise.resolve(getFlowerLogs());
    setLogs(flowerLogs);
  };

  useEffect(() => {
    getLogs();
  }, []);

  useEffect(() => {
    const timeToReload = setInterval(() => {
      const tmp = reloadTimer - 1;
      if (tmp < 0) getLogs();
      setReloadTimer(tmp < 0 ? 15 : tmp);
    }, 1000);

    return () => {
      clearInterval(timeToReload);
    };
  });

  return (
    <div>
      <div className={styles.optionsRow}>
        <div>
          <h6>Filter by type</h6>
          <select
            className={styles.selectDropdown}
            onChange={(e) => setFilterType(e.target.value)}
            value={filterType}>
            {typeSet.map((el) => (
              <option className={styles.selectOption} key={el} value={el}>
                {el}
              </option>
            ))}
          </select>
        </div>

        <div>
          <h6>Filter by state</h6>
          <select
            className={styles.selectDropdown}
            onChange={(e) => setFilterState(e.target.value)}
            value={filterState}>
            {stateSet.map((el) => (
              <option className={styles.selectOption} key={el} value={el}>
                {el}
              </option>
            ))}
          </select>
        </div>

        <div>
          <h6>Reload Data</h6>
          <div className={styles.refreshOptions}>
            <div className={styles.refreshButton} onClick={getLogs}>
              <ArrowRepeat />
            </div>
            <div>Refreshing in... {reloadTimer}s</div>
          </div>
        </div>
      </div>

      <hr />

      <table className={styles.logsTable}>
        <thead>
          <tr className={styles.row}>
            <th className={styles.rowHeader}>Uuid</th>
            <th className={styles.rowHeader}>Name</th>
            <th className={styles.rowHeader}>State</th>
            <th className={styles.rowHeader}>Retries</th>
            <th className={styles.rowHeader}>Args</th>
            <th className={styles.rowHeader}>Kwargs</th>
            <th className={styles.rowHeader}>Received</th>
          </tr>
        </thead>

        <tbody>
          {logs
            .filter((e) => filterByState(e, filterState))
            .filter((e) => filterByType(e, filterType))
            .slice(0, 100)
            .map((log) => (
              <tr key={log.uuid} className={styles.row}>
                <td className={styles.cell}>{log.uuid}</td>
                <td className={styles.cell}>{log.name}</td>
                <td className={styles.cell}>{log.state}</td>
                <td className={styles.cell}>{log.retries}</td>
                <td className={styles.cell}>{log.args}</td>
                <td className={styles.cell}>{log.kwargs}</td>
                <td className={styles.cell}>{getDateStringRepr(log.received)}</td>
              </tr>
            ))}
        </tbody>
      </table>
    </div>
  );
};

export default Flower;
