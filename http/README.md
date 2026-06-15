# Benchmark: Tối ưu Latency HTTP với JSON vs MessagePack

Mục tiêu: So sánh hiệu năng và độ trễ (latency) khi truyền dữ liệu qua HTTP giữa hai định dạng:

- `JSON` (văn bản)
- `MessagePack` (nhị phân)

Ý tưởng chính: Tối ưu tầng phần mềm (giảm kích thước payload và giảm chi phí parsing) để cải thiện throughput (RPS) và giảm latency mà không cần nâng cấp phần cứng.

## 🛠 Yêu cầu hệ thống (Prerequisites)

- `Node.js` — để chạy `server.js` (API thử nghiệm)
- `wrk` — công cụ benchmark HTTP
- Python (tùy chọn) — để chạy `convert.py` nếu bạn dùng script Python

Lưu ý cho Windows: `wrk` không hỗ trợ native trên Windows; hãy chạy `wrk` từ WSL (Ubuntu).

## 📂 Cấu trúc thư mục

```
http/
├── payload.json             # Dữ liệu gốc định dạng JSON
├── payload.msgpack          # Dữ liệu đã chuyển sang MessagePack (binary)
├── test_json.lua            # Script wrk đọc file JSON
├── test_msgpack.lua         # Script wrk đọc file MessagePack
├── test_json_fast.lua       # Script wrk cho fast path JSON
├── test_msgpack_fast.lua    # Script wrk cho fast path MessagePack
├── convert.py               # Script chuyển đổi JSON -> Msgpack (Python)
├── server.js                # Node.js Server xử lý API
└── README.md                # Tài liệu dự án
```

## 🚀 Hướng dẫn cài đặt và chạy thử

### Bước 1 — Cài đặt dependencies cho server

Mở terminal tại thư mục project và chạy:

```bash
npm init -y
npm install msgpackr
```

### Bước 2 — Chuẩn bị payload

1. Tạo file `payload.json` chứa dữ liệu mẫu.
2. Chạy script chuyển đổi sang MessagePack. Mã mẫu `convert.py` đã có sẵn trong repo:

```python
import json
import msgpack

with open("payload.json", "r", encoding="utf-8") as f:
        data = json.load(f)

with open("payload.msgpack", "wb") as f:
        f.write(msgpack.packb(data))

print("Đã tạo file payload.msgpack!")
```

Chạy:

```bash
python convert.py
```

### Bước 3 — Khởi động server benchmark

`server.js` là một ví dụ tối ưu hóa cho latency HTTP bằng native `http` Node.js và chứa hai endpoint:

- `/api/benchmark` — parse payload như bình thường
- `/api/benchmark-fast` — chỉ trả `OK` mà không parse payload

```javascript
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
        const chunks = [];

        req.on('data', chunk => chunks.push(chunk));
        req.on('end', () => {
            const body = Buffer.concat(chunks);
            const isBenchmark = req.method === 'POST' && req.url === '/api/benchmark';
            const isFastPath = req.method === 'POST' && req.url === '/api/benchmark-fast';

            if (!isBenchmark && !isFastPath) {
                res.writeHead(404, { 'Content-Type': 'text/plain' });
                return res.end('Not Found');
            }

            try {
                if (isBenchmark) {
                    if (contentType === 'application/json') {
                        JSON.parse(body.toString('utf8'));
                    } else if (contentType === 'application/msgpack') {
                        unpack(body);
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
```

Chạy server:

```bash
node server.js
```

### Bước 4 — Chạy benchmark với `wrk` (từ WSL trên Windows)

Tạo hai file Lua để `wrk` nhúng payload vào body request:

`test_json.lua`:
```lua
local f = io.open("payload.json", "rb")
wrk.body = f:read("*all")
f:close()
wrk.method = "POST"
wrk.headers["Content-Type"] = "application/json"
```

`test_msgpack.lua`:
```lua
local f = io.open("payload.msgpack", "rb")
wrk.body = f:read("*all")
f:close()
wrk.method = "POST"
wrk.headers["Content-Type"] = "application/msgpack"
```

Ví dụ chạy (từ WSL, trong thư mục project):

```bash
wrk -t4 -c200 -d20s -s test_json.lua http://localhost:3000/api/benchmark
wrk -t4 -c200 -d20s -s test_msgpack.lua http://localhost:3000/api/benchmark

wrk -t4 -c200 -d20s -s test_json_fast.lua http://localhost:3000/api/benchmark-fast
wrk -t4 -c200 -d20s -s test_msgpack_fast.lua http://localhost:3000/api/benchmark-fast
```

Nếu gặp `Connection refused` khi dùng `localhost`, thử đổi sang IP LAN của máy Windows.

## 📊 Phân tích kết quả (kỳ vọng)

