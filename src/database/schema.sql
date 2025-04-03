-- Create tables for OKR tracking
CREATE TABLE IF NOT EXISTS practices (
    practice_id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    owner VARCHAR(100) NOT NULL
);

CREATE TABLE IF NOT EXISTS okrs (
    okr_id VARCHAR(10) PRIMARY KEY,
    practice_id INTEGER REFERENCES practices(practice_id),
    name VARCHAR(200) NOT NULL,
    description TEXT,
    year INTEGER,
    owner VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS key_results (
    kr_id VARCHAR(10) PRIMARY KEY,
    okr_id VARCHAR(10) REFERENCES okrs(okr_id),
    name VARCHAR(200) NOT NULL,
    description TEXT,
    benchmark FLOAT,
    target VARCHAR(50),
    current_value FLOAT,
    status VARCHAR(50),
    tracking_frequency VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS actions (
    action_id VARCHAR(10) PRIMARY KEY,
    kr_id VARCHAR(10) REFERENCES key_results(kr_id),
    description TEXT,
    owner VARCHAR(100),
    due_date DATE,
    status VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS metrics (
    metric_id VARCHAR(10) PRIMARY KEY,
    kr_id VARCHAR(10) REFERENCES key_results(kr_id),
    date DATE,
    value FLOAT,
    target FLOAT,
    status VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);