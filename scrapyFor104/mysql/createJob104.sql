CREATE DATABASE `job104`;

USE `job104`

CREATE TABLE `job`(
    `job_id` INT AUTO_INCREMENT,
    `job_title` varchar(50),
    `company` varchar(35),
    `salary_min` INT,
    `salary_max` FLOAT,
    `address` varchar(35),
    `industry` varchar(20),
    `update_time` DATE,
    PRIMARY KEY(`job_id`),
    UNIQUE(`job_title`, `company`)
);

CREATE TABLE `Categories`(
    `category_id` INT AUTO_INCREMENT,
    `category_name` varchar(20),
    PRIMARY KEY(`category_id`),
    UNIQUE(`category_name`)
);

CREATE TABLE `Skills`(
    `skill_id` INT AUTO_INCREMENT,
    `name` varchar(20),
    PRIMARY KEY(`skill_id`),
    UNIQUE(`name`)
);

CREATE TABLE `Tools`(
    `tool_id` INT AUTO_INCREMENT,
    `specialty_tool` varchar(20),
    PRIMARY KEY(`tool_id`),
    UNIQUE(`specialty_tool`)
);

CREATE TABLE `Education`(
    `education_id` INT AUTO_INCREMENT,
    `level` varchar(10),
    PRIMARY KEY(`education_id`),
    UNIQUE(`level`)
);

CREATE TABLE `Experience`(
    `experience_id` INT AUTO_INCREMENT,
    `experience` varchar(20),
    PRIMARY KEY(`experience_id`),
    UNIQUE(`experience`)
);

CREATE TABLE `Job_Category`(
    `job_id` INT,
    `category_id` INT,
    FOREIGN KEY(`job_id`) REFERENCES `job`(`job_id`),
    FOREIGN KEY(`category_id`) REFERENCES `Categories`(`category_id`),
    UNIQUE(`job_id`, `category_id`)
);

CREATE TABLE `Job_Skill`(
    `job_id` INT,
    `skill_id` INT,
    FOREIGN KEY(`job_id`) REFERENCES `job`(`job_id`),
    FOREIGN KEY(`skill_id`) REFERENCES `Skills`(`skill_id`),
    UNIQUE(`job_id`, `skill_id`)
);

CREATE TABLE `Job_Tool`(
    `job_id` INT,
    `tool_id` INT,
    FOREIGN KEY(`job_id`) REFERENCES `job`(`job_id`),
    FOREIGN KEY(`tool_id`) REFERENCES `Tools`(`tool_id`),
    UNIQUE(`job_id`, `tool_id`)
);

CREATE TABLE `Job_Education`(
    `job_id` INT,
    `education_id` INT,
    FOREIGN KEY(`job_id`) REFERENCES `job`(`job_id`),
    FOREIGN KEY(`education_id`) REFERENCES `Education`(`education_id`),
    UNIQUE(`job_id`, `education_id`)
);

CREATE TABLE `Job_Experience`(
    `job_id` INT,
    `experience_id` INT,
    FOREIGN KEY(`job_id`) REFERENCES `job`(`job_id`),
    FOREIGN KEY(`experience_id`) REFERENCES `Experience`(`experience_id`),
    UNIQUE(`job_id`, `experience_id`)
);
