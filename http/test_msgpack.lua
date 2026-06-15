local f = io.open("payload.msgpack", "rb")
local payload = f:read("*all")
f:close()

wrk.method = "POST"
wrk.body   = payload
wrk.headers["Content-Type"] = "application/msgpack"