import React, { FC, useState, MouseEvent } from 'react';
import { SideMenuItemDTO } from '../sideMenu/SideMenuStruct';
import { ArrowDownShort, ArrowUpShort } from 'react-bootstrap-icons';
import styles from './MenuItem.module.scss';
import { Link } from 'react-router-dom';

export interface MenuItemProps {
  presentationProps: SideMenuItemDTO;
  isActive: (href: string) => boolean;
  handleClick: (href: string) => void;
}

export const MenuItem: FC<MenuItemProps> = ({ presentationProps, isActive, handleClick }) => {
  const [isExpanded, setIsExpanded] = useState<boolean>(false);

  const onExpandClick = (e: MouseEvent<HTMLElement>) => {
    setIsExpanded(!isExpanded);
    e.stopPropagation();
    e.preventDefault();
  };

  const onNavigate = () => {
    if (presentationProps.href) handleClick(presentationProps.href);
  };

  return (
    <>
      {presentationProps.href ? (
        <Link
          className={`${styles.menuItem} ${
            isActive(presentationProps.href) ? styles.active : styles.inactive
          }`}
          to={presentationProps.href}
          onClick={onNavigate}>
          <div className={styles.iconContainer}>{presentationProps.icon}</div>
          <div className={styles.label}>{presentationProps.label}</div>
          {presentationProps.subNodes && presentationProps.subNodes.length > 0 && (
            <button onClick={onExpandClick} type="button" className={styles.expandButton}>
              {isExpanded ? <ArrowUpShort /> : <ArrowDownShort />}
            </button>
          )}
        </Link>
      ) : (
        <div className={styles.menuItem}>
          <div className={styles.iconContainer}>{presentationProps.icon}</div>
          <div className={styles.label}>{presentationProps.label}</div>
          {presentationProps.subNodes && presentationProps.subNodes.length > 0 && (
            <button onClick={onExpandClick} type="button" className={styles.expandButton}>
              {isExpanded ? <ArrowUpShort /> : <ArrowDownShort />}
            </button>
          )}
        </div>
      )}
      {isExpanded && presentationProps.subNodes && presentationProps.subNodes.length > 0 && (
        <div className={styles.subNodes}>
          {presentationProps.subNodes.map((node, index) => (
            <MenuItem
              key={index}
              presentationProps={node}
              isActive={isActive}
              handleClick={handleClick}
            />
          ))}
        </div>
      )}
    </>
  );
};
