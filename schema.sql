CREATE TABLE users(
    id SERIAL PRIMARY KEY,
    user_id BIGINT,
    first_name VARCHAR(63),
    is_admin BOOLEAN DEFAULT false,
    is_active BOOLEAN DEFAULT false,
    conversation BOOLEAN);

CREATE TABLE chats(
    id SERIAL PRIMARY KEY,
    chat_id BIGINT,
    title VARCHAR(255),
    type VARCHAR(20),
    is_admin_chat BOOLEAN DEFAULT false,
    notify_errors BOOLEAN DEFAULT false,
    user_lang VARCHAR(6) DEFAULT 'ru');
