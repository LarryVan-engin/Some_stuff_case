local f = io.open("payload.json", "rb")
local payload = f:read("*all")
f:close()

wrk.method = "POST"
wrk.body = payload
wrk.headers["Content-Type"] = "application/json"
wrk.path = "/api/benchmark-fast"
