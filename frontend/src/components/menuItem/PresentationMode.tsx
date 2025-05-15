'use client';

import React, { useEffect, useState } from 'react';
import { CaretRight, Easel3 } from 'react-bootstrap-icons';
import styles from './MenuItem.module.scss';
import FullscreenDashboards from '../FullScreenDashboards/FullscreenDashboards';
import { savedFullscreenDashboardId } from '@/app/presentationMode/PresentationMode';
import { createRoot, Root } from 'react-dom/client';
import Link from 'next/link';

const fullscreenElementId = 'fullscreen-view-wrapper';

const PresentationMode = () => {
  const [fullscreenRoot, setFullscreenRoot] = useState<Root | null>(null);

  const handleFullScreenChange = () => {
    if (!document.fullscreenElement && fullscreenRoot !== null) {
      fullscreenRoot.unmount();
      document.getElementById(fullscreenElementId)?.remove();
    }
  };

  const onPlayClick = (e: { stopPropagation: () => void }) => {
    e.stopPropagation();

    const dashboardId = localStorage.getItem(savedFullscreenDashboardId) || '';

    const output = document.createElement('div');
    output.setAttribute('id', fullscreenElementId);
    document.getElementById('root')?.children[0].appendChild(output);
    output.requestFullscreen();

    const root = createRoot(output);
    root.render(<FullscreenDashboards dashboardId={dashboardId} />);
    setFullscreenRoot(root);
  };

  useEffect(() => {
    document.addEventListener('fullscreenchange', handleFullScreenChange);
    return () => document.removeEventListener('fullscreenchange', handleFullScreenChange);
  }, [fullscreenRoot]);

  return (
    <Link href="/presentationMode" className={styles.link}>
      <div className={styles.menuItem}>
        <div className={styles.iconContainer}>
          <Easel3 />
        </div>
        <div className={styles.label}>Presentation Mode</div>
        <button onClick={onPlayClick} type="button" className={styles.expandButton}>
          <CaretRight />
        </button>
      </div>
    </Link>
  );
};

export default PresentationMode;