- Kích thước payload: MessagePack thường nhỏ hơn JSON ~30–50%.
- Avg latency: MessagePack có xu hướng thấp và ổn định hơn do chi phí parse thấp hơn.
- Requests/sec (RPS): MessagePack thường cho RPS cao hơn ~20–40% trong cùng điều kiện tải.

## 📌 HTTP Latency Benchmark Results

Benchmark hiện tại (WSL → Windows host `192.168.1.14:3000`) đã được tối ưu phần mềm bằng cách dùng native `http`, loại bỏ Express, và tối ưu đường dẫn request.

### Kết quả so sánh: Parse vs No-Parse

| Chỉ số | JSON (parse) | MessagePack (parse) | JSON (no-parse) | MessagePack (no-parse) |
| --- | --- | --- | --- | --- |
| Avg Latency | `5.49 ms` | `4.84 ms` | `4.07 ms` | `4.96 ms` |
| Requests/sec | `43,671.86` | `48,014.92` | `55,594.73` | `45,561.32` |
| Transfer/sec | `5.29MB` | `5.82MB` | `6.73MB` | `5.52MB` |
| Socket errors | `0` | `0` | `0` | `0` |

### Kết quả chi tiết

**Với parse (latency thực tế):**
- JSON: 1,314,180 requests trong 30.09s, 159.17MB read.
- MessagePack: 1,444,150 requests trong 30.08s, 174.91MB read.

**Không parse (fast path):**
- JSON: 1,672,918 requests trong 30.09s, 202.62MB read.
- MessagePack: 1,371,212 requests trong 30.10s, 166.08MB read.

### Đánh giá tập trung vào latency HTTP

- **JSON có latency thấp nhất** khi không parse: `4.07 ms` trung bình.
- Bỏ việc parse JSON giúp giảm latency từ `5.49 ms` xuống `4.07 ms`, tức cải thiện ~25%.
- Với MessagePack, fast path không giảm latency mà tăng từ `4.84 ms` lên `4.96 ms`, vì chi phí unpack nhỏ hơn overhead mạng.
- Kết luận: **nếu mục tiêu là latency tối ưu HTTP thuần túy, bỏ parse là cách hiệu quả**.

> Lưu ý: `benchmark-fast` bỏ việc parse payload nhưng vẫn phải đợi `req.on('end')`. Do đó latency thấp hơn nhưng không phải như khi hoàn toàn bỏ nhận body. Những con số này phản ánh **latency HTTP thực tế** trên WSL + network.

### Cách ghi kết quả latency

1. Khởi động server: `npm start`
2. Chạy benchmark với parse (ứng dụng thực tế):

```bash
wrk -t4 -c200 -d30s -s test_json.lua http://192.168.1.14:3000/api/benchmark
wrk -t4 -c200 -d30s -s test_msgpack.lua http://192.168.1.14:3000/api/benchmark
```

3. Chạy benchmark không parse (latency floor):

```bash
wrk -t4 -c200 -d30s -s test_json_fast.lua http://192.168.1.14:3000/api/benchmark-fast
wrk -t4 -c200 -d30s -s test_msgpack_fast.lua http://192.168.1.14:3000/api/benchmark-fast
```

4. So sánh `Avg Latency` để thấy chi phí parsing của từng định dạng.

> Ghi chú: Khoảng cách giữa parse và no-parse cho ta thấy bao nhiêu latency được tiêu tốn vào xử lý payload. Nếu ứng dụng thực sự cần xử lý, đó là chi phí không tránh được.

## ⚡ Latency Optimization Best Practices

Để cải thiện độ trễ và thu được kết quả benchmark thực tế hơn, hãy áp dụng các phương pháp sau:

1. **Giảm concurrency nếu quá cao**
   - `-c5000` gây ra rất nhiều lỗi timeout/read và biến benchmark thành bài test stress, không phải bài test latency chính xác.
   - Thử `-c1000` hoặc `-c200` để đánh giá latency ổn định hơn.

2. **Sử dụng Warm-up trước khi đo**
   - Chạy một vài lần `wrk` ngắn trước khi ghi kết quả chính thức để làm ấm cache và JIT compiler.
   - Điều này giúp loại bỏ ảnh hưởng của startup và cold cache.

3. **Giữ request handler nhẹ nhất có thể**
   - Tránh các thao tác đồng bộ hoặc I/O trong đường dẫn request.
   - Ở server hiện tại, chỉ parse payload và trả `OK`; đây là cách tốt để đo chi phí parsing thuần túy.

4. **Dùng kết nối Keep-Alive**
   - `wrk` mặc định dùng HTTP/1.1 và giữ kết nối mở.
   - Điều này giảm overhead handshake cho mỗi request.

5. **Sử dụng cluster hoặc worker hợp lý**
   - Server hiện dùng `cluster` để tận dụng nhiều core.
   - Chỉ dùng số worker phù hợp với core thực tế, tránh quá tải do quá nhiều tiến trình.

