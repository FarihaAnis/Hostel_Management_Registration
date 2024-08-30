CREATE DATABASE `loginpage` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
CREATE TABLE `account_reg` (
  `id` int NOT NULL AUTO_INCREMENT,
  `email` varchar(120) NOT NULL,
  `password` varchar(60) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
CREATE TABLE `admin_page` (
  `id` int NOT NULL AUTO_INCREMENT,
  `org_name` varchar(120) NOT NULL,
  `reg_date` date NOT NULL,
  `org_email` varchar(60) NOT NULL,
  `org_contact_number` varchar(30) NOT NULL,
  `status` varchar(30) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
CREATE TABLE `employee_reg_acc` (
  `id` int NOT NULL AUTO_INCREMENT,
  `first_name` varchar(60) NOT NULL,
  `last_name` varchar(60) NOT NULL,
  `job_title` varchar(60) NOT NULL,
  `department` varchar(60) NOT NULL,
  `gender` varchar(30) NOT NULL,
  `date_of_birth` date NOT NULL,
  `marital_status` varchar(30) NOT NULL,
  `email` varchar(120) NOT NULL,
  `contact_number` varchar(30) NOT NULL,
  `street_address` varchar(120) NOT NULL,
  `city` varchar(60) NOT NULL,
  `state` varchar(40) NOT NULL,
  `postcode` int NOT NULL,
  `country` varchar(60) NOT NULL,
  `employee_id` int NOT NULL,
  KEY `id_idx` (`id`),
  KEY `employee_account_reg` (`employee_id`),
  CONSTRAINT `employee_account_reg` FOREIGN KEY (`employee_id`) REFERENCES `account_reg` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
CREATE TABLE `login_details` (
  `id` int NOT NULL AUTO_INCREMENT,
  `email` varchar(120) NOT NULL,
  `password` varchar(60) NOT NULL,
  `account_type` varchar(60) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
