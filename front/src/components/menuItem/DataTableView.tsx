import React, { FC, useState, MouseEvent } from 'react';
import { CaretRight, Table } from 'react-bootstrap-icons';
// import { useNavigate } from 'react-router-dom';
import styles from './MenuItem.module.scss';

const DataTableView = () => {
  // const navigate = useNavigate();

  // const onMenuItemClick = (e: { stopPropagation: () => void }) => {
  //   navigate('/datatableview');
  //   e.stopPropagation();
  // };

  return (
    // <div className={styles.menuItem} onClick={onMenuItemClick}>
    <div className={styles.menuItem}>
      <div className={styles.iconContainer}>
        <Table />
      </div>
      <div className={styles.label}>Data Table View</div>
    </div>
  );
};

export default DataTableView;
