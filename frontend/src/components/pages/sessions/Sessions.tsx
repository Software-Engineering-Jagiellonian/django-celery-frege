import React, { FC, useEffect, useState } from 'react';
import 'bootstrap/dist/css/bootstrap.min.css';
import styles from './sessions.module.scss';
import { getSessions } from './utils/getSessions';
import { Session } from './Session';

export interface SessionI {
  id: number;
  isActive: true;
  clientIp: string;
  browser: string;
  browserVersion: string;
  os: string;
  osVersion: string;
  device: string;
  createdAt: string;
  seenAt: string;
}

export const Sessions = () => {
  const [sessions, setSessions] = useState<Array<SessionI>>([]);
  const [error, setError] = useState<string>('');

  useEffect(() => {
    getSessions()
      .then((r) => {
        setSessions(r);
        setError('');
      })
      .catch((err) => setError(err.message));
  }, []);

  return (
    <div className={styles.sessionsWrapper}>
      <h2>Active Sessions</h2>

      <hr />

      {error !== '' && (
        <div className={styles.errorMessage}>
          {error}. You must be logged in to access this resource.
        </div>
      )}

      <div className={styles.sessionsList}>
        <div className={styles.sessionHeader}>Id</div>
        <div className={styles.sessionHeader}>Status</div>
        <div className={styles.sessionHeader}>Ip</div>
        <div className={styles.sessionHeader}>Browser</div>
        <div className={styles.sessionHeader}>Os</div>
        <div className={styles.sessionHeader}>Device</div>
        <div className={styles.sessionHeader}>Created At</div>
        <div className={styles.sessionHeader}>Last Used</div>
        <div />

        {sessions.map((session: SessionI) => (
          <Session
            key={session.id}
            session={session}
            setSessions={setSessions}
            setError={setError}
          />
        ))}
      </div>
    </div>
  );
};
