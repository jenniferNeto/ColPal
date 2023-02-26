CREATE DATABASE stable_db;

USE stable_db;

CREATE TABLE users (
    user_id INT PRIMARY KEY,
    username VARCHAR(50),
    password VARCHAR(50),
    user_role VARCHAR(20)
);

CREATE TABLE pipelines (
    pipeline_id INT PRIMARY KEY,
    pipeline_name VARCHAR(50),
    created_by INT,
    created_date DATETIME,
    modified_by INT,
    modified_date DATETIME,
    approved_by INT,
    approved_date DATETIME,
    is_approved BOOLEAN DEFAULT false,
    is_active BOOLEAN DEFAULT true
);

CREATE TABLE pipeline_files (
    file_id INT PRIMARY KEY,
    file_name VARCHAR(50),
    file_type VARCHAR(50),
    file_path VARCHAR(255),
    pipeline_id INT,
    created_by INT,
    created_date DATETIME,
    modified_by INT,
    modified_date DATETIME,
    approved_by INT,
    approved_date DATETIME,
    is_approved BOOLEAN DEFAULT false,
    is_active BOOLEAN DEFAULT true
);

-- Sample data for users table
INSERT INTO users (user_id, username, password, user_role) VALUES
    (1, 'admin', 'admin', 'admin'),
    (2, 'approver', 'password', 'approver'),
    (3, 'uploader', 'password', 'uploader');
    
