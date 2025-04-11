'use client';

import React from 'react';
import { Table } from 'react-bootstrap-icons';
import styles from './MenuItem.module.scss';
import Link from 'next/link';

const DataTableView = () => {
  return (
    <div className={styles.menuItem}>
      <Link href="/dataTableView">
        <div className={styles.menuItem}>
          <div className={styles.iconContainer}>
            <Table />
          </div>
          <div className={styles.label}>Data Table View</div>
        </div>
      </Link>
    </div>
  );
};

export default DataTableView;
