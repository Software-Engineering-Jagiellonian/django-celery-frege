import React, { useState } from 'react';
import styles from '../Flower.module.scss';
import { Arrow90degDown, Arrow90degUp } from 'react-bootstrap-icons';

export const handleDataTypes = (property: string, obj: any) => {
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
            <span className={styles.subLink}>
              <a href={obj}>{obj}</a>
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
          <li>{property}</li>
          <div className={styles.subObject}>
            {Object.entries(obj).map(([key, value]: [key: string, value: any]) => (
              <Sublist key={key} property={key} obj={value} />
            ))}
          </div>
        </>
      );
    default:
      return <li>{property}: unknown object</li>;
  }
};

const Sublist: React.FC<{ property: string; obj: any }> = ({ property, obj }) => {
  const [show, setShow] = useState(false);

  const ToggleButton = () => (
    <span onClick={() => setShow(!show)}>{show ? <Arrow90degUp /> : <Arrow90degDown />}</span>
  );

  if (obj === null) return <li>{property}: null</li>;

  if (Array.isArray(obj) && obj.length === 0) return <li>{property}: []</li>;

  if (typeof obj === 'object')
    return (
      <>
        <li>
          <ToggleButton />
          {property}
        </li>
        <div className={styles.subObject}>
          {show &&
            Object.entries(obj).map(([key, value]: [key: string, value: any]) => (
              <Sublist key={key} property={key} obj={value} />
            ))}
        </div>
      </>
    );

  if (Array.isArray(obj))
    return (
      <>
        <li>
          <ToggleButton />
          {property}
        </li>
        <div className={styles.subObject}>
          {show &&
            obj.map((el: any, i: number) => (
              <React.Fragment key={i}>{handleDataTypes(i.toString(), el)}</React.Fragment>
            ))}
        </div>
      </>
    );
  return <>{handleDataTypes(property, obj)}</>;
};

export default Sublist;
