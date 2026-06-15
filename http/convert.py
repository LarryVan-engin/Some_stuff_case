import json
import msgpack

# 1. Đọc file JSON của bạn
with open("payload.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# 2. Chuyển đổi và ghi ra file nhị phân msgpack
with open("payload.msgpack", "wb") as f:
    f.write(msgpack.packb(data))

print("Đã tạo xong file payload.msgpack thành công!")