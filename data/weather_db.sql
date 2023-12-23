DROP DATABASE IF EXISTS weather_api;
CREATE DATABASE IF NOT EXISTS weather_api;
USE weather_api;

CREATE TABLE stations (
    id          SMALLINT UNSIGNED    AUTO_INCREMENT,
    name        VARCHAR(10)     NOT NULL,
    distance    INT UNSIGNED    NOT NULL,
    latitude    DECIMAL(10, 7)    NOT NULL,
    longitude   DECIMAL(10, 7)    NOT NULL,
    useCount    INT UNSIGNED    DEFAULT 0,
    quality     INT UNSIGNED    DEFAULT 0,
    contribution     INT UNSIGNED    DEFAULT 0,
    PRIMARY KEY (id)
);
ALTER TABLE `weather_api`.`stations` 
ADD UNIQUE INDEX `unq_name`(`name`) USING BTREE;

CREATE TABLE weather (
    id          BIGINT UNSIGNED    AUTO_INCREMENT,
    date        DATE            NOT NULL,
    datetime_epoch timestamp    NOT NULL,
    datetime    DATETIME        ,
    type        SMALLINT        DEFAULT 0 COMMENT "0 means day, 1 means hour",
    tempmax     DECIMAL(7,2)     DEFAULT 0,
    tempmin     DECIMAL(7,2)     DEFAULT 0,
    temp     DECIMAL(7,2)     DEFAULT 0,
    feelslikemax     DECIMAL(7,2)     DEFAULT 0,
    feelslikemin     DECIMAL(7,2)     DEFAULT 0,
    feelslike     DECIMAL(7,2)     DEFAULT 0,
    dew     DECIMAL(7,2)     DEFAULT 0,
    humidity     DECIMAL(7,2)     DEFAULT 0,
    precip     DECIMAL(10,5)     DEFAULT 0,
    precipprob     INT UNSIGNED     DEFAULT 0,
    precipcover     DECIMAL(7,2)     DEFAULT 0,
    preciptype      VARCHAR(100)    DEFAULT '',
    snow     INT UNSIGNED     DEFAULT 0,
    snowdepth     DECIMAL(7,2)     DEFAULT 0,
    windgust     DECIMAL(7,2)     DEFAULT 0,
    windspeed     DECIMAL(7,2)     DEFAULT 0,
    winddir     DECIMAL(7,2)     DEFAULT 0,
    pressure     DECIMAL(7,2)     DEFAULT 0,
    cloudcover     DECIMAL(7,2)     DEFAULT 0,
    visibility     INT UNSIGNED     DEFAULT 0,
    solarradiation     DECIMAL(7,2)     DEFAULT 0,
    solarenergy     DECIMAL(7,2)     DEFAULT 0,
    uvindex     INT UNSIGNED     DEFAULT 0,
    severerisk     INT UNSIGNED     DEFAULT 0,
    sunrise     DATETIME          DEFAULT NULL,
    sunrise_epoch     TIMESTAMP     DEFAULT NULL,
    sunset     DATETIME          DEFAULT NULL,
    sunset_epoch     TIMESTAMP     DEFAULT NULL,
    moonphase     DECIMAL(7,2)     DEFAULT 0,
    conditions     VARCHAR(200)     DEFAULT '',
    description     VARCHAR(255)     DEFAULT '',
    icon        VARCHAR(50)     DEFAULT '',
    stations    VARCHAR(100)    DEFAULT '',
    source      VARCHAR(20)     DEFAULT '',
    PRIMARY KEY (id)
);
ALTER TABLE `weather_api`.`weather` 
ADD UNIQUE INDEX `unq_date_datetime_type`(`date`, `datetime`, `type`) USING BTREE;