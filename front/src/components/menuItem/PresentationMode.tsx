import React, { useEffect, useState } from 'react';
import { CaretRight, Easel3 } from 'react-bootstrap-icons';
// import { useNavigate } from 'react-router-dom';
import styles from './MenuItem.module.scss';
import FullscreenDashboards from '../FullScreenDashboards/FullscreenDashboards';
import { savedFullscreenDashboardId } from '../pages/presentationMode/PresentationMode';
import { createRoot, Root } from 'react-dom/client';

const fullscreenElementId = 'fullscreen-view-wrapper';

const PresentationMode = () => {
  // const navigate = useNavigate();
  const [fullscreenRoot, setFullscreenRoot] = useState<Root | null>(null);

  // const onMenuItemClick = (e: { stopPropagation: () => void }) => {
  //   navigate('/presentation');
  //   e.stopPropagation();
  // };

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
    // <div className={styles.menuItem} onClick={onMenuItemClick}>
    <div className={styles.menuItem}>
      <div className={styles.iconContainer}>
        <Easel3 />
      </div>
      <div className={styles.label}>Presentation Mode</div>
      <button onClick={onPlayClick} type="button" className={styles.expandButton}>
        <CaretRight />
      </button>
    </div>
  );
};

export default PresentationMode;
