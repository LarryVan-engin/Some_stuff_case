const http = require('http');
const os = require('os');
const cluster = require('cluster');
const { unpack } = require('msgpackr');

const numCPUs = os.cpus().length;
const port = 3000;

function printServerSpecs() {
    const totalRAM = (os.totalmem() / 1024 / 1024 / 1024).toFixed(2);
    const freeRAM = (os.freemem() / 1024 / 1024 / 1024).toFixed(2);
    const cpuModel = os.cpus()[0].model;
    
    console.log('\n==================================================');
    console.log(`🚀 PRIMARY PROCESS ĐANG CHẠY (PID: ${process.pid})`);
    console.log('==================================================');
    console.log('💻 THÔNG SỐ PHẦN CỨNG & MÔI TRƯỜNG:');
    console.log(`   - Hệ điều hành : ${os.type()} ${os.release()} (${os.arch()})`);
    console.log(`   - CPU          : ${cpuModel}`);
    console.log(`   - Số luồng CPU : ${numCPUs} Cores`);
    console.log(`   - RAM          : ${totalRAM} GB (Trống: ${freeRAM} GB)`);
    console.log(`   - Node.js Ver  : ${process.version}`);
    console.log('==================================================');
    console.log(`⏳ Khởi tạo ${numCPUs} Workers để chia tải...\n`);
}

if (cluster.isPrimary) {
    printServerSpecs();

    for (let i = 0; i < numCPUs; i++) {
        cluster.fork();
    }

    cluster.on('exit', (worker, code, signal) => {
        console.log(`⚠️ Worker ${worker.process.pid} vừa chết. Đang hồi sinh...`);
        cluster.fork();
    });
} else {
    const server = http.createServer((req, res) => {
        const contentType = (req.headers['content-type'] || '').split(';')[0].trim();
        const isBenchmark = req.method === 'POST' && req.url === '/api/benchmark';
        const isFastPath = req.method === 'POST' && req.url === '/api/benchmark-fast';

        if (!isBenchmark && !isFastPath) {
            res.writeHead(404, { 'Content-Type': 'text/plain' });
            return res.end('Not Found');
        }

        let body = null;
        if (isBenchmark) {
            body = [];
        }

        req.on('data', chunk => {
            if (isBenchmark) {
                body.push(chunk);
            }
        });

        req.on('end', () => {
            try {
                if (isBenchmark) {
                    const data = Buffer.concat(body);
                    if (contentType === 'application/json') {
                        JSON.parse(data.toString('utf8'));
                    } else if (contentType === 'application/msgpack') {
                        unpack(data);
                    }
                }

                res.writeHead(200, {
                    'Content-Type': 'text/plain',
                    'Content-Length': '2',
                    Connection: 'keep-alive'
                });
                res.end('OK');
            } catch (error) {
                res.writeHead(400, { 'Content-Type': 'text/plain' });
                res.end('Error');
            }
        });
    });

    server.keepAliveTimeout = 65000;
    server.headersTimeout = 70000;

    server.listen(port, () => {
        console.log(`✅ Worker đã sẵn sàng (PID: ${process.pid}) - Listening at http://localhost:${port}`);
    });
}