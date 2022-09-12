CREATE DATABASE IF NOT EXISTS `url` ;
USE `url`;

DROP TABLE IF EXISTS `url`;
CREATE TABLE IF NOT EXISTS `url` (
    `id` int(20) NOT NULL AUTO_INCREMENT,
    `short_url` varchar(150) NOT NULL,
    `original_url` varchar(500) NOT NULL,
    `creator` varchar(150) NOT NULL,
    `click_count` int(20) NOT NULL default 0,
    PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1;
