import React, { FC } from 'react';
import styles from './navbar.module.scss';
import { List } from 'react-bootstrap-icons';
import { Link } from 'react-router-dom';
import { User } from '../widgets/user/User';

interface TopBarProps {
  onMenuClick: () => void;
}

export const Navbar: FC<TopBarProps> = ({ onMenuClick }) => {
  return (
    <div className={styles.navbar}>
      <div className={styles.leftAligned}>
        <button className={styles.navbarButton} onClick={onMenuClick}>
          <List size={28} color="white" />
        </button>
        <Link to="/" className={styles.logo}>
          <img src="/logo-frege.png" width="60" height="48" alt="logo" />
        </Link>
        <h1 className={styles.title}>Frege</h1>
      </div>

      <div className={styles.rightAligned}>
        <User />
      </div>
    </div>
  );
};
