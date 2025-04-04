import React from 'react';
import ContributorsList from '../../src/components/autorsList/ContributorsList';
import styles from './home.module.scss';

function Home() {
  return (
    <div>
      <div className={styles.coordinators}>
        <h3>Project Coordinators</h3>
        <ul>
          <li>Jarek Hryszko</li>
          <li>Michał Piotrowski</li>
          <li>Adam Roman</li>
        </ul>
      </div>
      <h3>Project Contributors</h3>
      <ContributorsList />
    </div>
  );
}
export default Home;
