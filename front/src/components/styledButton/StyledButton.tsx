import React, { FC } from 'react';
import styles from './styledButton.module.scss';
import { ButtonProps } from 'react-bootstrap';

export const StyledButton: FC<ButtonProps> = (props) => {
  const classes = props.className ? `${styles.menuButton} ${props.className}` : styles.menuButton;
  return (
    <button {...props} className={classes} type="button">
      {props.children}
    </button>
  );
};
