-- MySQL dump 10.13  Distrib 8.0.39, for Win64 (x86_64)
--
-- Host: localhost    Database: project_hm
-- ------------------------------------------------------
-- Server version	8.0.39

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `admins`
--

DROP TABLE IF EXISTS `admins`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `admins` (
  `admin_id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `email` varchar(100) NOT NULL,
  `password` varchar(255) NOT NULL,
  PRIMARY KEY (`admin_id`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `admins`
--

LOCK TABLES `admins` WRITE;
/*!40000 ALTER TABLE `admins` DISABLE KEYS */;
INSERT INTO `admins` VALUES (1,'roshan ','roshan@gmail.com','admin@123'),(2,'sai','sai@gmail.com','admin@456'),(3,'cherukuru','cherukuru@gmail.com','admin@abc'),(4,'Zoro','zoro@gmail.com','zoro@123');
/*!40000 ALTER TABLE `admins` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `appointments`
--

DROP TABLE IF EXISTS `appointments`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `appointments` (
  `appointment_id` int NOT NULL AUTO_INCREMENT,
  `first_name` varchar(100) NOT NULL,
  `last_name` varchar(100) NOT NULL,
  `email` varchar(100) NOT NULL,
  `phone` varchar(15) NOT NULL,
  `medical_condition` text,
  `medications` text,
  `allergies` text,
  `doctor_id` int NOT NULL,
  `appointment_date` date NOT NULL,
  `timeslot` varchar(20) NOT NULL,
  `status` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`appointment_id`),
  KEY `doctor_id` (`doctor_id`),
  CONSTRAINT `appointments_ibfk_1` FOREIGN KEY (`doctor_id`) REFERENCES `doctors` (`doctor_id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `appointments`
--

LOCK TABLES `appointments` WRITE;
/*!40000 ALTER TABLE `appointments` DISABLE KEYS */;
INSERT INTO `appointments` VALUES (4,'ro','bo','robo@gamil.com','100','none','none','none',1,'2024-12-30','11am','Pending'),(5,'ro','sa','rosa@gmail.com','8567419517','noe','none','none',1,'2024-12-31','9am','Pending');
/*!40000 ALTER TABLE `appointments` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `approved_appointments`
--

DROP TABLE IF EXISTS `approved_appointments`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `approved_appointments` (
  `appointment_id` int NOT NULL,
  `first_name` varchar(255) NOT NULL,
  `last_name` varchar(255) NOT NULL,
  `email` varchar(255) NOT NULL,
  `phone` varchar(15) NOT NULL,
  `medical_condition` varchar(255) DEFAULT NULL,
  `medications` varchar(255) DEFAULT NULL,
  `allergies` varchar(255) DEFAULT NULL,
  `doctor_id` int DEFAULT NULL,
  `appointment_date` date DEFAULT NULL,
  `timeslot` time DEFAULT NULL,
  `patient_id` int DEFAULT NULL,
  `status` varchar(50) DEFAULT NULL,
  `doctor_name` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`appointment_id`),
  KEY `doctor_id` (`doctor_id`),
  KEY `patient_id` (`patient_id`),
  CONSTRAINT `approved_appointments_ibfk_1` FOREIGN KEY (`doctor_id`) REFERENCES `doctors` (`doctor_id`),
  CONSTRAINT `approved_appointments_ibfk_2` FOREIGN KEY (`patient_id`) REFERENCES `patients` (`patient_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `approved_appointments`
--

LOCK TABLES `approved_appointments` WRITE;
/*!40000 ALTER TABLE `approved_appointments` DISABLE KEYS */;
INSERT INTO `approved_appointments` VALUES (2,'Jane','Doe','jane.doe@example.com','5552345678','Fever','Tylenol','None',1,'2024-01-15','09:00:00',NULL,'approved','Dr. Smith'),(3,'John','Smith','pat@gmail.com','5559876543','Headache','Ibuprofen','Peanuts',1,'2024-01-20','10:30:00',NULL,'approved','Dr. Smith');
/*!40000 ALTER TABLE `approved_appointments` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `discharged_patients`
--

DROP TABLE IF EXISTS `discharged_patients`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `discharged_patients` (
  `id` int NOT NULL AUTO_INCREMENT,
  `appointment_id` int NOT NULL,
  `first_name` varchar(255) NOT NULL,
  `last_name` varchar(255) NOT NULL,
  `doctor_name` varchar(255) DEFAULT NULL,
  `discharge_date` datetime NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `discharged_patients`
--

LOCK TABLES `discharged_patients` WRITE;
/*!40000 ALTER TABLE `discharged_patients` DISABLE KEYS */;
INSERT INTO `discharged_patients` VALUES (1,1,'sai','cher','rosh','2025-01-02 09:35:43');
/*!40000 ALTER TABLE `discharged_patients` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `doctors`
--

DROP TABLE IF EXISTS `doctors`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `doctors` (
  `doctor_id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(100) DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL,
  `password` varchar(255) DEFAULT NULL,
  `specialization` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`doctor_id`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `doctors`
--

LOCK TABLES `doctors` WRITE;
/*!40000 ALTER TABLE `doctors` DISABLE KEYS */;
INSERT INTO `doctors` VALUES (1,'Roshan ','roshan@gmail.com','doc@123','ortho'),(2,'Dr. Taylor','dr.taylor@example.com','securepassword123','General Medicine');
/*!40000 ALTER TABLE `doctors` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `jobapplications`
--

DROP TABLE IF EXISTS `jobapplications`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `jobapplications` (
  `id` int NOT NULL AUTO_INCREMENT,
  `job_title` varchar(100) NOT NULL,
  `full_name` varchar(100) NOT NULL,
  `email` varchar(100) NOT NULL,
  `phone` varchar(50) NOT NULL,
  `cover_letter` text NOT NULL,
  `status` varchar(20) DEFAULT 'pending',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `jobapplications`
--

LOCK TABLES `jobapplications` WRITE;
/*!40000 ALTER TABLE `jobapplications` DISABLE KEYS */;
INSERT INTO `jobapplications` VALUES (1,'Registered Nurse','Robin','robin@gmail.com','8554669557','hello, my name is robin id like to apply for this job I got experience of 3 years as a nurse.\r\nThank you','pending');
/*!40000 ALTER TABLE `jobapplications` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `patients`
--

DROP TABLE IF EXISTS `patients`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `patients` (
  `patient_id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `email` varchar(255) NOT NULL,
  `password` varchar(255) NOT NULL,
  `phone_number` varchar(15) NOT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`patient_id`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `patients`
--

LOCK TABLES `patients` WRITE;
/*!40000 ALTER TABLE `patients` DISABLE KEYS */;
INSERT INTO `patients` VALUES (1,'Roshan','pat@gmail.com','pat@123','7331121312','2025-01-03 03:53:16');
/*!40000 ALTER TABLE `patients` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ready_to_discharge`
--

DROP TABLE IF EXISTS `ready_to_discharge`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `ready_to_discharge` (
  `appointment_id` int NOT NULL,
  `first_name` varchar(100) DEFAULT NULL,
  `last_name` varchar(100) DEFAULT NULL,
  `appointment_date` date DEFAULT NULL,
  `timeslot` varchar(50) DEFAULT NULL,
  `medical_condition` varchar(255) DEFAULT NULL,
  `discharge_date` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `doctor_name` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`appointment_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ready_to_discharge`
--

LOCK TABLES `ready_to_discharge` WRITE;
/*!40000 ALTER TABLE `ready_to_discharge` DISABLE KEYS */;
INSERT INTO `ready_to_discharge` VALUES (1,'John','Doe','2024-01-15','09:00:00','Normal','2025-01-06 05:11:17','Dr. Smith'),(2,'ro','sai','2024-12-30','03:00:00','critcal','2024-12-30 09:28:05','rosh'),(3,'ravi','cher','2024-12-30','05:00:00','normal','2025-01-06 05:06:44','rosh'),(5,'Charlie','Brown','2024-01-17','11:00:00','Stomach Ache','2025-01-06 05:18:25','Dr. Smith'),(6,'David','Williams','2024-01-17','11:00:00','Allergy','2025-01-06 05:26:37','Dr. Smith');
/*!40000 ALTER TABLE `ready_to_discharge` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-01-28  9:48:43
