'use client';

import { Navbar } from '@/src/components/navbar/Navbar';
import { SideMenu } from '@/src/components/sideMenu/SideMenu';
import { useState, useEffect, ReactNode } from 'react';
import styles from '../src/App.module.scss';

interface NavigationBarProps {
  children: ReactNode;
}

export default function NavigationBar({ children }: NavigationBarProps) {
  const [isMenuCollapsed, setIsMenuCollapsed] = useState(false);
  useEffect(() => {
    document.title = 'Frege';
  }, []);
  return (
    <div className={styles.App}>
      <Navbar onMenuClick={() => setIsMenuCollapsed(!isMenuCollapsed)} />
      <div className={styles.ContentNav}>
        <SideMenu className={isMenuCollapsed ? styles.hidden : styles.visible} />
        <div className={styles.mainContent}>{children}</div>
      </div>
    </div>
  );
}
