-- MySQL dump 10.13  Distrib 8.0.45, for Linux (x86_64)
--
-- Host: localhost    Database: monitoring_hub
-- ------------------------------------------------------
-- Server version	8.0.45

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
-- Table structure for table `alerts`
--

DROP TABLE IF EXISTS `alerts`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `alerts` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `resource_id` bigint NOT NULL,
  `metric_name` varchar(100) NOT NULL,
  `severity` varchar(20) NOT NULL,
  `current_value` double NOT NULL,
  `threshold` double NOT NULL,
  `status` varchar(20) NOT NULL,
  `value` double DEFAULT NULL,
  `triggered_at` datetime NOT NULL,
  `resolved_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `alerts`
--

LOCK TABLES `alerts` WRITE;
/*!40000 ALTER TABLE `alerts` DISABLE KEYS */;
INSERT INTO `alerts` VALUES (1,1,'cpu','CRITICAL',0,0,'ACTIVE',NULL,'2026-02-23 06:26:51',NULL);
/*!40000 ALTER TABLE `alerts` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `audit_logs`
--

DROP TABLE IF EXISTS `audit_logs`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `audit_logs` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `actor` varchar(100) DEFAULT NULL,
  `action` varchar(100) DEFAULT NULL,
  `payload` json DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `audit_logs`
--

LOCK TABLES `audit_logs` WRITE;
/*!40000 ALTER TABLE `audit_logs` DISABLE KEYS */;
/*!40000 ALTER TABLE `audit_logs` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `aws_accounts`
--

DROP TABLE IF EXISTS `aws_accounts`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `aws_accounts` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `account_name` varchar(100) NOT NULL,
  `account_id` varchar(20) NOT NULL,
  `role_arn` varchar(255) NOT NULL,
  `external_id` varchar(100) DEFAULT NULL,
  `default_region` varchar(20) DEFAULT 'ap-south-2',
  `status` enum('active','inactive') DEFAULT 'active',
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `description` varchar(255) DEFAULT NULL,
  `onboarded_by` bigint DEFAULT NULL,
  `last_synced_at` timestamp NULL DEFAULT NULL,
  `last_discovered_at` timestamp NULL DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `idx_aws_accounts_last_discovered` (`last_discovered_at`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `aws_accounts`
--

LOCK TABLES `aws_accounts` WRITE;
/*!40000 ALTER TABLE `aws_accounts` DISABLE KEYS */;
INSERT INTO `aws_accounts` VALUES (1,'AuroGov','924922671984','arn:aws:iam::924922671984:role/GrafanaEC2Role',NULL,'ap-south-2','active','2026-02-23 10:01:14',NULL,NULL,NULL,'2026-02-24 07:07:58');
/*!40000 ALTER TABLE `aws_accounts` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `dashboard_panels`
--

DROP TABLE IF EXISTS `dashboard_panels`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `dashboard_panels` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `dashboard_id` bigint DEFAULT NULL,
  `metric_id` bigint DEFAULT NULL,
  `title` varchar(100) DEFAULT NULL,
  `visualization` enum('line','bar','gauge','table') DEFAULT NULL,
  `refresh_interval` int DEFAULT NULL,
  `enabled` tinyint(1) DEFAULT '1',
  `position_x` int DEFAULT '0',
  `position_y` int DEFAULT '0',
  `width` int DEFAULT '6',
  `height` int DEFAULT '4',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `dashboard_panels`
--

LOCK TABLES `dashboard_panels` WRITE;
/*!40000 ALTER TABLE `dashboard_panels` DISABLE KEYS */;
/*!40000 ALTER TABLE `dashboard_panels` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `dashboards`
--

DROP TABLE IF EXISTS `dashboards`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `dashboards` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `name` varchar(100) DEFAULT NULL,
  `aws_account_id` bigint DEFAULT NULL,
  `is_default` tinyint(1) DEFAULT '0',
  `enabled` tinyint(1) DEFAULT '1',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `dashboards`
--

LOCK TABLES `dashboards` WRITE;
/*!40000 ALTER TABLE `dashboards` DISABLE KEYS */;
/*!40000 ALTER TABLE `dashboards` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `environments`
--

DROP TABLE IF EXISTS `environments`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `environments` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `name` varchar(50) NOT NULL,
  `tag_key` varchar(50) NOT NULL,
  `tag_value` varchar(50) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `environments`
--

LOCK TABLES `environments` WRITE;
/*!40000 ALTER TABLE `environments` DISABLE KEYS */;
INSERT INTO `environments` VALUES (1,'prod','environment','prod'),(2,'uat','environment','uat');
/*!40000 ALTER TABLE `environments` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `metric_catalog`
--

DROP TABLE IF EXISTS `metric_catalog`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `metric_catalog` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `service` varchar(50) DEFAULT NULL,
  `metric_name` varchar(100) DEFAULT NULL,
  `namespace` varchar(100) DEFAULT NULL,
  `statistic` varchar(20) DEFAULT NULL,
  `unit` varchar(20) DEFAULT NULL,
  `default_interval` int DEFAULT NULL,
  `enabled` tinyint(1) DEFAULT '1',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `metric_catalog`
--

LOCK TABLES `metric_catalog` WRITE;
/*!40000 ALTER TABLE `metric_catalog` DISABLE KEYS */;
INSERT INTO `metric_catalog` VALUES (1,'ec2','CPUUtilization','AWS/EC2','Average','Percent',300,1),(2,'ec2','StatusCheckFailed','AWS/EC2','Maximum','Count',300,1),(3,'ec2','CPUUtilization','AWS/EC2','Average','Percent',300,1),(4,'ec2','StatusCheckFailed','AWS/EC2','Maximum','Count',300,1),(5,'ebs','VolumeQueueLength','AWS/EBS','Average','Count',300,1),(6,'ebs','BurstBalance','AWS/EBS','Average','Percent',300,1),(7,'alb','HTTPCode_Target_5XX_Count','AWS/ApplicationELB','Sum','Count',300,1),(8,'alb','HealthyHostCount','AWS/ApplicationELB','Average','Count',300,1),(9,'rds','CPUUtilization','AWS/RDS','Average','Percent',300,1),(10,'rds','FreeStorageSpace','AWS/RDS','Average','Bytes',300,1),(11,'apigw','5XXError','AWS/ApiGateway','Sum','Count',300,1);
/*!40000 ALTER TABLE `metric_catalog` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `metric_configs`
--

DROP TABLE IF EXISTS `metric_configs`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `metric_configs` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `metric_id` bigint DEFAULT NULL,
  `aws_account_id` bigint DEFAULT NULL,
  `collection_interval` int DEFAULT NULL,
  `enabled` tinyint(1) DEFAULT '1',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `metric_configs`
--

LOCK TABLES `metric_configs` WRITE;
/*!40000 ALTER TABLE `metric_configs` DISABLE KEYS */;
/*!40000 ALTER TABLE `metric_configs` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `metric_definitions`
--

DROP TABLE IF EXISTS `metric_definitions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `metric_definitions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `service` varchar(50) DEFAULT NULL,
  `metric_name` varchar(100) DEFAULT NULL,
  `namespace` varchar(100) DEFAULT NULL,
  `statistic` varchar(20) DEFAULT NULL,
  `unit` varchar(20) DEFAULT NULL,
  `description` varchar(255) DEFAULT NULL,
  `enabled` tinyint(1) DEFAULT '1',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `metric_definitions`
--

LOCK TABLES `metric_definitions` WRITE;
/*!40000 ALTER TABLE `metric_definitions` DISABLE KEYS */;
/*!40000 ALTER TABLE `metric_definitions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `metrics`
--

