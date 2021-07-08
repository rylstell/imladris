
DROP DATABASE IF EXISTS imladrisdb;
CREATE DATABASE IF NOT EXISTS imladrisdb;


USE imladrisdb;


CREATE TABLE Crypto (
    crypto_id INT NOT NULL AUTO_INCREMENT,
    cmc_id INT,
    nomics_id VARCHAR(20),
    name VARCHAR(100),
    symbol VARCHAR(100),
    category VARCHAR(50),
    description VARCHAR(1200),
    slug VARCHAR(100),
    logo VARCHAR(100),
    subreddit VARCHAR(100),
    website VARCHAR(200),
    platform_id INT,
    twitter_username VARCHAR(100),
    twitter_following BOOLEAN DEFAULT 0,
    source VARCHAR(20),
    date_added DATETIME,
    test_crypto BOOLEAN DEFAULT 0,
    PRIMARY KEY (crypto_id)
);


CREATE TABLE Interval_1hr (
    interval_id INT NOT NULL AUTO_INCREMENT,
    crypto_id INT NOT NULL,
    price DOUBLE,
    volume DOUBLE,
    circulating_supply BIGINT,
    twitter_followers INT,
    e3434 DOUBLE,
    interval_count INT,
    timestamp DATETIME NOT NULL,
    PRIMARY KEY (interval_id),
    FOREIGN KEY (crypto_id) REFERENCES Crypto(crypto_id)
);


CREATE TABLE IntValue (
    int_value_id VARCHAR(30) NOT NULL,
    value INT,
    PRIMARY KEY (int_value_id)
);


INSERT INTO IntValue (int_value_id, value) VALUES ('interval_count', 0);
