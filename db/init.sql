CREATE TABLE users (
    `id` BINARY(16) PRIMARY KEY,
    `name` VARCHAR(255) UNIQUE,
    `password_hash` BINARY(32),
    `creation_date` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    `password_changed` BOOLEAN DEFAULT 0
);

CREATE TABLE games (
    `id` BINARY(16) PRIMARY KEY,
    `player` BINARY(16),
    `word` VARCHAR(16),
    `tries` SMALLINT,
    `guesses` JSON,
    `created` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    `solved` INT DEFAULT 0
);