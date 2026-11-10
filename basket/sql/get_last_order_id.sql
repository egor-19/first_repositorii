SELECT MAX(o_id) AS order_id
FROM user_order
WHERE u_id = %s;