import React, { FC, useEffect, useState } from 'react';
import 'bootstrap/dist/css/bootstrap.min.css';
import styles from './users.module.scss';
import { getUsers } from './utils/getUsers';
import { User } from './User';

export interface UserI {
  id: number;
  name: string;
  login: string;
  email: string;
  isAdmin: boolean;
  isDisabled: boolean;
  lastSeenAt: string;
  lastSeenAtAge: string;
  authLabels: Array<string>;
}

export const Users = () => {
  const [users, setUsers] = useState<Array<UserI>>([]);
  const [page, setPage] = useState<number>(1);
  const [error, setError] = useState<string>('');

  useEffect(() => {
    getUsers(page)
      .then((r) => {
        setUsers(r);
        setError('');
      })
      .catch((err) => setError(err.message));
  }, [page]);

  return (
    <div className={styles.usersWrapper}>
      <div className={styles.actionsRow}>
        <div>Page</div>
        <input
          type="number"
          className={styles.pageSelector}
          value={page}
          onChange={(e) => setPage(parseInt(e.target.value))}
        />
      </div>

      <hr />

      {error !== '' && (
        <div className={styles.errorMessage}>
          {error}. You must be logged in as admin in order to access this resource.
        </div>
      )}

      <div className={styles.usersList}>
        <div />
        <div className={styles.userHeader}>Login</div>
        <div className={styles.userHeader}>Email</div>
        <div className={styles.userHeader}>Admin?</div>
        <div className={styles.userHeader}>Disabled?</div>
        <div className={styles.userHeader}>Last seen</div>

        {users.map((user: UserI) => (
          <User key={user.id} user={user} />
        ))}
      </div>
    </div>
  );
};
