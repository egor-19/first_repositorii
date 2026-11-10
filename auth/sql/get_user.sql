SELECT id, username, password, user_group
FROM users
WHERE username = %s AND password = %s;