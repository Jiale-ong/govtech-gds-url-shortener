CREATE DATABASE IF NOT EXISTS `govtech_url` ;
USE `govtech_url`;

DROP TABLE IF EXISTS `govtech_url`;
CREATE TABLE IF NOT EXISTS `govtech_url` (
    `id` int(20) NOT NULL AUTO_INCREMENT,
    `short_url` varchar(150) NOT NULL,
    `original_url` varchar(500) NOT NULL,
    `creator` varchar(150) NOT NULL,
    `click_count` int(20) NOT NULL default 0,
    PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1;
