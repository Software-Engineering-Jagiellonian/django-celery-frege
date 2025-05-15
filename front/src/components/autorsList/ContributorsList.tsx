import React from 'react';
import styles from './ContributorsList.module.scss';
import { contributors } from './contributors';

function ContributorsList() {
  return (
    <div className={styles.contributorsList}>
      {Object.entries(contributors).map(([year, contributors]) => {
        return (
          <div key={year}>
            <h5 className={styles.year}>{year}</h5>
            <ul>
              {contributors.map((contributor) => (
                <li key={contributor}>{contributor}</li>
              ))}
            </ul>
          </div>
        );
      })}
    </div>
  );
}

export default ContributorsList;
