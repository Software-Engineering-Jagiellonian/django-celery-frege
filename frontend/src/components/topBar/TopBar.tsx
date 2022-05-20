import React, { FC } from 'react';
import styles from './navbar.module.scss';
import { MenuAppFill } from 'react-bootstrap-icons';

interface TopBarProps {
  onMenuClick: () => void;
}

const Topbar: FC<TopBarProps> = ({ onMenuClick }) => {
  return (
    <div className={styles.navbar}>
      <button className={styles.menuButton} onClick={onMenuClick}>
        <MenuAppFill />
      </button>
    </div>
  );
};

export default Topbar;
