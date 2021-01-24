SELECT blink.capacity.timestamp, blink.address.state, blink.branch.title, blink.capacity.capacity
FROM blink.capacity
JOIN blink.branch ON blink.capacity.branch_id = blink.branch.id
JOIN blink.address on blink.capacity.branch_id = blink.address.id
WHERE status_code = 0
ORDER BY timestamp DESC;