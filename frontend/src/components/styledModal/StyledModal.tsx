import React, { FC, ReactNode } from 'react';
import Modal from 'react-bootstrap/Modal';
import { StyledButton } from '../styledButton/StyledButton';
import styles from './styledModal.module.scss';

interface StyledModalProps {
  children: ReactNode;
  show: boolean;
  onCancel?: () => void;
  onSave?: () => void;
  header: string;
}

export const StyledModal: FC<StyledModalProps> = ({ children, show, onCancel, onSave, header }) => {
  return (
    <Modal show={show} contentClassName={styles.modal}>
      <Modal.Header>
        <Modal.Title>{header}</Modal.Title>
      </Modal.Header>
      <Modal.Body>{children}</Modal.Body>
      <Modal.Footer>
        {onCancel ? (
          <StyledButton onClick={onCancel} className={styles.button}>
            Cancel
          </StyledButton>
        ) : undefined}
        {onSave ? (
          <StyledButton onClick={onSave} className={styles.button}>
            Ok
          </StyledButton>
        ) : undefined}
      </Modal.Footer>
    </Modal>
  );
};
