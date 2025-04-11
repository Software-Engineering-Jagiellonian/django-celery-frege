import type { NextConfig } from 'next';

const nextConfig: NextConfig = {
  /* config options here */
  output: 'standalone',
  crossOrigin: 'anonymous',

  async rewrites() {
    return [
      {
        source: "/grafana/:path*", 
        destination: "http://localhost:3000/:path*", 
      },
    ];
  },
  


};

export default nextConfig;
