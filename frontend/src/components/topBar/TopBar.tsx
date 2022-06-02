import React, { FC } from 'react';
import styles from './navbar.module.scss';
import { MenuAppFill } from 'react-bootstrap-icons';
import { StyledButton } from '../styledButton/StyledButton';

interface TopBarProps {
  onMenuClick: () => void;
}

export const TopBar: FC<TopBarProps> = ({ onMenuClick }) => {
  return (
    <div className={styles.navbar}>
      <StyledButton className={styles.menuButton} onClick={onMenuClick}>
        <MenuAppFill />
      </StyledButton>
    </div>
  );
};
