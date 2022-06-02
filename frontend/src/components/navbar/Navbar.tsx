import React, { FC } from 'react';
import styles from './navbar.module.scss';
import { MenuAppFill } from 'react-bootstrap-icons';
import { StyledButton } from '../styledButton/StyledButton';
import {Link} from "react-router-dom";

interface TopBarProps {
  onMenuClick: () => void;
}

export const Navbar: FC<TopBarProps> = ({ onMenuClick }) => {
  return (
    <div className={styles.navbar}>
        <Link to="/" className={styles.logo} >
            <img src="/logo-frege.png" width="60" height="45" className="d-inline-block align-top navbr-image" alt="logo"/>
            </Link>
        <h1 className={styles.title}>
            Frege
        </h1>
      <StyledButton className={styles.menuButton} onClick={onMenuClick}>
        <MenuAppFill />
      </StyledButton>
    </div>
  );
};
