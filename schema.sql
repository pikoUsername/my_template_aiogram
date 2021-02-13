CREATE TABLE users(
    id SERIAL PRIMARY KEY,
    user_id BIGINT,
    name VARCHAR(63),
    is_admin BOOLEAN,
    conversation BOOLEAN);

CREATE TABLE chats(
    id SERIAL PRIMARY KEY,
    chat_id BIGINT,
    title VARCHAR(255),
    type VARCHAR(20));
