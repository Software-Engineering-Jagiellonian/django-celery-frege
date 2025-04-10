import React from 'react';
import { PeopleFill } from 'react-bootstrap-icons';
import styles from './MenuItem.module.scss';
import Link from 'next/link';

const Users = () => {
  return (
    <Link href="/users">
      <div className={styles.menuItem}>
        <div className={styles.iconContainer}>
          <PeopleFill />
        </div>
        <div className={styles.label}>All users</div>
      </div>
    </Link>
  );
};

export default Users;
