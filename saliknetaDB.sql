-- MySQL dump 10.13  Distrib 8.0.14, for Win64 (x86_64)
--
-- Host: localhost    Database: saliknetadb
-- ------------------------------------------------------
-- Server version	8.0.14

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
 SET NAMES utf8 ;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `auth_group`
--

DROP TABLE IF EXISTS `auth_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `auth_group` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(80) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group`
--

LOCK TABLES `auth_group` WRITE;
/*!40000 ALTER TABLE `auth_group` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group_permissions`
--

DROP TABLE IF EXISTS `auth_group_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `auth_group_permissions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `group_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group_permissions`
--

LOCK TABLES `auth_group_permissions` WRITE;
/*!40000 ALTER TABLE `auth_group_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_permission`
--

DROP TABLE IF EXISTS `auth_permission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `auth_permission` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `codename` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`),
  CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=93 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_permission`
--

LOCK TABLES `auth_permission` WRITE;
/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
INSERT INTO `auth_permission` VALUES (1,'Can add log entry',1,'add_logentry'),(2,'Can change log entry',1,'change_logentry'),(3,'Can delete log entry',1,'delete_logentry'),(4,'Can view log entry',1,'view_logentry'),(5,'Can add permission',2,'add_permission'),(6,'Can change permission',2,'change_permission'),(7,'Can delete permission',2,'delete_permission'),(8,'Can view permission',2,'view_permission'),(9,'Can add group',3,'add_group'),(10,'Can change group',3,'change_group'),(11,'Can delete group',3,'delete_group'),(12,'Can view group',3,'view_group'),(13,'Can add user',4,'add_user'),(14,'Can change user',4,'change_user'),(15,'Can delete user',4,'delete_user'),(16,'Can view user',4,'view_user'),(17,'Can add content type',5,'add_contenttype'),(18,'Can change content type',5,'change_contenttype'),(19,'Can delete content type',5,'delete_contenttype'),(20,'Can view content type',5,'view_contenttype'),(21,'Can add session',6,'add_session'),(22,'Can change session',6,'change_session'),(23,'Can delete session',6,'delete_session'),(24,'Can view session',6,'view_session'),(25,'Can add back load',7,'add_backload'),(26,'Can change back load',7,'change_backload'),(27,'Can delete back load',7,'delete_backload'),(28,'Can view back load',7,'view_backload'),(29,'Can add backload lines',8,'add_backloadlines'),(30,'Can change backload lines',8,'change_backloadlines'),(31,'Can delete backload lines',8,'delete_backloadlines'),(32,'Can view backload lines',8,'view_backloadlines'),(33,'Can add branch',9,'add_branch'),(34,'Can change branch',9,'change_branch'),(35,'Can delete branch',9,'delete_branch'),(36,'Can view branch',9,'view_branch'),(37,'Can add cashier',10,'add_cashier'),(38,'Can change cashier',10,'change_cashier'),(39,'Can delete cashier',10,'delete_cashier'),(40,'Can view cashier',10,'view_cashier'),(41,'Can add category',11,'add_category'),(42,'Can change category',11,'change_category'),(43,'Can delete category',11,'delete_category'),(44,'Can view category',11,'view_category'),(45,'Can add delivered products',12,'add_deliveredproducts'),(46,'Can change delivered products',12,'change_deliveredproducts'),(47,'Can delete delivered products',12,'delete_deliveredproducts'),(48,'Can view delivered products',12,'view_deliveredproducts'),(49,'Can add delivery',13,'add_delivery'),(50,'Can change delivery',13,'change_delivery'),(51,'Can delete delivery',13,'delete_delivery'),(52,'Can view delivery',13,'view_delivery'),(53,'Can add invoice lines',14,'add_invoicelines'),(54,'Can change invoice lines',14,'change_invoicelines'),(55,'Can delete invoice lines',14,'delete_invoicelines'),(56,'Can view invoice lines',14,'view_invoicelines'),(57,'Can add manager',15,'add_manager'),(58,'Can change manager',15,'change_manager'),(59,'Can delete manager',15,'delete_manager'),(60,'Can view manager',15,'view_manager'),(61,'Can add order lines',16,'add_orderlines'),(62,'Can change order lines',16,'change_orderlines'),(63,'Can delete order lines',16,'delete_orderlines'),(64,'Can view order lines',16,'view_orderlines'),(65,'Can add product',17,'add_product'),(66,'Can change product',17,'change_product'),(67,'Can delete product',17,'delete_product'),(68,'Can view product',17,'view_product'),(69,'Can add purchase order',18,'add_purchaseorder'),(70,'Can change purchase order',18,'change_purchaseorder'),(71,'Can delete purchase order',18,'delete_purchaseorder'),(72,'Can view purchase order',18,'view_purchaseorder'),(73,'Can add sales invoice',19,'add_salesinvoice'),(74,'Can change sales invoice',19,'change_salesinvoice'),(75,'Can delete sales invoice',19,'delete_salesinvoice'),(76,'Can view sales invoice',19,'view_salesinvoice'),(77,'Can add supplier',20,'add_supplier'),(78,'Can change supplier',20,'change_supplier'),(79,'Can delete supplier',20,'delete_supplier'),(80,'Can view supplier',20,'view_supplier'),(81,'Can add transfer lines',21,'add_transferlines'),(82,'Can change transfer lines',21,'change_transferlines'),(83,'Can delete transfer lines',21,'delete_transferlines'),(84,'Can view transfer lines',21,'view_transferlines'),(85,'Can add transfer order',22,'add_transferorder'),(86,'Can change transfer order',22,'change_transferorder'),(87,'Can delete transfer order',22,'delete_transferorder'),(88,'Can view transfer order',22,'view_transferorder'),(89,'Can add post',23,'add_post'),(90,'Can change post',23,'change_post'),(91,'Can delete post',23,'delete_post'),(92,'Can view post',23,'view_post');
/*!40000 ALTER TABLE `auth_permission` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user`
--

DROP TABLE IF EXISTS `auth_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `auth_user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) NOT NULL,
  `first_name` varchar(30) NOT NULL,
  `last_name` varchar(150) NOT NULL,
  `email` varchar(254) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user`
--

LOCK TABLES `auth_user` WRITE;
/*!40000 ALTER TABLE `auth_user` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user_groups`
--

DROP TABLE IF EXISTS `auth_user_groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `auth_user_groups` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `group_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_groups_user_id_group_id_94350c0c_uniq` (`user_id`,`group_id`),
  KEY `auth_user_groups_group_id_97559544_fk_auth_group_id` (`group_id`),
  CONSTRAINT `auth_user_groups_group_id_97559544_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `auth_user_groups_user_id_6a12ed8b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user_groups`
--

LOCK TABLES `auth_user_groups` WRITE;
/*!40000 ALTER TABLE `auth_user_groups` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_user_groups` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user_user_permissions`
--

DROP TABLE IF EXISTS `auth_user_user_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `auth_user_user_permissions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_user_permissions_user_id_permission_id_14a6b632_uniq` (`user_id`,`permission_id`),
  KEY `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user_user_permissions`
--

LOCK TABLES `auth_user_user_permissions` WRITE;
/*!40000 ALTER TABLE `auth_user_user_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_user_user_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_admin_log`
--

DROP TABLE IF EXISTS `django_admin_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `django_admin_log` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint(5) unsigned NOT NULL,
  `change_message` longtext NOT NULL,
  `content_type_id` int(11) DEFAULT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  KEY `django_admin_log_user_id_c564eba6_fk_auth_user_id` (`user_id`),
  CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `django_admin_log_user_id_c564eba6_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_admin_log`
--

LOCK TABLES `django_admin_log` WRITE;
/*!40000 ALTER TABLE `django_admin_log` DISABLE KEYS */;
/*!40000 ALTER TABLE `django_admin_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_content_type`
--

DROP TABLE IF EXISTS `django_content_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `django_content_type` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=24 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_content_type`
--

LOCK TABLES `django_content_type` WRITE;
/*!40000 ALTER TABLE `django_content_type` DISABLE KEYS */;
INSERT INTO `django_content_type` VALUES (1,'admin','logentry'),(3,'auth','group'),(2,'auth','permission'),(4,'auth','user'),(5,'contenttypes','contenttype'),(7,'salikneta','backload'),(8,'salikneta','backloadlines'),(9,'salikneta','branch'),(10,'salikneta','cashier'),(11,'salikneta','category'),(12,'salikneta','deliveredproducts'),(13,'salikneta','delivery'),(14,'salikneta','invoicelines'),(15,'salikneta','manager'),(16,'salikneta','orderlines'),(17,'salikneta','product'),(18,'salikneta','purchaseorder'),(19,'salikneta','salesinvoice'),(20,'salikneta','supplier'),(21,'salikneta','transferlines'),(22,'salikneta','transferorder'),(23,'Saliksys','post'),(6,'sessions','session');
/*!40000 ALTER TABLE `django_content_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_migrations`
--

DROP TABLE IF EXISTS `django_migrations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `django_migrations` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=18 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_migrations`
--

LOCK TABLES `django_migrations` WRITE;
/*!40000 ALTER TABLE `django_migrations` DISABLE KEYS */;
INSERT INTO `django_migrations` VALUES (1,'contenttypes','0001_initial','2018-12-08 14:47:43.484820'),(2,'auth','0001_initial','2018-12-08 14:47:55.205345'),(3,'admin','0001_initial','2018-12-08 14:47:57.099477'),(4,'admin','0002_logentry_remove_auto_add','2018-12-08 14:47:57.161967'),(5,'admin','0003_logentry_add_action_flag_choices','2018-12-08 14:47:57.224447'),(6,'contenttypes','0002_remove_content_type_name','2018-12-08 14:47:58.802213'),(7,'auth','0002_alter_permission_name_max_length','2018-12-08 14:47:59.630130'),(8,'auth','0003_alter_user_email_max_length','2018-12-08 14:48:01.004810'),(9,'auth','0004_alter_user_username_opts','2018-12-08 14:48:01.067293'),(10,'auth','0005_alter_user_last_login_null','2018-12-08 14:48:02.176449'),(11,'auth','0006_require_contenttypes_0002','2018-12-08 14:48:02.270140'),(12,'auth','0007_alter_validators_add_error_messages','2018-12-08 14:48:02.536106'),(13,'auth','0008_alter_user_username_max_length','2018-12-08 14:48:03.941623'),(14,'auth','0009_alter_user_last_name_max_length','2018-12-08 14:48:05.429277'),(15,'salikneta','0001_initial','2018-12-08 14:48:44.092181'),(16,'sessions','0001_initial','2018-12-08 14:48:44.904488'),(17,'Saliksys','0001_initial','2019-01-26 06:47:02.803988');
/*!40000 ALTER TABLE `django_migrations` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_session`
--

DROP TABLE IF EXISTS `django_session`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_expire_date_a5c62663` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_session`
--

LOCK TABLES `django_session` WRITE;
/*!40000 ALTER TABLE `django_session` DISABLE KEYS */;
INSERT INTO `django_session` VALUES ('6bgknscc5z43wm7gh2j1qn9yeulyhb99','YzJjNmFjMmJmYmE1YmEwZjYwYTY3OWI0Zjk0N2IxNjdhOTYyZWVjYjp7InVzZXJuYW1lIjoicHJvZHVjdGlvbkBnbWFpbC5jb20iLCJ1c2VydHlwZSI6Im1hbmFnZXIiLCJsb2dnZWQiOnRydWUsInVzZXJJRCI6NCwiZmlyc3RuYW1lIjoiUm9zZSIsImxhc3RuYW1lIjoiUHJvZHVjaXRvbiJ9','2019-06-25 08:07:24.838991'),('6nhr5yiou8zbsr57semiadvkecbk86ji','MDM4ODkxYTM0MjNjNzA3Y2YyOWFhMGU0NDRlYjY2YzNmNDkxZmEyMjp7InVzZXJuYW1lIjoiY2FzaGllckBnbWFpbC5jb20iLCJ1c2VydHlwZSI6ImNhc2hpZXIiLCJsb2dnZWQiOnRydWUsInVzZXJJRCI6MiwiZmlyc3RuYW1lIjoiQ2hpbmdvbmEiLCJsYXN0bmFtZSI6IkNoYXNoaWVyIn0=','2019-02-09 15:00:35.083223'),('dpi72r63l1bppqmijnw0t1qtq1kf49fq','MDM4ODkxYTM0MjNjNzA3Y2YyOWFhMGU0NDRlYjY2YzNmNDkxZmEyMjp7InVzZXJuYW1lIjoiY2FzaGllckBnbWFpbC5jb20iLCJ1c2VydHlwZSI6ImNhc2hpZXIiLCJsb2dnZWQiOnRydWUsInVzZXJJRCI6MiwiZmlyc3RuYW1lIjoiQ2hpbmdvbmEiLCJsYXN0bmFtZSI6IkNoYXNoaWVyIn0=','2019-01-30 09:57:46.273221'),('ij3i30ztkd8hmu1omuilo4fgxdhhm0f3','NTU5ZjgxY2YyYmU5NTMwOTdkMjgxNzRhMTkwMGI0NzQ2YjI1NDY3ODp7InVzZXJuYW1lIjoibWFuYWdlckBnbWFpbC5jb20iLCJsb2dnZWQiOnRydWUsInVzZXJJRCI6MywiZmlyc3RuYW1lIjoiTWFuYWdpbmciLCJsYXN0bmFtZSI6Ik1hbmFyb3QiLCJ1c2VydHlwZSI6Im1hbmFnZXIifQ==','2019-04-07 22:05:23.485096'),('iog12eywxkcttp8bq18ugjzr02bt7xjt','MDM4ODkxYTM0MjNjNzA3Y2YyOWFhMGU0NDRlYjY2YzNmNDkxZmEyMjp7InVzZXJuYW1lIjoiY2FzaGllckBnbWFpbC5jb20iLCJ1c2VydHlwZSI6ImNhc2hpZXIiLCJsb2dnZWQiOnRydWUsInVzZXJJRCI6MiwiZmlyc3RuYW1lIjoiQ2hpbmdvbmEiLCJsYXN0bmFtZSI6IkNoYXNoaWVyIn0=','2018-12-26 19:37:45.569007'),('ndhb3kvzfgbge272jpvk8y8k77scuydr','MDM4ODkxYTM0MjNjNzA3Y2YyOWFhMGU0NDRlYjY2YzNmNDkxZmEyMjp7InVzZXJuYW1lIjoiY2FzaGllckBnbWFpbC5jb20iLCJ1c2VydHlwZSI6ImNhc2hpZXIiLCJsb2dnZWQiOnRydWUsInVzZXJJRCI6MiwiZmlyc3RuYW1lIjoiQ2hpbmdvbmEiLCJsYXN0bmFtZSI6IkNoYXNoaWVyIn0=','2019-02-05 10:49:59.950988'),('qdg3ngulualdvjcbq1j5du19xa4ddrht','MDM4ODkxYTM0MjNjNzA3Y2YyOWFhMGU0NDRlYjY2YzNmNDkxZmEyMjp7InVzZXJuYW1lIjoiY2FzaGllckBnbWFpbC5jb20iLCJ1c2VydHlwZSI6ImNhc2hpZXIiLCJsb2dnZWQiOnRydWUsInVzZXJJRCI6MiwiZmlyc3RuYW1lIjoiQ2hpbmdvbmEiLCJsYXN0bmFtZSI6IkNoYXNoaWVyIn0=','2019-03-09 13:25:47.524474');
/*!40000 ALTER TABLE `django_session` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `notifs`
--

DROP TABLE IF EXISTS `notifs`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `notifs` (
  `notif_id` int(11) NOT NULL AUTO_INCREMENT,
  `msg` varchar(150) DEFAULT NULL,
  `timestamp` datetime DEFAULT NULL,
  `viewed` tinyint(4) DEFAULT '0',
  PRIMARY KEY (`notif_id`)
) ENGINE=InnoDB AUTO_INCREMENT=47 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `notifs`
--

LOCK TABLES `notifs` WRITE;
/*!40000 ALTER TABLE `notifs` DISABLE KEYS */;
INSERT INTO `notifs` VALUES (26,'New Item -Apple- has been added.','2018-12-12 19:23:24',1),(27,'New Item -Tomato- has been added.','2018-12-12 19:24:05',1),(28,'New Item -Buko Shake- has been added.','2018-12-12 19:24:56',1),(29,'New Item -Rice Meal- has been added.','2018-12-12 19:25:44',1),(30,'New Item -Pork Liempo- has been added.','2018-12-12 19:26:29',1),(31,'New Item -Eggs- has been added.','2018-12-12 19:27:07',1),(32,'New Item -Eggplant- has been added.','2018-12-12 19:27:56',1),(33,'New PO37 has been added.','2018-12-12 19:56:00',1),(34,'New PO38 has been added.','2018-12-12 19:56:46',1),(35,'New PO39 has been added.','2018-12-12 19:57:49',1),(36,'New PO40 has been added.','2018-12-12 19:58:13',1),(37,'Products have been backloaded.','2018-12-12 19:59:34',1),(38,'Products have been delivered.','2018-12-12 20:00:03',1),(39,'Products have been delivered.','2018-12-12 20:00:46',1),(40,'Products have been delivered.','2018-12-12 20:01:21',1),(41,'Products have been delivered.','2018-12-12 20:01:38',1),(42,'Products have been backloaded.','2018-12-12 20:07:21',1),(43,'Products have been backloaded.','2018-12-12 20:07:45',1),(44,'New Item -Jemuel Tit- has been added.','2019-01-16 10:01:38',1),(45,'New PO41 has been added.','2019-05-29 14:33:17',NULL),(46,'New PO42 has been added.','2019-05-29 14:34:04',NULL);
/*!40000 ALTER TABLE `notifs` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `salikneta_backload`
--

DROP TABLE IF EXISTS `salikneta_backload`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `salikneta_backload` (
  `idBackload` int(11) NOT NULL AUTO_INCREMENT,
  `backloadDate` date NOT NULL,
  `idCashier_id` int(11) NOT NULL,
  PRIMARY KEY (`idBackload`),
  KEY `salikneta_backload_idCashier_id_139ac1e7_fk_salikneta` (`idCashier_id`),
  CONSTRAINT `salikneta_backload_idCashier_id_139ac1e7_fk_salikneta` FOREIGN KEY (`idCashier_id`) REFERENCES `salikneta_cashier` (`idCashier`)
) ENGINE=InnoDB AUTO_INCREMENT=17 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `salikneta_backload`
--

LOCK TABLES `salikneta_backload` WRITE;
/*!40000 ALTER TABLE `salikneta_backload` DISABLE KEYS */;
INSERT INTO `salikneta_backload` VALUES (14,'2018-12-12',2),(15,'2018-12-12',2),(16,'2018-12-12',2);
/*!40000 ALTER TABLE `salikneta_backload` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `salikneta_backloadlines`
--

DROP TABLE IF EXISTS `salikneta_backloadlines`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `salikneta_backloadlines` (
  `idBackloadLines` int(11) NOT NULL AUTO_INCREMENT,
  `qty` double NOT NULL,
  `idProduct_id` int(11) NOT NULL,
  `reason` varchar(45) DEFAULT NULL,
  `idBackload` int(11) DEFAULT NULL,
  PRIMARY KEY (`idBackloadLines`),
  KEY `salikneta_backloadli_idProduct_id_dcecf50b_fk_salikneta` (`idProduct_id`),
  KEY `idBackload_idx` (`idBackload`),
  CONSTRAINT `idBackload` FOREIGN KEY (`idBackload`) REFERENCES `salikneta_backload` (`idBackload`),
  CONSTRAINT `salikneta_backloadli_idProduct_id_dcecf50b_fk_salikneta` FOREIGN KEY (`idProduct_id`) REFERENCES `salikneta_product` (`idProduct`)
) ENGINE=InnoDB AUTO_INCREMENT=19 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `salikneta_backloadlines`
--

LOCK TABLES `salikneta_backloadlines` WRITE;
/*!40000 ALTER TABLE `salikneta_backloadlines` DISABLE KEYS */;
INSERT INTO `salikneta_backloadlines` VALUES (13,5,4,'Expired',14),(14,4,7,'Expired',15),(15,2,6,'Dirty',15),(16,1,4,'Expired',16),(17,1,7,'Expired',16),(18,1,6,'Expired',16);
/*!40000 ALTER TABLE `salikneta_backloadlines` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `salikneta_branch`
--

DROP TABLE IF EXISTS `salikneta_branch`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `salikneta_branch` (
  `idBranch` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(45) NOT NULL,
  PRIMARY KEY (`idBranch`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `salikneta_branch`
--

LOCK TABLES `salikneta_branch` WRITE;
/*!40000 ALTER TABLE `salikneta_branch` DISABLE KEYS */;
INSERT INTO `salikneta_branch` VALUES (1,'Marketing'),(2,'Production'),(3,'Animal'),(4,'Vegetable ');
/*!40000 ALTER TABLE `salikneta_branch` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `salikneta_cashier`
--

DROP TABLE IF EXISTS `salikneta_cashier`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `salikneta_cashier` (
  `idCashier` int(11) NOT NULL AUTO_INCREMENT,
  `firstname` varchar(45) NOT NULL,
  `lastname` varchar(45) NOT NULL,
  `username` varchar(45) NOT NULL,
  `password` varchar(45) NOT NULL,
  `idBranch_id` int(11) NOT NULL,
  PRIMARY KEY (`idCashier`),
  KEY `salikneta_cashier_idBranch_id_9067f2ad_fk_salikneta` (`idBranch_id`),
  CONSTRAINT `salikneta_cashier_idBranch_id_9067f2ad_fk_salikneta` FOREIGN KEY (`idBranch_id`) REFERENCES `salikneta_branch` (`idBranch`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `salikneta_cashier`
--

LOCK TABLES `salikneta_cashier` WRITE;
/*!40000 ALTER TABLE `salikneta_cashier` DISABLE KEYS */;
INSERT INTO `salikneta_cashier` VALUES (2,'Chingona','Chashier','cashier@gmail.com','123',1),(3,'Manaloto','Managing','cashier2@gmail.com','123',1);
/*!40000 ALTER TABLE `salikneta_cashier` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `salikneta_category`
--

DROP TABLE IF EXISTS `salikneta_category`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `salikneta_category` (
  `idCategory` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(45) NOT NULL,
  `description` varchar(45) NOT NULL,
  PRIMARY KEY (`idCategory`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `salikneta_category`
--

LOCK TABLES `salikneta_category` WRITE;
/*!40000 ALTER TABLE `salikneta_category` DISABLE KEYS */;
INSERT INTO `salikneta_category` VALUES (5,'Poultry','Mga baboy na kakanin'),(6,'Fruits','Prutas at sibuyas'),(7,'Vegetable','Gulay at kamatis'),(8,'Special Item','Special menu'),(9,'Beverages','Inumin');
/*!40000 ALTER TABLE `salikneta_category` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `salikneta_deliveredproducts`
--

DROP TABLE IF EXISTS `salikneta_deliveredproducts`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `salikneta_deliveredproducts` (
  `idDeliveredProducts` int(11) NOT NULL AUTO_INCREMENT,
  `qty` double NOT NULL,
  `idDelivery_id` int(11) NOT NULL,
  `idOrderLines_id` int(11) NOT NULL,
  PRIMARY KEY (`idDeliveredProducts`),
  KEY `salikneta_deliveredp_idDelivery_id_f95a6dc8_fk_salikneta` (`idDelivery_id`),
  KEY `salikneta_deliveredp_idOrderLines_id_a6877487_fk_salikneta` (`idOrderLines_id`),
  CONSTRAINT `salikneta_deliveredp_idDelivery_id_f95a6dc8_fk_salikneta` FOREIGN KEY (`idDelivery_id`) REFERENCES `salikneta_delivery` (`idDelivery`),
  CONSTRAINT `salikneta_deliveredp_idOrderLines_id_a6877487_fk_salikneta` FOREIGN KEY (`idOrderLines_id`) REFERENCES `salikneta_orderlines` (`idOrderLines`)
) ENGINE=InnoDB AUTO_INCREMENT=49 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `salikneta_deliveredproducts`
--

LOCK TABLES `salikneta_deliveredproducts` WRITE;
/*!40000 ALTER TABLE `salikneta_deliveredproducts` DISABLE KEYS */;
INSERT INTO `salikneta_deliveredproducts` VALUES (44,25,48,37),(45,50,49,38),(46,1,49,39),(47,100,50,41),(48,88,51,40);
/*!40000 ALTER TABLE `salikneta_deliveredproducts` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `salikneta_delivery`
--

DROP TABLE IF EXISTS `salikneta_delivery`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `salikneta_delivery` (
  `idDelivery` int(11) NOT NULL AUTO_INCREMENT,
  `deliveryDate` date NOT NULL,
  `idPurchaseOrder_id` int(11) NOT NULL,
  PRIMARY KEY (`idDelivery`),
  KEY `salikneta_delivery_idPurchaseOrder_id_80bf84f2_fk_salikneta` (`idPurchaseOrder_id`),
  CONSTRAINT `salikneta_delivery_idPurchaseOrder_id_80bf84f2_fk_salikneta` FOREIGN KEY (`idPurchaseOrder_id`) REFERENCES `salikneta_purchaseorder` (`idPurchaseOrder`)
) ENGINE=InnoDB AUTO_INCREMENT=52 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `salikneta_delivery`
--

LOCK TABLES `salikneta_delivery` WRITE;
/*!40000 ALTER TABLE `salikneta_delivery` DISABLE KEYS */;
INSERT INTO `salikneta_delivery` VALUES (48,'2018-12-12',37),(49,'2018-12-12',38),(50,'2018-12-12',40),(51,'2019-05-29',39);
/*!40000 ALTER TABLE `salikneta_delivery` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `salikneta_ingredientlist`
--

DROP TABLE IF EXISTS `salikneta_ingredientlist`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `salikneta_ingredientlist` (
  `ingredientslistId` int(11) NOT NULL,
  `productProd` float NOT NULL,
  `prodUsed` float NOT NULL,
  `unitOfMeasure` varchar(45) NOT NULL,
  `ingredientProduct` int(11) NOT NULL,
  PRIMARY KEY (`ingredientslistId`),
  KEY `fk_salikneta_ingredientlist_salikneta_product_idx` (`ingredientProduct`),
  CONSTRAINT `fk_salikneta_ingredientlist_salikneta_product` FOREIGN KEY (`ingredientProduct`) REFERENCES `salikneta_product` (`idProduct`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `salikneta_ingredientlist`
--

LOCK TABLES `salikneta_ingredientlist` WRITE;
/*!40000 ALTER TABLE `salikneta_ingredientlist` DISABLE KEYS */;
/*!40000 ALTER TABLE `salikneta_ingredientlist` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `salikneta_invoicelines`
--

DROP TABLE IF EXISTS `salikneta_invoicelines`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `salikneta_invoicelines` (
  `idInvoiceLines` int(11) NOT NULL AUTO_INCREMENT,
  `unitPrice` double NOT NULL,
  `qty` double NOT NULL,
  `idProduct_id` int(11) NOT NULL,
  `disc` float DEFAULT NULL,
  `idSales` int(11) DEFAULT NULL,
  PRIMARY KEY (`idInvoiceLines`),
  KEY `salikneta_invoicelin_idProduct_id_ea44a6fb_fk_salikneta` (`idProduct_id`),
  KEY `idSales_idx` (`idSales`),
  CONSTRAINT `idSales` FOREIGN KEY (`idSales`) REFERENCES `salikneta_salesinvoice` (`idSales`),
  CONSTRAINT `salikneta_invoicelin_idProduct_id_ea44a6fb_fk_salikneta` FOREIGN KEY (`idProduct_id`) REFERENCES `salikneta_product` (`idProduct`)
) ENGINE=InnoDB AUTO_INCREMENT=36 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `salikneta_invoicelines`
--

LOCK TABLES `salikneta_invoicelines` WRITE;
/*!40000 ALTER TABLE `salikneta_invoicelines` DISABLE KEYS */;
INSERT INTO `salikneta_invoicelines` VALUES (5,30,5,4,20,6),(6,20,0.5,5,0,6),(7,160,0.75,8,0,6),(8,30,2,4,0,7),(9,65,5,7,5,7),(10,15,3,9,0,7),(11,78,4,6,0,8),(12,30,20,10,15,9),(13,20,10,5,0,10),(14,15,10,9,0,10),(15,65,5,7,10,11),(16,30,3,4,10,11),(17,78,2,6,0,11),(18,15,5,9,0,12),(19,65,20,7,20,12),(20,65,30,7,0,13),(21,30,10,4,0,13),(22,20,10,5,0,13),(23,78,5,6,0,13),(24,30,15,10,0,13),(25,30,17,4,10,14),(26,160,0.8,8,0,14),(27,160,0.5,8,10,15),(28,78,3,6,0,15),(29,20,19.5,5,0,16),(30,78,5,6,0,16),(31,160,7.25,8,0,17),(32,65,20,7,0,17),(33,78,1,6,4,17),(34,160,5.555,8,0,18),(35,15,7,9,0,18);
/*!40000 ALTER TABLE `salikneta_invoicelines` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `salikneta_manager`
--

DROP TABLE IF EXISTS `salikneta_manager`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `salikneta_manager` (
  `idManager` int(11) NOT NULL AUTO_INCREMENT,
  `firstname` varchar(45) NOT NULL,
  `lastname` varchar(45) NOT NULL,
  `username` varchar(45) NOT NULL,
  `password` varchar(45) NOT NULL,
  `idBranch_id` int(11) NOT NULL,
  PRIMARY KEY (`idManager`),
  KEY `salikneta_manager_idBranch_id_73d50c80_fk_salikneta` (`idBranch_id`),
  CONSTRAINT `salikneta_manager_idBranch_id_73d50c80_fk_salikneta` FOREIGN KEY (`idBranch_id`) REFERENCES `salikneta_branch` (`idBranch`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `salikneta_manager`
--

LOCK TABLES `salikneta_manager` WRITE;
/*!40000 ALTER TABLE `salikneta_manager` DISABLE KEYS */;
INSERT INTO `salikneta_manager` VALUES (3,'Managing','Manarot','manager@gmail.com','123',1),(4,'Rose','Produciton','production@gmail.com','123',2),(5,'Christohper','Animal','animal@gmail.com','123',3),(6,'Manny','Vegetable','vegetable@gmail.com','123',4),(7,'Mae','Marketing','marketing@gmail.com','123',1);
/*!40000 ALTER TABLE `salikneta_manager` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `salikneta_orderlines`
--

DROP TABLE IF EXISTS `salikneta_orderlines`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `salikneta_orderlines` (
  `idOrderLines` int(11) NOT NULL AUTO_INCREMENT,
  `qty` double NOT NULL,
  `idProduct_id` int(11) NOT NULL,
  `idPurchaseOrder_id` int(11) NOT NULL,
  PRIMARY KEY (`idOrderLines`),
  KEY `salikneta_orderlines_idProduct_id_669c2cc2_fk_salikneta` (`idProduct_id`),
  KEY `salikneta_orderlines_idPurchaseOrder_id_e0150586_fk_salikneta` (`idPurchaseOrder_id`),
  CONSTRAINT `salikneta_orderlines_idProduct_id_669c2cc2_fk_salikneta` FOREIGN KEY (`idProduct_id`) REFERENCES `salikneta_product` (`idProduct`),
  CONSTRAINT `salikneta_orderlines_idPurchaseOrder_id_e0150586_fk_salikneta` FOREIGN KEY (`idPurchaseOrder_id`) REFERENCES `salikneta_purchaseorder` (`idPurchaseOrder`)
) ENGINE=InnoDB AUTO_INCREMENT=44 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `salikneta_orderlines`
--

LOCK TABLES `salikneta_orderlines` WRITE;
/*!40000 ALTER TABLE `salikneta_orderlines` DISABLE KEYS */;
INSERT INTO `salikneta_orderlines` VALUES (37,50,4,37),(38,50,5,38),(39,50,6,38),(40,50,10,39),(41,100,7,40),(42,70,4,41),(43,90,8,42);
/*!40000 ALTER TABLE `salikneta_orderlines` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `salikneta_product`
--

DROP TABLE IF EXISTS `salikneta_product`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `salikneta_product` (
  `idProduct` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(45) NOT NULL,
  `description` varchar(45) NOT NULL,
  `suggestedUnitPrice` double NOT NULL,
  `unitsInStock` float NOT NULL,
  `reorderLevel` int(11) NOT NULL,
  `unitOfMeasure` varchar(45) NOT NULL,
  `SKU` int(11) NOT NULL,
  `barcode` varchar(45) NOT NULL,
  `img_path` varchar(150) DEFAULT NULL,
  `idCategory_id` int(11) NOT NULL,
  `unitsReserved` int(11) DEFAULT NULL,
  PRIMARY KEY (`idProduct`),
  KEY `salikneta_product_idCategory_id_e88bfcb9_fk_salikneta` (`idCategory_id`),
  CONSTRAINT `salikneta_product_idCategory_id_e88bfcb9_fk_salikneta` FOREIGN KEY (`idCategory_id`) REFERENCES `salikneta_category` (`idCategory`)
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `salikneta_product`
--

LOCK TABLES `salikneta_product` WRITE;
/*!40000 ALTER TABLE `salikneta_product` DISABLE KEYS */;
INSERT INTO `salikneta_product` VALUES (4,'Apple','Fresh Fuji Apple',30,14,40,'PCS',30,'','prod_img/download_fqnDSey.jpeg',6,5),(5,'Tomato','Tomato Fresh',20,54,40,'KGS',30,'','prod_img/download_1_C9aV9Ow.jpeg',7,0),(6,'Buko Shake','Buko Flavored Shake',78,7,30,'PCS',123,'','prod_img/download_2.jpeg',9,0),(7,'Rice Meal','Rice W/ Rice',65,115,50,'PCS',30,'','prod_img/download_3.jpeg',5,0),(8,'Pork Liempo','Pork Cut Liempo',160,29,30,'KGS',300,'','prod_img/download_4.jpeg',5,5),(9,'Eggs','Golden Eggs',15,15,40,'PCS',10,'','prod_img/download_5.jpeg',8,0),(10,'Eggplant','Raw Talong',30,101,30,'LBS',30,'','prod_img/basket.jpg',7,0);
/*!40000 ALTER TABLE `salikneta_product` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `salikneta_purchaseorder`
--

DROP TABLE IF EXISTS `salikneta_purchaseorder`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `salikneta_purchaseorder` (
  `idPurchaseOrder` int(11) NOT NULL AUTO_INCREMENT,
  `orderDate` date NOT NULL,
  `expectedDate` date NOT NULL,
  `idCashier_id` int(11) NOT NULL,
  `idSupplier_id` int(11) NOT NULL,
  `status` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`idPurchaseOrder`),
  KEY `salikneta_purchaseor_idCashier_id_eb9363f7_fk_salikneta` (`idCashier_id`),
  KEY `salikneta_purchaseor_idSupplier_id_f69c233c_fk_salikneta` (`idSupplier_id`),
  CONSTRAINT `salikneta_purchaseor_idCashier_id_eb9363f7_fk_salikneta` FOREIGN KEY (`idCashier_id`) REFERENCES `salikneta_cashier` (`idCashier`),
  CONSTRAINT `salikneta_purchaseor_idSupplier_id_f69c233c_fk_salikneta` FOREIGN KEY (`idSupplier_id`) REFERENCES `salikneta_supplier` (`idSupplier`)
) ENGINE=InnoDB AUTO_INCREMENT=44 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `salikneta_purchaseorder`
--

LOCK TABLES `salikneta_purchaseorder` WRITE;
/*!40000 ALTER TABLE `salikneta_purchaseorder` DISABLE KEYS */;
INSERT INTO `salikneta_purchaseorder` VALUES (37,'2018-01-01','2014-01-01',2,2,'PARTIALLY RECEIVED'),(38,'2014-01-01','2014-01-01',2,2,'PARTIALLY RECEIVED'),(39,'2014-01-01','2014-01-01',2,3,'PARTIALLY RECEIVED'),(40,'2014-01-01','2014-01-01',2,3,'RECEIVED'),(41,'2014-01-01','2014-01-01',3,2,'In Transit'),(42,'2014-01-01','2014-01-01',3,4,'In Transit');
/*!40000 ALTER TABLE `salikneta_purchaseorder` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `salikneta_salesinvoice`
--

DROP TABLE IF EXISTS `salikneta_salesinvoice`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `salikneta_salesinvoice` (
  `idSales` int(11) NOT NULL AUTO_INCREMENT,
  `invoiceDate` datetime NOT NULL,
  `customer` varchar(45) NOT NULL,
  `idCashier_id` int(11) NOT NULL,
  PRIMARY KEY (`idSales`),
  KEY `salikneta_salesinvoi_idCashier_id_5b7305bb_fk_salikneta` (`idCashier_id`),
  CONSTRAINT `salikneta_salesinvoi_idCashier_id_5b7305bb_fk_salikneta` FOREIGN KEY (`idCashier_id`) REFERENCES `salikneta_cashier` (`idCashier`)
) ENGINE=InnoDB AUTO_INCREMENT=19 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `salikneta_salesinvoice`
--

LOCK TABLES `salikneta_salesinvoice` WRITE;
/*!40000 ALTER TABLE `salikneta_salesinvoice` DISABLE KEYS */;
INSERT INTO `salikneta_salesinvoice` VALUES (6,'2018-11-12 19:38:58','WALK-IN',2),(7,'2018-11-12 19:39:54','WALK-IN',2),(8,'2018-11-15 19:40:41','WALK-IN',2),(9,'2018-11-16 19:41:10','WALK-IN',2),(10,'2018-11-16 19:41:27','WALK-IN',2),(11,'2018-12-09 19:42:09','WALK-IN',2),(12,'2018-12-09 19:42:24','WALK-IN',2),(13,'2018-12-10 19:43:18','WALK-IN',2),(14,'2018-12-10 19:44:40','WALK-IN',2),(15,'2018-12-10 19:46:12','WALK-IN',2),(16,'2018-12-12 19:46:41','WALK-IN',2),(17,'2018-12-12 19:47:21','WALK-IN',2),(18,'2018-12-12 19:48:22','WALK-IN',2);
/*!40000 ALTER TABLE `salikneta_salesinvoice` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `salikneta_supplier`
--

DROP TABLE IF EXISTS `salikneta_supplier`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `salikneta_supplier` (
  `idSupplier` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(45) NOT NULL,
  `contactNumber` varchar(45) NOT NULL,
  `emailAddress` varchar(45) NOT NULL,
  `website` varchar(45) NOT NULL,
  `address1` varchar(45) NOT NULL,
  `address2` varchar(45) NOT NULL,
  `city` varchar(45) NOT NULL,
  `province` varchar(45) NOT NULL,
  `country` varchar(45) NOT NULL,
  `postal` varchar(45) NOT NULL,
  PRIMARY KEY (`idSupplier`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `salikneta_supplier`
--

LOCK TABLES `salikneta_supplier` WRITE;
/*!40000 ALTER TABLE `salikneta_supplier` DISABLE KEYS */;
INSERT INTO `salikneta_supplier` VALUES (2,'Salikneta Farm','123','a@gmail.com','www.aran.com','Makati','Navotas','Tanza','Metro Manila','Philippines','7000'),(3,'San Miguel','09055123','123@gmail.com','www.smiguel.com','Makati','Mandaluyong','Mandakati','Metro Manila','Philippines','233'),(4,'ANimal','09123131933','d@y.com','WWW.C.Com','manila','antipolo','marikin','rizal','philippines','102');
/*!40000 ALTER TABLE `salikneta_supplier` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `salikneta_transferlines`
--

DROP TABLE IF EXISTS `salikneta_transferlines`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `salikneta_transferlines` (
  `idTransferLines` int(11) NOT NULL AUTO_INCREMENT,
  `qty` double NOT NULL,
  `idProduct_id` int(11) NOT NULL,
  `idTransferOrder_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`idTransferLines`),
  KEY `salikneta_transferli_idProduct_id_7e465771_fk_salikneta` (`idProduct_id`),
  KEY `idTransferOrder_idx` (`idTransferOrder_id`),
  CONSTRAINT `idTransferOrder` FOREIGN KEY (`idTransferOrder_id`) REFERENCES `salikneta_transferorder` (`idTransferOrder`),
  CONSTRAINT `salikneta_transferli_idProduct_id_7e465771_fk_salikneta` FOREIGN KEY (`idProduct_id`) REFERENCES `salikneta_product` (`idProduct`)
) ENGINE=InnoDB AUTO_INCREMENT=22 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `salikneta_transferlines`
--

LOCK TABLES `salikneta_transferlines` WRITE;
/*!40000 ALTER TABLE `salikneta_transferlines` DISABLE KEYS */;
INSERT INTO `salikneta_transferlines` VALUES (13,10,4,16),(14,5,5,17),(15,5,9,17),(16,2,10,17),(17,5,4,18),(18,5,8,18),(19,5,9,18),(20,5,4,19),(21,5,8,19);
/*!40000 ALTER TABLE `salikneta_transferlines` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `salikneta_transferorder`
--

DROP TABLE IF EXISTS `salikneta_transferorder`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `salikneta_transferorder` (
  `idTransferOrder` int(11) NOT NULL AUTO_INCREMENT,
  `transferDate` date NOT NULL,
  `expectedDate` date NOT NULL,
  `idCashier_id` int(11) NOT NULL,
  `source_id` int(11) DEFAULT NULL,
  `destination_id` int(11) DEFAULT NULL,
  `status` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`idTransferOrder`),
  KEY `salikneta_transferor_idCashier_id_f3b5c182_fk_salikneta` (`idCashier_id`),
  KEY `source_idx` (`source_id`),
  KEY `destination_idx` (`destination_id`),
  CONSTRAINT `destination` FOREIGN KEY (`destination_id`) REFERENCES `salikneta_branch` (`idBranch`),
  CONSTRAINT `salikneta_transferor_idCashier_id_f3b5c182_fk_salikneta` FOREIGN KEY (`idCashier_id`) REFERENCES `salikneta_cashier` (`idCashier`),
  CONSTRAINT `source` FOREIGN KEY (`source_id`) REFERENCES `salikneta_branch` (`idBranch`)
) ENGINE=InnoDB AUTO_INCREMENT=22 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `salikneta_transferorder`
--

LOCK TABLES `salikneta_transferorder` WRITE;
/*!40000 ALTER TABLE `salikneta_transferorder` DISABLE KEYS */;
INSERT INTO `salikneta_transferorder` VALUES (16,'2018-01-01','2018-01-01',2,1,2,'Finished'),(17,'2018-01-01','2018-01-01',2,1,2,'In Transit'),(18,'2018-01-01','2018-01-01',2,1,2,'Cancelled'),(19,'2018-01-01','2018-01-01',2,1,2,'Draft');
/*!40000 ALTER TABLE `salikneta_transferorder` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `saliksys_post`
--

DROP TABLE IF EXISTS `saliksys_post`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `saliksys_post` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(100) NOT NULL,
  `content` varchar(200) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `saliksys_post`
--

LOCK TABLES `saliksys_post` WRITE;
/*!40000 ALTER TABLE `saliksys_post` DISABLE KEYS */;
/*!40000 ALTER TABLE `saliksys_post` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2019-07-06 15:28:40
