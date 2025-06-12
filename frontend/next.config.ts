import type { NextConfig } from 'next';


const targetGrafana = process.env.NODE_ENV === 'production' ? 'backend' : process.env.REACT_APP_DOCKER_GRAFANA_HOST || 'localhost';
const portGrafana = process.env.NODE_ENV === 'production' ? '3000' : process.env.REACT_APP_DOCKER_GRAFANA_PORT || '3000';

const nextConfig: NextConfig = {
  /* config options here */
  output: 'standalone',
  crossOrigin: 'anonymous',

  async rewrites() {
    return [
      {
        source: "/grafana/:path*", 
        destination:`http://${targetGrafana}:${portGrafana}/:path*`,
      },
    ];
  },
  
};

export default nextConfig;
