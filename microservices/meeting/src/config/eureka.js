// src/config/eureka.js – registers the meeting service in Eureka as MEETING
const { Eureka } = require('eureka-js-client');

function createEurekaClient(port) {
    const host = process.env.EUREKA_INSTANCE_HOST || 'localhost';
    const ip = process.env.EUREKA_INSTANCE_IP || '127.0.0.1';
    const baseUrl = `http://${host}:${port}`;

    return new Eureka({
        instance: {
            app: 'MEETING',                          // name shown in the dashboard
            instanceId: `${host}:meeting:${port}`,   // unique per port -> several instances possible
            hostName: host,
            ipAddr: ip,
            port: { $: port, '@enabled': 'true' },
            vipAddress: 'meeting',
            homePageUrl: `${baseUrl}/swagger-ui`,
            statusPageUrl: `${baseUrl}/api/meetings/hello`,
            healthCheckUrl: `${baseUrl}/api/meetings/hello`,
            dataCenterInfo: {
                '@class': 'com.netflix.appinfo.InstanceInfo$DefaultDataCenterInfo',
                name: 'MyOwn',
            },
        },
        eureka: {
            host: process.env.EUREKA_HOST || 'localhost',
            port: Number(process.env.EUREKA_PORT) || 8761,
            servicePath: '/eureka/apps/',   // Spring Eureka path (the library default is /eureka/v2/apps/)
            maxRetries: 10,
            requestRetryDelay: 2000,
        },
    });
}

module.exports = { createEurekaClient };
