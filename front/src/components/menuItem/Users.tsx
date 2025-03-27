import React, { FC, useState, MouseEvent } from 'react';
import { PeopleFill } from 'react-bootstrap-icons';
// import { useNavigate } from 'react-router-dom';
import styles from './MenuItem.module.scss';

const Users = () => {
  // const navigate = useNavigate();

  // const onMenuItemClick = (e: { stopPropagation: () => void }) => {
  //   navigate('/users');
  //   e.stopPropagation();
  // };

  return (
    // <div className={styles.menuItem} onClick={onMenuItemClick}>
    <div className={styles.menuItem}>
      <div className={styles.iconContainer}>
        <PeopleFill />
      </div>
      <div className={styles.label}>All users</div>
    </div>
  );
};

export default Users;
