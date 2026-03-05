-- PostgreSQL Schema for Logs Classification App
-- Tables: users, rawdata, labels, dataset

-- Create users table
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create rawdata table
CREATE TABLE IF NOT EXISTS rawdata (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    log_text TEXT NOT NULL,
    source VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create labels table
CREATE TABLE IF NOT EXISTS labels (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) UNIQUE NOT NULL,
    description TEXT,
    color VARCHAR(7) DEFAULT '#007bff',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create dataset table
CREATE TABLE IF NOT EXISTS dataset (
    id SERIAL PRIMARY KEY,
    rawdata_id INTEGER REFERENCES rawdata(id) ON DELETE CASCADE,
    label_id INTEGER REFERENCES labels(id) ON DELETE CASCADE,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(rawdata_id, label_id) -- Prevent duplicate rawdata-label pairs
);

-- Create indexes for better query performance
CREATE INDEX IF NOT EXISTS idx_rawdata_user_id ON rawdata(user_id);
CREATE INDEX IF NOT EXISTS idx_dataset_rawdata_id ON dataset(rawdata_id);
CREATE INDEX IF NOT EXISTS idx_dataset_label_id ON dataset(label_id);
CREATE INDEX IF NOT EXISTS idx_dataset_user_id ON dataset(user_id);

-- Create a view for easier dataset access
CREATE OR REPLACE VIEW dataset_view AS
SELECT 
    d.id,
    d.created_at,
    d.updated_at,
    r.id as rawdata_id,
    r.log_text,
    r.source,
    r.created_at as rawdata_created_at,
    l.id as label_id,
    l.name as label_name,
    l.description as label_description,
    l.color as label_color,
    u.id as user_id,
    u.username,
    u.email
FROM dataset d
JOIN rawdata r ON d.rawdata_id = r.id
JOIN labels l ON d.label_id = l.id
JOIN users u ON d.user_id = u.id;