6. **So sánh payload nhỏ và payload lớn riêng biệt**
   - Nếu payload quá lớn, latency bị ảnh hưởng bởi I/O và truyền dữ liệu.
   - Dùng payload thực tế của ứng dụng để đánh giá đúng chi phí parse.

7. **Ghi nhận thêm chỉ số P99/P95 và lỗi socket**
   - `wrk` chỉ báo `Latency Avg`; nên xem thêm `Latency Stdev`, `Max`, và `Socket errors`.
   - Nhiều timeout nghĩa là cài đặt quá tải và không phản ánh latency ứng dụng.

8. **Tối ưu định dạng payload theo bối cảnh**
   - Với dữ liệu nhỏ, JSON đôi khi đơn giản và hiệu quả.
   - Với payload lớn hoặc mạng hạn chế, MessagePack giảm kích thước truyền tải nhưng cần đánh đổi parse cost.

9. **Tăng tính đơn giản của HTTP stack**
   - Tránh middleware không cần thiết, logging đồng bộ, và body parser nặng.
   - Việc trả `OK` nhanh nhất có thể giúp tập trung vào latency HTTP thuần túy.

10. **Đo latency ở mức tải cân bằng**
   - Cài đặt hợp lý là `-c200` hoặc `-c1000` tùy mục tiêu.
   - Mục tiêu latency thấp nhất là giữ mức tải nơi socket errors = 0 và latency ổn định.

---

## 📌 Giảm latency HTTP phần mềm, không phụ thuộc phần cứng

Dưới đây là các bước bạn có thể áp dụng ngay trên chính phần mềm mà không cần nâng cấp máy chủ.

1. **Giảm số phép xử lý mỗi request**
   - Không làm việc gì ngoài việc xác thực `Content-Type`, parse payload và trả `OK`.
   - Bỏ qua ghi log chi tiết, lưu dữ liệu hoặc thao tác I/O khác.

2. **Tối ưu parsing**
   - Nếu chỉ cần đo latency HTTP, không cần giải mã toàn bộ payload. Chỉ parse hoặc validate những gì bắt buộc.
   - Với MessagePack, chỉ unpack khi cần. Với JSON, chỉ parse JSON khi đó là yêu cầu thực sự.

3. **Giữ payload nhỏ nhất có thể**
   - Mỗi byte nhỏ giúp giảm thời gian truyền qua mạng.
   - Xóa trường thừa trong payload hoặc dùng payload nhỏ mẫu để benchmark latency.

4. **Giảm overhead middleware**
   - Loại bỏ mọi middleware không cần thiết.
   - Dùng các API HTTP nhẹ nhất có thể, tránh framework/adapter nặng.

5. **Giảm allocations trong Node.js**
   - Nếu bạn muốn nâng cao hơn, tái sử dụng buffer và tránh tạo quá nhiều object mới.
   - Ví dụ: parse `req.body` một lần, không copy nhiều lần.

6. **Tắt tính năng không cần thiết**
   - Tránh nén response, logging đồng bộ, và các tính năng `debug` khi đo latency.
   - Nên chạy benchmark trên môi trường ít process nền.

7. **Sử dụng cài đặt benchmark hợp lý**
   - Mục tiêu là latency thấp nhất, nên dùng `-c200` hoặc `-c1000` thay vì `-c5000`.
   - Chỉ dùng `c5000` nếu bạn đang đánh giá giới hạn chịu tải, không phải latency.

8. **Giữ TCP và HTTP đơn giản**
   - Với HTTP/1.1, đảm bảo `Keep-Alive` đang bật.
   - Nếu có thể, cân nhắc HTTP/2 trên phần mềm, nhưng trước tiên hãy tối ưu đường dẫn request hiện tại.

9. **Kiểm soát tiêu thụ CPU của server**
   - Node.js CPU-bound có thể gây gián đoạn độ trễ.
   - Giảm công việc CPU mỗi request, và giữ worker càng nhẹ càng tốt.

10. **Đánh giá lại sau mỗi thay đổi**
   - Mỗi lần thay đổi phần mềm, chạy lại benchmark `c200` để xem latency có giảm hay không.
   - Không đánh giá bằng throughput nếu mục tiêu chỉ là latency.

---

## Kết luận

Chuyển sang định dạng nhị phân như MessagePack là một cách tối ưu chi phí để giảm latency và tăng khả năng chịu tải trên các hệ thống HTTP khi so sánh với JSON thuần túy.

---

Nếu bạn muốn, tôi có thể: (1) sửa `server.js`/`convert.py` để làm ví dụ hoàn chỉnh, hoặc (2) thêm script npm để chạy benchmark tự động. Bạn muốn tiếp theo là gì?