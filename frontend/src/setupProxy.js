const { createProxyMiddleware } = require('http-proxy-middleware');

const targetGrafana = process.env.REACT_APP_DOCKER_GRAFANA_HOST || 'localhost';
const portGrafana = process.env.REACT_APP_DOCKER_GRAFANA_PORT || '3000';

const targetFlower ='localhost';
const portFlower = process.env.DOCKER_FLOWER_PORT || '5555';

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

  app.use(
    '/flower',
    createProxyMiddleware({
      target: `http://${targetFlower}:${portFlower}`,
      changeOrigin: true,
      pathRewrite: { '^/flower': '' },
      onProxyReq: (proxyReq, req, res) => {
        proxyReq.setHeader('Host', 'localhost');
      }
    })
  )
};
