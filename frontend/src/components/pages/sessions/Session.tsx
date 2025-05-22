import React, { FC, useEffect, useState } from 'react';
import 'bootstrap/dist/css/bootstrap.min.css';
import styles from './session.module.scss';
import { CheckLg, XLg } from 'react-bootstrap-icons';
import { SessionI } from './Sessions';
import { StyledButton } from '../../styledButton/StyledButton';
import { getSessions } from './utils/getSessions';
import axios from 'axios';
import { parseDate } from './utils/parseDate';

export const Session: React.FC<{
  session: SessionI;
  setSessions: (arg0: Array<SessionI>) => void;
  setError: (arg0: string) => void;
}> = ({ session, setSessions, setError }) => {
  const onRevokeClick = () => {
    const config = {
      method: 'post',
      url: `grafana/api/user/revoke-auth-token`,
      headers: {},
      data: {
        authTokenId: session.id
      }
    };

    axios(config)
      .then(function (response) {
        getSessions()
          .then((r) => {
            setSessions(r);
            setError('');
          })
          .catch((err) => setError(err.message));
      })
      .catch(function (error) {
        setError(
          `${error.message}. Please remember: You can't revoke access to your current session.`
        );
      });
  };

  return (
    <>
      <div className={styles.sessionInfoTransparent}>{session.id}</div>
      {session.isActive ? (
        <div className={styles.activeStatus}>
          <CheckLg /> active
        </div>
      ) : (
        <div className={styles.inactiveStatus}>
          <XLg /> inactive
        </div>
      )}
      <div className={styles.sessionInfoTransparent}>{session.clientIp}</div>
      <div className={styles.sessionInfo}>
        {session.browser} {session.browserVersion}
      </div>
      <div className={styles.sessionInfo}>
        {session.os} {session.osVersion}
      </div>
      <div className={styles.sessionInfo}>{session.device}</div>
      <div className={styles.sessionInfoTransparent}>{parseDate(session.createdAt)}</div>
      <div className={styles.sessionInfoTransparent}>{parseDate(session.seenAt)}</div>
      <StyledButton className={styles.revokeButton} onClick={onRevokeClick}>
        Revoke access
      </StyledButton>
    </>
  );
};
