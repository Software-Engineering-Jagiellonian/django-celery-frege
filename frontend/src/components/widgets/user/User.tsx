import React, { FC, useEffect, useState } from 'react';
import 'bootstrap/dist/css/bootstrap.min.css';
import styles from './user.module.scss';
import { StyledButton } from '../../styledButton/StyledButton';
import axios from "axios";
import { useNavigate } from 'react-router-dom';

export const getUser = async () => {
    let result: any
    result = null

    const config = {
        method: 'get',
        url: `grafana/api/user`,
        headers: { }
    };
      
    await axios(config)
    .then(function (response) {
        result = response.data
    })
    .catch(function (error) {
        console.log(error)
    });

    return result
}

export interface minimalUserI {
    name: string
    avatarUrl: string
}

export const User = () => {
    const [user, setUser] = useState<null | minimalUserI>(null);
    const navigate = useNavigate();

    useEffect(() => {
        getUser()
        .then(r => {
            if (r === null) setUser(null)
            else setUser({
                name: r.login,
                avatarUrl: r.avatarUrl
            })
        })
    }, []);

    if (user === null) return (
        <>
            <div className={styles.userWrapper}>
                <a href="/grafana/login"><StyledButton className={styles.loginButton}>Login</StyledButton></a>
            </div>
        </>  
    )

    return (
        <div className={styles.userWrapper} onClick={() => navigate("/sessions")}>
            <div className={styles.userName}>{user.name}</div>
            <div className={styles.userIcon}><img src={user.avatarUrl} alt="user icon" /></div>
        </div>
    );
};
