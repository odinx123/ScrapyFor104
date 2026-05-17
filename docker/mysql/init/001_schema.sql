CREATE DATABASE IF NOT EXISTS `job104` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE DATABASE IF NOT EXISTS `jobdatabase` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

USE `job104`;

CREATE TABLE IF NOT EXISTS `job`(
    `job_id` INT AUTO_INCREMENT,
    `source_job_key` varchar(32),
    `source_url` varchar(255),
    `dedupe_key` char(40),
    `job_title` varchar(50),
    `company` varchar(35),
    `salary_min` INT,
    `salary_max` FLOAT,
    `address` varchar(35),
    `industry` varchar(20),
    `update_time` DATE,
    PRIMARY KEY(`job_id`),
    UNIQUE KEY `uq_job_source_key` (`source_job_key`),
    UNIQUE KEY `uq_job_dedupe_key` (`dedupe_key`),
    UNIQUE(`job_title`, `company`)
);

CREATE TABLE IF NOT EXISTS `Categories`(
    `category_id` INT AUTO_INCREMENT,
    `category_name` varchar(20),
    PRIMARY KEY(`category_id`),
    UNIQUE(`category_name`)
);

CREATE TABLE IF NOT EXISTS `Skills`(
    `skill_id` INT AUTO_INCREMENT,
    `name` varchar(20),
    PRIMARY KEY(`skill_id`),
    UNIQUE(`name`)
);

CREATE TABLE IF NOT EXISTS `Tools`(
    `tool_id` INT AUTO_INCREMENT,
    `specialty_tool` varchar(20),
    PRIMARY KEY(`tool_id`),
    UNIQUE(`specialty_tool`)
);

CREATE TABLE IF NOT EXISTS `Education`(
    `education_id` INT AUTO_INCREMENT,
    `level` varchar(10),
    PRIMARY KEY(`education_id`),
    UNIQUE(`level`)
);

CREATE TABLE IF NOT EXISTS `Experience`(
    `experience_id` INT AUTO_INCREMENT,
    `experience` varchar(20),
    PRIMARY KEY(`experience_id`),
    UNIQUE(`experience`)
);

CREATE TABLE IF NOT EXISTS `Job_Category`(
    `job_id` INT,
    `category_id` INT,
    FOREIGN KEY(`job_id`) REFERENCES `job`(`job_id`) ON DELETE CASCADE,
    FOREIGN KEY(`category_id`) REFERENCES `Categories`(`category_id`) ON DELETE CASCADE,
    UNIQUE(`job_id`, `category_id`)
);

CREATE TABLE IF NOT EXISTS `Job_Skill`(
    `job_id` INT,
    `skill_id` INT,
    FOREIGN KEY(`job_id`) REFERENCES `job`(`job_id`) ON DELETE CASCADE,
    FOREIGN KEY(`skill_id`) REFERENCES `Skills`(`skill_id`) ON DELETE CASCADE,
    UNIQUE(`job_id`, `skill_id`)
);

CREATE TABLE IF NOT EXISTS `Job_Tool`(
    `job_id` INT,
    `tool_id` INT,
    FOREIGN KEY(`job_id`) REFERENCES `job`(`job_id`) ON DELETE CASCADE,
    FOREIGN KEY(`tool_id`) REFERENCES `Tools`(`tool_id`) ON DELETE CASCADE,
    UNIQUE(`job_id`, `tool_id`)
);

CREATE TABLE IF NOT EXISTS `Job_Education`(
    `job_id` INT,
    `education_id` INT,
    FOREIGN KEY(`job_id`) REFERENCES `job`(`job_id`) ON DELETE CASCADE,
    FOREIGN KEY(`education_id`) REFERENCES `Education`(`education_id`) ON DELETE CASCADE,
    UNIQUE(`job_id`, `education_id`)
);

CREATE TABLE IF NOT EXISTS `Job_Experience`(
    `job_id` INT,
    `experience_id` INT,
    FOREIGN KEY(`job_id`) REFERENCES `job`(`job_id`) ON DELETE CASCADE,
    FOREIGN KEY(`experience_id`) REFERENCES `Experience`(`experience_id`) ON DELETE CASCADE,
    UNIQUE(`job_id`, `experience_id`)
);

USE `jobdatabase`;

CREATE TABLE IF NOT EXISTS `job` LIKE `job104`.`job`;
CREATE TABLE IF NOT EXISTS `Categories` LIKE `job104`.`Categories`;
CREATE TABLE IF NOT EXISTS `Skills` LIKE `job104`.`Skills`;
CREATE TABLE IF NOT EXISTS `Tools` LIKE `job104`.`Tools`;
CREATE TABLE IF NOT EXISTS `Education` LIKE `job104`.`Education`;
CREATE TABLE IF NOT EXISTS `Experience` LIKE `job104`.`Experience`;
CREATE TABLE IF NOT EXISTS `Job_Category` LIKE `job104`.`Job_Category`;
CREATE TABLE IF NOT EXISTS `Job_Skill` LIKE `job104`.`Job_Skill`;
CREATE TABLE IF NOT EXISTS `Job_Tool` LIKE `job104`.`Job_Tool`;
CREATE TABLE IF NOT EXISTS `Job_Education` LIKE `job104`.`Job_Education`;
CREATE TABLE IF NOT EXISTS `Job_Experience` LIKE `job104`.`Job_Experience`;
