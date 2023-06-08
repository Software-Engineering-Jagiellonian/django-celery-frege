import axios, { AxiosRequestConfig } from 'axios';
import React, { useState, useEffect } from 'react';
import styles from '../Flower.module.scss';
import { targetFlower, portFlower } from '../../../logs/Flower/Flower';
import { X, XLg } from 'react-bootstrap-icons';

export const getFlowerWorkerData = async (): Promise<Array<string>> => {
    const url = `http://${targetFlower}:${portFlower}/api/workers`
    let apiData: Array<string> = []

    await axios.get(url)
    .then(async (response: any) => {
        apiData = response.data
        apiData = Object.keys(apiData)
    })
    .catch(function (error) {
        throw Error(error)
    });
   
    return apiData;
};

export const postShutdownWorker = async (name: string): Promise<any> => {
    const url = `http://${targetFlower}:${portFlower}/api/worker/shutdown/${name}`
    let message = ""

    await axios.post(url)
    .then(async (response: any) => {
        message = response.data
    })
    .catch(function (error) {
        throw Error(error)
    });
   
    return message;
}

const WorkerShutdown = () => {
    const [data, setData] = useState<Array<string>>([]);
    const [message, setMessage] = useState<{color: string, text: string}>({color: "green", text: ""});

    const getData = async () => {
        getFlowerWorkerData()
        .then(r => {setData(r); setMessage({color: "green", text: ""})})
        .catch(err => setMessage({color: "red", text: err.message}))
    }

    const shutdownWorker = async (name: string) => {
        postShutdownWorker(name)
        .then(r => {setMessage({color: "green", text: r.message})})
        .catch(err => setMessage({color: "red", text: err.message}))
    }

    useEffect(() => {
        getData()
    }, [])
 
    return (
    <div>
        {message.text !== "" && <div className={styles.errorMessage} style={{color: message.color}}>{message.text}</div>}
        <h5>Active workers:</h5>
        <ul className={styles.workersList}>
            {data.map((worker: string) => <li className={styles.workerItem} key={worker}><XLg onClick={() => shutdownWorker(worker)} />{worker}</li>)}
        </ul>
    </div>
    )
}

export default WorkerShutdown