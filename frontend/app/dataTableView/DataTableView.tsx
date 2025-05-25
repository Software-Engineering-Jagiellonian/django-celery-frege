'use client';

import React, { useState, useEffect } from 'react';
import styles from './DataTableView.module.scss';
import { analyzedStatus } from './utils/analyzedStatus';
import { getRepoMetrics } from './utils/getRepoMetrics';
import { languagesSet } from './utils/languagesSet';
import { RepositoryFileItem } from './utils/RepositoryFileItem';

export const rowLimit = 100;

const getDateStringRepr = (timestamp: number) => {
  const d = new Date(timestamp);
  return d.toUTCString();
};

const getMetricsCellRepr = (metricsString: string) => {
  if (metricsString === '') return <></>;
  const metrics = JSON.parse(metricsString);
  const keys = Object.keys(metrics);

  return (
    <div className={styles.metricsCell}>
      {keys.map((key: string, i: number) => (
        <React.Fragment key={i}>
          <div className={styles.metricsInfo}>
            <div>{key}:</div>
            <div>{metrics[key]}</div>
          </div>
          <hr />
        </React.Fragment>
      ))}
    </div>
  );
};

const DataTableView = () => {
  const [page, setPage] = useState<number>(0);
  const [languages, setLanguages] = useState<string[]>([]);
  const [analyzed, setAnalyzed] = useState<number>(0);
  const [data, setData] = useState<RepositoryFileItem[]>([]);

  const getData = async (page: number, languages: string[], analyzed: number) => {
    const metricsData = await Promise.resolve(getRepoMetrics(page, languages, analyzed));
    setData(metricsData);
  };

  useEffect(() => {
    getData(0, [], 0);
  }, []);

  const handleLanguageClick = (language: string) => {
    let tmp = [];
    if (languages.some((lan) => lan === language)) {
      tmp = languages.filter((lan) => lan !== language);
      setLanguages(tmp);
    } else {
      tmp = [...languages, language];
      setLanguages(tmp);
    }
    getData(page, tmp, analyzed);
  };

  const handlePageClick = (e: { target: { value: string | number } }) => {
    if (typeof e.target.value === 'number') {
      setPage(e.target.value);
      getData(e.target.value, languages, analyzed);
    } else {
      const tmp = isNaN(parseInt(e.target.value)) ? 0 : parseInt(e.target.value);
      setPage(tmp);
      getData(tmp, languages, analyzed);
    }
  };

  const handleStateClick = (e: { target: { value: string } }) => {
    setAnalyzed(parseInt(e.target.value));
    getData(page, languages, parseInt(e.target.value));
  };

  return (
    <div>
      <div className={styles.languageOptionsRow}>
        <h6>Filter by language</h6>
        <div className={styles.languageRow}>
          {languagesSet.map((el, i) => (
            <div
              className={
                languages.some((lan) => lan === el)
                  ? styles.languageSelected
                  : styles.languageNotSelected
              }
              key={i}
              onClick={() => handleLanguageClick(el)}>
              {el}
            </div>
          ))}
        </div>
      </div>

      <div className={styles.optionsRow}>
        <div>
          <h6>Filter by state</h6>
          <select className={styles.selectDropdown} onChange={handleStateClick} value={analyzed}>
            {analyzedStatus.map((el, i) => (
              <option className={styles.selectOption} key={i} value={el.value}>
                {el.name}
              </option>
            ))}
          </select>
        </div>

        <div>
          <h6>Goto Page</h6>
          <input
            type="number"
            className={styles.pageSelector}
            value={page}
            onChange={handlePageClick}
          />
        </div>
      </div>

      <hr />

      <table className={styles.metricsTable}>
        <thead>
          <tr className={styles.row}>
            <th className={styles.rowHeader}>Id</th>
            <th className={styles.rowHeader}>Analyzed</th>
            <th className={styles.rowHeader}>Language</th>
            <th className={styles.rowHeader}>Repo Relative File Path</th>
            <th className={styles.rowHeader}>Metrics</th>
            <th className={styles.rowHeader}>Analyzed Time</th>
            <th className={styles.rowHeader}>Repository Id</th>
          </tr>
        </thead>

        <tbody>
          {data.map((log, i) => (
            <tr key={i} className={styles.row}>
              <td className={styles.cell}>{log.id}</td>
              <td className={styles.cell}>{log.analyzed ? 'True' : 'False'}</td>
              <td className={styles.cell}>{log.language}</td>
              <td className={styles.cell}>{log.repo_relative_file_path}</td>
              <td className={styles.cell}>{getMetricsCellRepr(log.metrics || '')}</td>
              <td className={styles.cell}>{getDateStringRepr(log.analyzed_time || 0)}</td>
              <td className={styles.cell}>{log.repository_id}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default DataTableView;
