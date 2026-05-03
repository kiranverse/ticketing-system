import redis

redis_client = redis.Redis(host="localhost", port=6380, decode_responses=True)

# Lua script - atomic check + lock in one step
RESERVE_SCRIPT = """
local key = KEYS[1]
local user_id = ARGV[1]
local ttl = ARGV[2]

if redis.call("EXISTS", key) == 1 then
    return 0
end

redis.call("SET", key, user_id, "EX", tonumber(ttl))
return 1
"""

reserve_lua = redis_client.register_script(RESERVE_SCRIPT)