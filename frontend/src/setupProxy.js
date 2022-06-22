const { createProxyMiddleware } = require('http-proxy-middleware');

const target = process.env.REACT_APP_DOCKER_GRAFANA_HOST || 'localhost';
const port = process.env.REACT_APP_DOCKER_GRAFANA_PORT || '3000';

module.exports = function (app) {
  app.use(
    '/grafana',
    createProxyMiddleware({
      target: `http://${target}:${port}`,
      changeOrigin: true,
      pathRewrite: { '^/grafana': '' },
      onProxyReq: (proxyReq, req, res) => {
        proxyReq.setHeader('Host', 'localhost');
      }
    })
  );
};
