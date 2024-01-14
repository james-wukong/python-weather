/*
 Navicat MySQL Data Transfer

 Source Server         : MySQL-4002-docker-ver8.0
 Source Server Type    : MySQL
 Source Server Version : 80200 (8.2.0)
 Source Host           : localhost:3306
 Source Schema         : weather_api

 Target Server Type    : MySQL
 Target Server Version : 80200 (8.2.0)
 File Encoding         : 65001

 Date: 13/01/2024 22:17:59
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

CREATE DATABASE IF NOT EXISTS `weather_api`;
USE `weather_api`;

-- ----------------------------
-- Table structure for locations
-- ----------------------------
DROP TABLE IF EXISTS `locations`;
CREATE TABLE `locations` (
  `id` bigint unsigned NOT NULL AUTO_INCREMENT,
  `longitude` decimal(10,7) DEFAULT NULL,
  `latitude` decimal(10,7) DEFAULT NULL,
  `resolved_addr` varchar(100) DEFAULT NULL,
  `address` varchar(100) DEFAULT NULL,
  `timezone` varchar(100) DEFAULT NULL,
  `description` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `unq_longitude_latitude` (`longitude`,`latitude`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- ----------------------------
-- Table structure for stations
-- ----------------------------
DROP TABLE IF EXISTS `stations`;
CREATE TABLE `stations` (
  `id` smallint unsigned NOT NULL AUTO_INCREMENT,
  `name_abbr` varchar(10) NOT NULL,
  `name` varchar(100) NOT NULL,
  `distance` int unsigned NOT NULL,
  `latitude` decimal(10,7) NOT NULL,
  `longitude` decimal(10,7) NOT NULL,
  `use_count` int unsigned DEFAULT '0',
  `quality` int unsigned DEFAULT '0',
  `contribution` int unsigned DEFAULT '0',
  PRIMARY KEY (`id`),
  UNIQUE KEY `unq_name` (`name_abbr`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- ----------------------------
-- Table structure for weather_details
-- ----------------------------
DROP TABLE IF EXISTS `weather_details`;
CREATE TABLE `weather_details` (
  `id` bigint unsigned NOT NULL AUTO_INCREMENT,
  `location_id` bigint unsigned NOT NULL,
  `date` date NOT NULL,
  `datetime_epoch` int NOT NULL,
  `datetime` datetime DEFAULT NULL,
  `type` smallint DEFAULT '0' COMMENT '0 means day, 1 means hour',
  `tempmax` decimal(7,2) DEFAULT '0.00',
  `tempmin` decimal(7,2) DEFAULT '0.00',
  `temp` decimal(7,2) DEFAULT '0.00',
  `feelslikemax` decimal(7,2) DEFAULT '0.00',
  `feelslikemin` decimal(7,2) DEFAULT '0.00',
  `feelslike` decimal(7,2) DEFAULT '0.00',
  `dew` decimal(7,2) DEFAULT '0.00',
  `humidity` decimal(7,2) DEFAULT '0.00',
  `precip` decimal(10,5) DEFAULT '0.00000',
  `precipprob` int unsigned DEFAULT '0',
  `precipcover` decimal(7,2) DEFAULT '0.00',
  `preciptype` varchar(100) DEFAULT '',
  `snow` int unsigned DEFAULT '0',
  `snowdepth` decimal(7,2) DEFAULT '0.00',
  `windgust` decimal(7,2) DEFAULT '0.00',
  `windspeed` decimal(7,2) DEFAULT '0.00',
  `winddir` decimal(7,2) DEFAULT '0.00',
  `pressure` decimal(7,2) DEFAULT '0.00',
  `cloudcover` decimal(7,2) DEFAULT '0.00',
  `visibility` int unsigned DEFAULT '0',
  `solarradiation` decimal(7,2) DEFAULT '0.00',
  `solarenergy` decimal(7,2) DEFAULT '0.00',
  `uvindex` int unsigned DEFAULT '0',
  `severerisk` int unsigned DEFAULT '0',
  `sunrise` datetime DEFAULT NULL,
  `sunrise_epoch` int DEFAULT NULL,
  `sunset` datetime DEFAULT NULL,
  `sunset_epoch` int DEFAULT NULL,
  `moonphase` decimal(7,2) DEFAULT '0.00',
  `conditions` varchar(200) DEFAULT '',
  `description` varchar(255) DEFAULT '',
  `icon` varchar(50) DEFAULT '',
  `stations` varchar(100) DEFAULT '',
  `source` varchar(20) DEFAULT '',
  PRIMARY KEY (`id`),
  UNIQUE KEY `unq_date_datetime_type` (`location_id`, `date`,`datetime`,`type`) USING BTREE,
  KEY `location_id` (`location_id`),
  CONSTRAINT `weather_details_ibfk_1` FOREIGN KEY (`location_id`) REFERENCES `locations` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

SET FOREIGN_KEY_CHECKS = 1;
