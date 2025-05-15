import type { NextConfig } from 'next';


const targetGrafana = process.env.REACT_APP_DOCKER_GRAFANA_HOST || 'localhost';
const portGrafana = process.env.REACT_APP_DOCKER_GRAFANA_PORT || '3000';

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
