import React, { useState, useEffect } from 'react';
import styles from './Django.module.scss';
import SubObject from './SubObject';
import { Arrow90degDown, Arrow90degUp } from 'react-bootstrap-icons';

export const handleDataTypes = (property: string, obj: any, setData: any) => {
  switch (typeof obj) {
    case 'undefined':
      return <li>{property}: unknown</li>;
    case 'boolean':
      return (
        <li>
          {property}: {obj.toString()}
        </li>
      );
    case 'number':
      return (
        <li>
          {property}: {obj.toString()}
        </li>
      );
    case 'bigint':
      return (
        <li>
          {property}: {obj.toString()}
        </li>
      );
    case 'string':
      if (obj.startsWith('http'))
        return (
          <li>
            {property}:{' '}
            <span onClick={() => setData({ request: obj, data: {} })} className={styles.subLink}>
              {obj}
            </span>
          </li>
        );
      return (
        <li>
          {property}: {obj}
        </li>
      );
    case 'object':
      return (
        <>
          <div className={styles.subObject}>
            {Object.entries(obj).map(([key, value]: [key: string, value: any]) => (
              <SubObject key={key} property={key} obj={value} setData={setData} />
            ))}
          </div>
          <hr />
        </>
      );
    default:
      return <li>{property}: unknown object</li>;
  }
};

const Sublist: React.FC<{ property: string; obj: any; setData: any }> = ({
  property,
  obj,
  setData
}) => {
  const [show, setShow] = useState(true);
  const ToggleButton = () => (
    <span onClick={() => setShow(!show)}>{show ? <Arrow90degUp /> : <Arrow90degDown />}</span>
  );

  if (obj === null) return <li>{property}: null</li>;
  if (Array.isArray(obj) && obj.length === 0) return <li>{property}: []</li>;
  if (Array.isArray(obj))
    return (
      <>
        <li>
          <ToggleButton />
          {property}:
        </li>
        <ul>
          {show &&
            obj.map((el: any, i: number) => (
              <React.Fragment key={i}>{handleDataTypes(i.toString(), el, setData)}</React.Fragment>
            ))}
        </ul>
      </>
    );
  return <>{handleDataTypes(property, obj, setData)}</>;
};

export default Sublist;
