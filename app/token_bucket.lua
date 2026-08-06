-- Get data from Redis
local tokens = redis.call("GET", KEYS[1])
local last_time = redis.call("GET", KEYS[2])

-- Get values passed from Python
local bucket_size = tonumber(ARGV[1])
local refill_rate = tonumber(ARGV[2])
local current_time = tonumber(ARGV[3])

-- First request from this user
if not tokens or not last_time then
    tokens = bucket_size
    last_time = current_time
else
    tokens = tonumber(tokens)
    last_time = tonumber(last_time)
end

-- Refill tokens
local elapsed = current_time - last_time
tokens = math.min(bucket_size, tokens + elapsed * refill_rate)

-- No tokens left
if tokens < 1 then
    redis.call("SET", KEYS[1], tokens)
    redis.call("SET", KEYS[2], current_time)
    return 0
end

-- Consume one token
tokens = tokens - 1

-- Save updated values
redis.call("SET", KEYS[1], tokens)
redis.call("SET", KEYS[2], current_time)

return 1