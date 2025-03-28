import React, { FC, useEffect, useState } from 'react';
import 'bootstrap/dist/css/bootstrap.min.css';
import styles from './user.module.scss';
import { CheckLg, Person, XLg } from 'react-bootstrap-icons';
import { UserI } from './Users';

export const User: React.FC<{ user: UserI }> = ({ user }) => {
  return (
    <>
      <div className={styles.personIcon}>
        <Person />
      </div>
      <div className={styles.personInfo}>{user.login}</div>
      <div className={styles.personInfo}>{user.email}</div>
      {user.isAdmin ? (
        <div className={styles.userConfirmed}>
          <CheckLg />
        </div>
      ) : (
        <div className={styles.userNotConfirmed}>
          <XLg />
        </div>
      )}
      {user.isDisabled ? (
        <div className={styles.userConfirmed}>
          <CheckLg />
        </div>
      ) : (
        <div className={styles.userNotConfirmed}>
          <XLg />
        </div>
      )}
      <div className={styles.personInfo}>{user.lastSeenAtAge} ago</div>
    </>
  );
};
