// src/server.js – starts HTTP, then registers in Eureka; deregisters on shutdown
const app = require('./app');
const { createEurekaClient } = require('./config/eureka');

const PORT = Number(process.env.PORT) || 8083;
const eurekaClient = process.env.EUREKA_ENABLED === 'false' ? null : createEurekaClient(PORT);

const server = app.listen(PORT, () => {
  console.log(`meeting service on http://localhost:${PORT} (Swagger: /swagger-ui)`);
  if (!eurekaClient) return;
  eurekaClient.start((err) => {
    if (err) console.error('Eureka registration failed:', err.message || err);
    else console.log(`Registered in Eureka as MEETING (localhost:meeting:${PORT})`);
  });
});

// Clean deregistration (Ctrl+C = SIGINT, docker stop = SIGTERM)
let stopping = false;
function shutdown(signal) {
  if (stopping) return;
  stopping = true;
  console.log(`${signal} received, deregistering from Eureka...`);
  const close = () => server.close(() => process.exit(0));
  if (eurekaClient) eurekaClient.stop(close); else close();
  setTimeout(() => process.exit(0), 5000).unref(); // safety net
}
process.on('SIGINT', () => shutdown('SIGINT'));
process.on('SIGTERM', () => shutdown('SIGTERM'));