DROP TABLE IF EXISTS `metrics`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `metrics` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `resource_id` bigint NOT NULL,
  `metric_name` varchar(100) NOT NULL,
  `metric_value` double DEFAULT NULL,
  `metric_timestamp` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=68 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `metrics`
--

LOCK TABLES `metrics` WRITE;
/*!40000 ALTER TABLE `metrics` DISABLE KEYS */;
INSERT INTO `metrics` VALUES (2,1,'cpu',39.53,'2026-02-23 05:16:52'),(3,2,'cpu',23.98,'2026-02-23 05:16:52'),(4,1,'cpu',92.36,'2026-02-23 06:26:52'),(5,2,'cpu',22.94,'2026-02-23 06:26:52'),(6,1,'cpu',0,'2026-02-23 11:01:45'),(7,2,'cpu',0,'2026-02-23 11:01:46'),(8,3,'cpu',0,'2026-02-23 11:01:47'),(9,4,'cpu',0,'2026-02-23 11:01:48'),(10,5,'cpu',0,'2026-02-23 11:01:49'),(11,6,'cpu',0,'2026-02-23 11:01:49'),(12,7,'cpu',0,'2026-02-23 11:01:50'),(13,8,'cpu',22.6,'2026-02-23 11:01:51'),(14,9,'cpu',6.19,'2026-02-23 11:01:52'),(15,10,'cpu',0.27,'2026-02-23 11:01:53'),(16,11,'cpu',0,'2026-02-23 11:01:54'),(17,12,'cpu',0,'2026-02-23 11:01:54'),(18,13,'cpu',0,'2026-02-23 11:01:55'),(19,14,'cpu',47.47,'2026-02-23 11:01:56'),(20,15,'cpu',4.12,'2026-02-23 11:01:57'),(21,16,'cpu',0,'2026-02-23 11:01:58'),(22,17,'cpu',0.08,'2026-02-23 11:01:59'),(23,1,'cpu',0,'2026-02-24 05:12:38'),(24,2,'cpu',0,'2026-02-24 05:12:39'),(25,3,'cpu',0,'2026-02-24 05:12:39'),(26,4,'cpu',0,'2026-02-24 05:12:39'),(27,5,'cpu',0,'2026-02-24 05:12:40'),(28,6,'cpu',0,'2026-02-24 05:12:40'),(29,7,'cpu',0,'2026-02-24 05:12:41'),(30,8,'cpu',8.85,'2026-02-24 05:12:41'),(31,9,'cpu',4.78,'2026-02-24 05:12:42'),(32,10,'cpu',2.83,'2026-02-24 05:12:42'),(33,11,'cpu',0,'2026-02-24 05:12:43'),(34,12,'cpu',0,'2026-02-24 05:12:43'),(35,13,'cpu',0,'2026-02-24 05:12:43'),(36,14,'cpu',18.23,'2026-02-24 05:12:44'),(37,15,'cpu',4.11,'2026-02-24 05:12:44'),(38,16,'cpu',0,'2026-02-24 05:12:45'),(39,17,'cpu',0.08,'2026-02-24 05:12:45'),(40,8,'cpuutilization',9.120974105567,'2026-02-24 09:15:28'),(41,8,'statuscheckfailed',0,'2026-02-24 09:15:29'),(42,8,'cpuutilization',9.120974105567,'2026-02-24 09:15:29'),(43,8,'statuscheckfailed',0,'2026-02-24 09:15:30'),(44,14,'cpuutilization',17.495950687348145,'2026-02-24 09:15:39'),(45,14,'statuscheckfailed',0,'2026-02-24 09:15:39'),(46,14,'cpuutilization',17.495950687348145,'2026-02-24 09:15:40'),(47,14,'statuscheckfailed',0,'2026-02-24 09:15:40'),(48,15,'cpuutilization',4.056664523515344,'2026-02-24 09:15:41'),(49,15,'statuscheckfailed',0,'2026-02-24 09:15:41'),(50,15,'cpuutilization',4.056664523515344,'2026-02-24 09:15:41'),(51,15,'statuscheckfailed',0,'2026-02-24 09:15:42'),(52,17,'cpuutilization',0.08501676665230226,'2026-02-24 09:15:44'),(53,17,'statuscheckfailed',0,'2026-02-24 09:15:44'),(54,17,'cpuutilization',0.08501676665230226,'2026-02-24 09:15:45'),(55,17,'statuscheckfailed',0,'2026-02-24 09:15:45'),(56,23,'cpuutilization',9.120974105567,'2026-02-24 09:15:54'),(57,23,'statuscheckfailed',0,'2026-02-24 09:15:55'),(58,23,'cpuutilization',9.120974105567,'2026-02-24 09:15:55'),(59,23,'statuscheckfailed',0,'2026-02-24 09:15:56'),(60,28,'statuscheckfailed',0,'2026-02-24 09:16:04'),(61,28,'statuscheckfailed',0,'2026-02-24 09:16:04'),(62,29,'statuscheckfailed',0,'2026-02-24 09:16:05'),(63,29,'statuscheckfailed',0,'2026-02-24 09:16:06'),(64,31,'cpuutilization',0.09157204222303619,'2026-02-24 09:16:08'),(65,31,'statuscheckfailed',0,'2026-02-24 09:16:09'),(66,31,'cpuutilization',0.09157204222303619,'2026-02-24 09:16:09'),(67,31,'statuscheckfailed',0,'2026-02-24 09:16:10');
/*!40000 ALTER TABLE `metrics` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `resources`
--

DROP TABLE IF EXISTS `resources`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `resources` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `aws_account_id` bigint NOT NULL,
  `resource_type` varchar(20) NOT NULL,
  `resource_id` varchar(100) NOT NULL,
  `name` varchar(255) DEFAULT NULL,
  `tags` json DEFAULT NULL,
  `environment_id` bigint DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=32 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `resources`
--

LOCK TABLES `resources` WRITE;
/*!40000 ALTER TABLE `resources` DISABLE KEYS */;
INSERT INTO `resources` VALUES (1,1,'ec2','i-0abc123','web-server-1',NULL,NULL,'2026-02-23 06:25:02'),(2,1,'ec2','i-0def456','api-server-1',NULL,NULL,'2026-02-23 06:25:02'),(3,1,'ec2','i-0ae6bbde37e6fd71a','linux - don\'t delete',NULL,NULL,'2026-02-23 10:15:34'),(4,1,'ec2','i-0fc64aadc2a5686fb','JUMP_HOST',NULL,NULL,'2026-02-23 10:15:34'),(5,1,'ec2','i-0ef71e28c46d455ae','LLM-testing',NULL,NULL,'2026-02-23 10:15:34'),(6,1,'ec2','i-04e60fe5209205693','CI testing ',NULL,NULL,'2026-02-23 10:15:34'),(7,1,'ec2','i-064552b905b43f04c','CW Demo',NULL,NULL,'2026-02-23 10:15:34'),(8,1,'ec2','i-05103de7bd4a197be','Demo-server',NULL,NULL,'2026-02-23 10:15:34'),(9,1,'ec2','i-001bd6c1a5a8ec6e4','Grafan-test',NULL,NULL,'2026-02-23 10:15:34'),(10,1,'ec2','i-09b3c369b61943e58','Prometheus',NULL,NULL,'2026-02-23 10:15:34'),(11,1,'ec2','i-0edf7952695975de8','DemoInstance',NULL,NULL,'2026-02-23 10:15:34'),(12,1,'ec2','i-02b24dd863590574a','My-linux-server',NULL,NULL,'2026-02-23 10:15:34'),(13,1,'ec2','i-0d118a4ce2f1272ad','MetaBase-don\'t delete',NULL,NULL,'2026-02-23 10:15:34'),(14,1,'ec2','i-0301d1d155ba900d2','OptScale Server -- dont delete',NULL,NULL,'2026-02-23 10:15:34'),(15,1,'ec2','i-0826299b450c5f26f','GRAFANA-2-Main',NULL,NULL,'2026-02-23 10:15:34'),(16,1,'ec2','i-0e7024d1a0e400bd0','Optscale-Main',NULL,NULL,'2026-02-23 10:15:34'),(17,1,'ec2','i-02b9635fb5da05fbb','Monitoring Dashboard - Don\'t Delete',NULL,NULL,'2026-02-23 10:15:34'),(18,1,'ec2','i-0ae6bbde37e6fd71a','linux - don\'t delete',NULL,NULL,'2026-02-24 07:07:58'),(19,1,'ec2','i-0fc64aadc2a5686fb','JUMP_HOST',NULL,NULL,'2026-02-24 07:07:58'),(20,1,'ec2','i-0ef71e28c46d455ae','LLM-testing',NULL,NULL,'2026-02-24 07:07:58'),(21,1,'ec2','i-04e60fe5209205693','CI testing ',NULL,NULL,'2026-02-24 07:07:58'),(22,1,'ec2','i-064552b905b43f04c','CW Demo',NULL,NULL,'2026-02-24 07:07:58'),(23,1,'ec2','i-05103de7bd4a197be','Demo-server',NULL,NULL,'2026-02-24 07:07:58'),(24,1,'ec2','i-001bd6c1a5a8ec6e4','Grafan-test',NULL,NULL,'2026-02-24 07:07:58'),(25,1,'ec2','i-09b3c369b61943e58','Prometheus',NULL,NULL,'2026-02-24 07:07:58'),(26,1,'ec2','i-02b24dd863590574a','My-linux-server',NULL,NULL,'2026-02-24 07:07:58'),(27,1,'ec2','i-0d118a4ce2f1272ad','MetaBase-don\'t delete',NULL,NULL,'2026-02-24 07:07:58'),(28,1,'ec2','i-0301d1d155ba900d2','OptScale Server -- dont delete',NULL,NULL,'2026-02-24 07:07:58'),(29,1,'ec2','i-0826299b450c5f26f','GRAFANA-2-Main',NULL,NULL,'2026-02-24 07:07:58'),(30,1,'ec2','i-0e7024d1a0e400bd0','Optscale-Main',NULL,NULL,'2026-02-24 07:07:58'),(31,1,'ec2','i-02b9635fb5da05fbb','Monitoring Dashboard - Don\'t Delete',NULL,NULL,'2026-02-24 07:07:58');
/*!40000 ALTER TABLE `resources` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `thresholds`
--

DROP TABLE IF EXISTS `thresholds`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `thresholds` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `aws_account_id` bigint NOT NULL,
  `resource_type` varchar(50) NOT NULL,
  `metric_id` bigint NOT NULL,
  `warning_value` double NOT NULL,
  `critical_value` double NOT NULL,
  `comparison` enum('>','<','>=','<=') NOT NULL,
  `evaluation_period` int NOT NULL DEFAULT '5',
  `enabled` tinyint(1) DEFAULT '1',
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uniq_threshold` (`aws_account_id`,`resource_type`,`metric_id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `thresholds`
--

LOCK TABLES `thresholds` WRITE;
/*!40000 ALTER TABLE `thresholds` DISABLE KEYS */;
INSERT INTO `thresholds` VALUES (1,1,'ec2',1,60,80,'>',5,1,'2026-02-24 09:22:00'),(2,1,'ec2',3,60,80,'>',5,1,'2026-02-24 09:22:00');
/*!40000 ALTER TABLE `thresholds` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `username` varchar(100) NOT NULL,
  `password_hash` varchar(255) NOT NULL,
  `role` varchar(20) NOT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-02-24 18:32:59
