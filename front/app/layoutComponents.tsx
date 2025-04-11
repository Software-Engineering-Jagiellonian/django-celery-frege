'use client';

import { Navbar } from '@/src/components/navbar/Navbar';
import { SideMenu } from '@/src/components/sideMenu/SideMenu';
import { useState, useEffect } from 'react';
import styles from '../src//App.module.scss';

export default function NavigationBar({ children }) {
  const [isMenuCollapsed, setIsMenuCollapsed] = useState(false);
  useEffect(() => {
    document.title = 'Frege';
  }, []);
  //   return <Navbar onMenuClick={() => setIsMenuCollapsed(!isMenuCollapsed)} />;
  return (
    <div className={styles.App}>
      <Navbar onMenuClick={() => setIsMenuCollapsed(!isMenuCollapsed)} />
      <div className={styles.ContentNav}>
        <SideMenu className={isMenuCollapsed ? styles.hidden : undefined} />
        <div className={styles.mainContent}>{children}</div>
      </div>
    </div>
  );
}
