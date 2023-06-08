import React, { useState, useEffect } from 'react';
import styles from './Flower.module.scss';
import FlowerAPIBrowser from './components/FlowerAPIBrowser';
import WorkerShutdown from './components/WorkerShutdown';

const flowerServices = [
    {
        id: -1,
        name: "------------",
        displayName: "",
        component: <></>
    },
    {
        id: 0,
        name: "Flower API Browser",
        displayName: "Flower API Browser",
        component: <FlowerAPIBrowser />
    },
    {
        id: 1,
        name: "Worker Shutdown",
        displayName: "Worker Shutdown",
        component: <WorkerShutdown />
    }
]

const Flower = () => {
    const [selected, setSelected] = useState(-1)
    const selectedService = flowerServices.find(el => el.id === selected)

    const handleChange = (e: { target: { value: string; }; }) => {
        setSelected(parseInt(e.target.value))
    }

    const TaskPicker = () => <select className={styles.selectDropdown} onChange={handleChange} value={selected}>
        {flowerServices.map((el, i) => <option className={styles.selectOption} key={i} value={el.id}>{el.name}</option>)}
    </select>

    if (selectedService === undefined) return(<><TaskPicker /><hr /></>)
    return(<>
        <TaskPicker />
        <hr />
        <h3>{selectedService.displayName}</h3>
        <hr />
        {selectedService.component}
    </>)
}

export default Flower