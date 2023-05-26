import React, { useState, useEffect } from 'react';
import styles from './Django.module.scss';
import Sublist, { handleDataTypes as handleSubListDataTypes } from './Sublist';

export const handleDataTypes = (property: string, obj: any, setData: any) => {
    switch(typeof obj){
        case "undefined":
            return <><div>{property}</div><div>unknown</div></>
        case "boolean":
            return <><div>{property}</div><div>{obj.toString()}</div></>
        case "number":
            return <><div>{property}</div><div>{obj.toString()}</div></>
        case "bigint":
            return <><div>{property}</div><div>{obj.toString()}</div></>
        case "string":
            if (obj.startsWith("http"))
                return <><div>{property}</div><div onClick={() => setData({request: obj, data: {}})} className={styles.subLink}>{obj}</div></>
            return <><div>{property}</div><div>{obj}</div></>
        case "object":
            return <>
            <div>{property}:</div>
            <div />
            <ul className={styles.subObject}>{Object.entries(obj).map(([key, value]: [key: string, value: any]) => <SubObject key={key} property={key} obj={value} setData={setData} />)}</ul>
            <div />
            </>
        default:
            return <li>{property}: unknown object</li>
    }
}

const SubObject: React.FC <{property: string, obj: any, setData: any}> = ({property, obj, setData}) => {
    if (obj === null) return(<><div>{property}</div><div>null</div></>)
    if (Array.isArray(obj)) return(<ul>{obj.map((el: any, i: number) => <React.Fragment key={i}>{handleSubListDataTypes(property, el, setData)}</React.Fragment>)}</ul>)
    return(<>{handleDataTypes(property, obj, setData)}</>)
}

export default SubObject