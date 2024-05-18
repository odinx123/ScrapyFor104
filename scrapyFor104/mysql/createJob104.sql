CREATE DATABASE `job104`;

USE `job104`

CREATE TABLE `job`(
    `name` varchar(50),
    `company` varchar(20),
    `salary` varchar(20),
    `job_category` varchar(20),
    `update_time` DATE,
    `exp` varchar(10),
    `address` varchar(20),
    `edu` varchar(10),
    PRIMARY KEY(`name`, `company`)
);