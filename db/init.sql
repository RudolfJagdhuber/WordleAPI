CREATE TABLE games (
    `id` BINARY(16) PRIMARY KEY,
    `player` BINARY(16),
    `word` VARCHAR(16),
    `tries` SMALLINT,
    `guesses` JSON,
    `created` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    `solved` INT DEFAULT 0
);