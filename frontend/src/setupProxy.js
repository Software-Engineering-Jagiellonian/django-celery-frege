const { createProxyMiddleware } = require('http-proxy-middleware');

const targetGrafana = process.env.REACT_APP_DOCKER_GRAFANA_HOST || 'localhost';
const portGrafana = process.env.REACT_APP_DOCKER_GRAFANA_PORT || '3000';

module.exports = function (app) {
  app.use(
    '/grafana',
    createProxyMiddleware({
      target: `http://${targetGrafana}:${portGrafana}`,
      changeOrigin: true,
      pathRewrite: { '^/grafana': '' },
      onProxyReq: (proxyReq, req, res) => {
        proxyReq.setHeader('Host', 'localhost');
      }
    })
  );
};
