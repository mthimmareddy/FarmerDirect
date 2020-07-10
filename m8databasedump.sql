-- MySQL dump 10.13  Distrib 8.0.20, for Win64 (x86_64)
--
-- Host: localhost    Database: m8
-- ------------------------------------------------------
-- Server version	8.0.20

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
-- Table structure for table `blog_user`
--

DROP TABLE IF EXISTS `blog_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `blog_user` (
  `id` int NOT NULL AUTO_INCREMENT,
  `username` varchar(20) NOT NULL,
  `email` varchar(120) NOT NULL,
  `image_file` varchar(20) NOT NULL,
  `password` varchar(60) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `blog_user`
--

LOCK TABLES `blog_user` WRITE;
/*!40000 ALTER TABLE `blog_user` DISABLE KEYS */;
/*!40000 ALTER TABLE `blog_user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `cart`
--

DROP TABLE IF EXISTS `cart`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `cart` (
  `userid` int NOT NULL,
  `productid` int NOT NULL,
  `quantity` int NOT NULL,
  PRIMARY KEY (`userid`,`productid`),
  KEY `productid` (`productid`),
  CONSTRAINT `cart_ibfk_1` FOREIGN KEY (`userid`) REFERENCES `user` (`userid`),
  CONSTRAINT `cart_ibfk_2` FOREIGN KEY (`productid`) REFERENCES `product` (`productid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `cart`
--

LOCK TABLES `cart` WRITE;
/*!40000 ALTER TABLE `cart` DISABLE KEYS */;
INSERT INTO `cart` VALUES (1,3,1),(1,11,1),(2,3,1),(3,21,8),(16,7,1),(16,10,2);
/*!40000 ALTER TABLE `cart` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `category`
--

DROP TABLE IF EXISTS `category`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `category` (
  `categoryid` int NOT NULL AUTO_INCREMENT,
  `category_name` varchar(100) NOT NULL,
  `category_image` varchar(200) NOT NULL,
  `date_posted` datetime NOT NULL,
  PRIMARY KEY (`categoryid`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `category`
--

LOCK TABLES `category` WRITE;
/*!40000 ALTER TABLE `category` DISABLE KEYS */;
INSERT INTO `category` VALUES (1,'Vegetables','/static/images/Vege.png','2020-04-19 14:48:36'),(2,'Bakery','Bakery.png','2020-04-19 14:49:27'),(3,'Fruits','Fruits.png','2020-04-19 14:59:16'),(4,'Dairy','Dairy.png','2020-04-19 16:10:40'),(7,'Honey','','2020-05-10 20:16:53'),(8,'Babycare','','2020-06-23 16:50:37');
/*!40000 ALTER TABLE `category` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `latereturn`
--

DROP TABLE IF EXISTS `latereturn`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `latereturn` (
  `lateorderid` int NOT NULL AUTO_INCREMENT,
  `orderid` int NOT NULL,
  `actual_returndate` datetime NOT NULL,
  `fine_latereturn` int DEFAULT NULL,
  `actual_price` decimal(10,0) NOT NULL,
  PRIMARY KEY (`lateorderid`,`orderid`),
  KEY `orderid` (`orderid`),
  CONSTRAINT `latereturn_ibfk_1` FOREIGN KEY (`orderid`) REFERENCES `rental_order` (`orderid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `latereturn`
--

LOCK TABLES `latereturn` WRITE;
/*!40000 ALTER TABLE `latereturn` DISABLE KEYS */;
/*!40000 ALTER TABLE `latereturn` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `order`
--

DROP TABLE IF EXISTS `order`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `order` (
  `orderid` int NOT NULL,
  `order_date` datetime NOT NULL,
  `total_price` decimal(10,0) NOT NULL,
  `userid` int NOT NULL,
  PRIMARY KEY (`orderid`,`userid`),
  KEY `userid` (`userid`),
  CONSTRAINT `order_ibfk_1` FOREIGN KEY (`userid`) REFERENCES `user` (`userid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `order`
--

LOCK TABLES `order` WRITE;
/*!40000 ALTER TABLE `order` DISABLE KEYS */;
INSERT INTO `order` VALUES (1,'2020-06-19 03:24:34',2000,14),(2,'2020-06-19 03:26:07',2000,14),(3,'2020-06-19 03:27:38',2000,14),(4,'2020-06-19 03:28:46',2000,14),(12,'2020-06-19 03:29:15',2000,14),(16,'2020-06-19 03:29:45',2000,14),(18,'2020-06-19 03:31:54',2000,14),(20,'2020-06-19 03:33:11',2000,14),(21,'2020-06-19 03:33:40',2000,14),(21,'2020-06-19 15:27:36',2000,15),(23,'2020-06-19 15:29:03',2000,15),(24,'2020-06-19 15:31:40',2000,15),(25,'2020-06-19 15:34:02',2000,15),(26,'2020-06-19 15:46:03',2000,15),(27,'2020-06-19 19:40:44',2000,1),(27,'2020-06-19 18:35:06',2000,5),(27,'2020-06-19 15:47:19',2000,15),(1972,'2020-06-19 20:06:12',2000,5),(4609,'2020-06-19 21:21:52',2000,1),(8128,'2020-06-19 20:07:57',2000,1),(9736,'2020-06-19 20:05:01',2000,5),(72166,'2020-06-29 16:40:10',1062,1),(88202,'2020-06-19 20:17:11',2000,1),(158328,'2020-06-19 22:01:31',4354,5),(208456,'2020-06-22 00:52:00',35,1),(315523,'2020-06-19 21:57:48',2000,5),(533720,'2020-06-19 22:01:33',4354,5),(616647,'2020-06-19 21:57:52',2000,5),(756202,'2020-07-03 00:45:06',2832,1),(766033,'2020-06-29 16:51:09',826,1),(869331,'2020-06-19 21:57:53',2000,5),(926451,'2020-06-19 21:57:50',2000,5);
/*!40000 ALTER TABLE `order` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ordered_product`
--

DROP TABLE IF EXISTS `ordered_product`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `ordered_product` (
  `ordproductid` int NOT NULL AUTO_INCREMENT,
  `orderid` int NOT NULL,
  `productid` int NOT NULL,
  `quantity` int NOT NULL,
  PRIMARY KEY (`ordproductid`),
  KEY `orderid` (`orderid`),
  KEY `productid` (`productid`),
  CONSTRAINT `ordered_product_ibfk_1` FOREIGN KEY (`orderid`) REFERENCES `order` (`orderid`),
  CONSTRAINT `ordered_product_ibfk_2` FOREIGN KEY (`productid`) REFERENCES `product` (`productid`)
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ordered_product`
--

LOCK TABLES `ordered_product` WRITE;
/*!40000 ALTER TABLE `ordered_product` DISABLE KEYS */;
INSERT INTO `ordered_product` VALUES (1,27,1,1),(2,88202,3,1),(3,88202,1,1),(4,88202,9,1),(5,315523,4,1),(6,315523,5,1),(7,926451,10,1),(8,208456,5,1),(9,208456,16,1),(10,208456,20,1),(11,766033,20,1),(12,766033,10,8);
/*!40000 ALTER TABLE `ordered_product` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `post`
--

DROP TABLE IF EXISTS `post`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `post` (
  `id` int NOT NULL AUTO_INCREMENT,
  `title` varchar(100) NOT NULL,
  `date_posted` datetime NOT NULL,
  `content` text NOT NULL,
  `author` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `author` (`author`),
  CONSTRAINT `post_ibfk_1` FOREIGN KEY (`author`) REFERENCES `user` (`userid`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `post`
--

LOCK TABLES `post` WRITE;
/*!40000 ALTER TABLE `post` DISABLE KEYS */;
INSERT INTO `post` VALUES (3,'“I always overhear aunties at weddings saying\"','2020-06-27 22:47:44','“I always overhear aunties at weddings saying\"“I always overhear aunties at weddings saying\"\r\n“I always overhear aunties at weddings saying\"\r\n“I always overhear aunties at weddings saying\"\r\n“I always overhear aunties at weddings saying\"',16);
/*!40000 ALTER TABLE `post` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `producer_product`
--

DROP TABLE IF EXISTS `producer_product`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `producer_product` (
  `producerid` int NOT NULL,
  `productid` int NOT NULL,
  `created_on` datetime NOT NULL,
  PRIMARY KEY (`producerid`,`productid`),
  KEY `productid` (`productid`),
  CONSTRAINT `producer_product_ibfk_1` FOREIGN KEY (`producerid`) REFERENCES `user` (`userid`),
  CONSTRAINT `producer_product_ibfk_2` FOREIGN KEY (`productid`) REFERENCES `product` (`productid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `producer_product`
--

LOCK TABLES `producer_product` WRITE;
/*!40000 ALTER TABLE `producer_product` DISABLE KEYS */;
INSERT INTO `producer_product` VALUES (1,4,'2020-04-19 16:09:15'),(1,5,'2020-04-19 16:09:58'),(1,6,'2020-04-19 16:11:25'),(1,20,'2020-06-29 16:37:59'),(2,1,'2020-04-19 14:50:17'),(2,3,'2020-04-19 14:59:58'),(2,7,'2020-04-19 18:26:16'),(2,8,'2020-04-19 18:31:52'),(2,9,'2020-04-19 19:22:05'),(2,10,'2020-04-19 19:31:28'),(2,11,'2020-04-19 19:52:46'),(2,12,'2020-04-28 00:42:27'),(2,15,'2020-06-22 02:42:25'),(3,21,'2020-07-03 04:26:26'),(5,16,'2020-06-23 16:54:28'),(5,19,'2020-06-23 17:01:31'),(16,14,'2020-06-22 02:00:09'),(20,22,'2020-07-04 19:02:54');
/*!40000 ALTER TABLE `producer_product` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `product`
--

DROP TABLE IF EXISTS `product`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `product` (
  `productid` int NOT NULL AUTO_INCREMENT,
  `sku` varchar(50) NOT NULL,
  `product_name` varchar(100) NOT NULL,
  `description` varchar(100) NOT NULL,
  `image` varchar(100) NOT NULL,
  `quantity` int NOT NULL,
  `regular_price` decimal(10,0) DEFAULT NULL,
  `discounted_price` decimal(10,0) DEFAULT NULL,
  `product_rating` decimal(10,0) DEFAULT NULL,
  `product_review` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`productid`)
) ENGINE=InnoDB AUTO_INCREMENT=23 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `product`
--

LOCK TABLES `product` WRITE;
/*!40000 ALTER TABLE `product` DISABLE KEYS */;
INSERT INTO `product` VALUES (1,'15','Oraganic carrots','Spinach','8229f28846cbaba5.png',198,20,15,0,'available'),(3,'12','Papaya','Papaya','5effd8aff138e0be.png',48,20,15,0,'available'),(4,'6','Beans','Beans','b24b4b5a2032b413.png',499,20,15,0,'available'),(5,'21','chillies','chillies','b2017257b32fb642.png',17,30,15,0,'available'),(6,'15','Oraganic Eggs','Oraganic Eggs','e20b113ad806ba09.png',225,80,15,0,'available'),(7,'12','Watermelon','Watermelon','da07eea7d2a94dde.png',100,12,15,0,'available'),(8,'12','Ragi millets','Ragi millets','7ea45d123fc83808.png',120,400,15,0,'available'),(9,'13','Banana','Banana','09b2ad84b491e0f3.png',19,30,15,0,'available'),(10,'12','Chocalate cake','Chocalate cake','da657b58c171c1ae.png',0,300,15,0,'available'),(11,'12','muskmelon','muskmelon','2a97dc93ac2ddc4a.png',200,30,15,0,'available'),(12,'13','Oraganic Beans','Oraganic Beans','f263b756454f8e32.png',45,30,15,0,'available'),(14,'15','Vicks vaporub','Vicks vaporub','e82c38facf44df26.png',20,50,15,0,'available'),(15,'24','Wheat','Wheat','2e5d2329c236c0a8.png',100,56,15,0,'available'),(16,'15','baby powder','baby powder','4f2b1682139b8d01.png',299,200,15,0,'available'),(19,'12','Mango icecream','mango icecream','e029e56ada5494b6.png',20,400,15,0,'available'),(20,'23','Baby bicycle','Bicycle for kids of age 4','2afbdce170f03cfb.jpg',-2,700,15,0,'Out of stock'),(21,'34','Face_masks','Face_masks','a817ff73af5fde16.png',200,300,15,0,'Price per piece'),(22,'45','Moneyplant','Money plant very good for health n wealth','3f42659ed463cd3c.jpg',2,10,15,0,'Price per piece');
/*!40000 ALTER TABLE `product` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `product_category`
--

DROP TABLE IF EXISTS `product_category`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `product_category` (
  `categoryid` int NOT NULL,
  `productid` int NOT NULL,
  `created_on` datetime NOT NULL,
  PRIMARY KEY (`categoryid`,`productid`),
  KEY `productid` (`productid`),
  CONSTRAINT `product_category_ibfk_1` FOREIGN KEY (`categoryid`) REFERENCES `category` (`categoryid`),
  CONSTRAINT `product_category_ibfk_2` FOREIGN KEY (`productid`) REFERENCES `product` (`productid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `product_category`
--

LOCK TABLES `product_category` WRITE;
/*!40000 ALTER TABLE `product_category` DISABLE KEYS */;
INSERT INTO `product_category` VALUES (1,1,'2020-04-19 14:50:17'),(1,4,'2020-04-19 16:09:15'),(1,5,'2020-04-19 16:09:57'),(1,12,'2020-04-28 00:42:26'),(1,15,'2020-06-22 02:42:24'),(1,19,'2020-06-23 17:06:35'),(1,22,'2020-07-04 19:02:54'),(2,10,'2020-04-19 19:31:27'),(3,3,'2020-04-19 14:59:58'),(3,7,'2020-04-19 18:26:16'),(3,9,'2020-04-19 19:22:05'),(3,11,'2020-04-19 19:52:46'),(4,6,'2020-04-19 16:11:25'),(7,14,'2020-06-22 02:00:08'),(8,16,'2020-06-23 16:54:28'),(8,20,'2020-06-29 16:37:59'),(8,21,'2020-07-03 04:26:26');
/*!40000 ALTER TABLE `product_category` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `rental_cart`
--

DROP TABLE IF EXISTS `rental_cart`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `rental_cart` (
  `userid` int NOT NULL,
  `productid` int NOT NULL,
  `quantity` int NOT NULL,
  `days` int NOT NULL,
  PRIMARY KEY (`userid`,`productid`),
  KEY `productid` (`productid`),
  CONSTRAINT `rental_cart_ibfk_1` FOREIGN KEY (`userid`) REFERENCES `user` (`userid`),
  CONSTRAINT `rental_cart_ibfk_2` FOREIGN KEY (`productid`) REFERENCES `rental_product` (`productid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `rental_cart`
--

LOCK TABLES `rental_cart` WRITE;
/*!40000 ALTER TABLE `rental_cart` DISABLE KEYS */;
INSERT INTO `rental_cart` VALUES (2,2,1,2),(15,5,1,4);
/*!40000 ALTER TABLE `rental_cart` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `rental_category`
--

DROP TABLE IF EXISTS `rental_category`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `rental_category` (
  `categoryid` int NOT NULL AUTO_INCREMENT,
  `category_name` varchar(100) NOT NULL,
  `category_image` varchar(200) NOT NULL,
  PRIMARY KEY (`categoryid`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `rental_category`
--

LOCK TABLES `rental_category` WRITE;
/*!40000 ALTER TABLE `rental_category` DISABLE KEYS */;
INSERT INTO `rental_category` VALUES (1,'Tractor and Loaders',''),(2,'cleaning',''),(3,'land preparation',''),(4,'harvesting',''),(5,'Sprayers',''),(6,'cleaning','');
/*!40000 ALTER TABLE `rental_category` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `rental_order`
--

DROP TABLE IF EXISTS `rental_order`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `rental_order` (
  `orderid` int NOT NULL AUTO_INCREMENT,
  `rentalproductid` int NOT NULL,
  `userid` int NOT NULL,
  `rentalorder_date` datetime NOT NULL,
  `rentalreturn_date` datetime NOT NULL,
  `total_price` decimal(10,0) NOT NULL,
  `rental_status` int NOT NULL,
  PRIMARY KEY (`orderid`,`rentalproductid`,`userid`),
  KEY `rentalproductid` (`rentalproductid`),
  KEY `userid` (`userid`),
  CONSTRAINT `rental_order_ibfk_1` FOREIGN KEY (`rentalproductid`) REFERENCES `rental_product` (`productid`),
  CONSTRAINT `rental_order_ibfk_2` FOREIGN KEY (`userid`) REFERENCES `user` (`userid`)
) ENGINE=InnoDB AUTO_INCREMENT=18 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `rental_order`
--

LOCK TABLES `rental_order` WRITE;
/*!40000 ALTER TABLE `rental_order` DISABLE KEYS */;
INSERT INTO `rental_order` VALUES (1,1,12,'2020-05-23 00:00:00','2020-05-30 00:00:00',14000,1),(2,1,12,'2020-05-23 00:00:00','2020-05-30 00:00:00',14000,1),(3,1,14,'2020-06-17 00:00:00','2020-06-26 00:00:00',18000,0),(4,2,3,'2020-06-18 00:00:00','2020-06-20 00:00:00',2000,0),(5,4,14,'2020-06-24 00:00:00','2020-06-30 00:00:00',8000,1),(6,4,14,'2020-06-25 00:00:00','2020-06-30 00:00:00',5000,0),(7,4,14,'2020-06-25 00:00:00','2020-06-30 00:00:00',5000,0),(8,1,14,'2020-06-25 00:00:00','2020-06-27 00:00:00',4000,0),(9,3,14,'2020-06-21 00:00:00','2020-06-30 00:00:00',17500,0),(10,5,15,'2020-06-26 00:00:00','2020-06-30 00:00:00',4000,0),(11,2,2,'2020-06-25 00:00:00','2020-06-27 00:00:00',2000,0),(12,2,2,'2020-06-26 00:00:00','2020-06-30 00:00:00',4000,0),(13,5,5,'2020-06-29 00:00:00','2020-06-30 00:00:00',5000,0),(14,5,3,'2020-06-26 00:00:00','2020-06-30 00:00:00',4000,0),(15,2,3,'2020-06-20 00:00:00','2020-06-25 00:00:00',5000,0),(16,2,5,'2020-06-30 00:00:00','2020-07-04 00:00:00',4000,0),(17,2,5,'2020-06-26 00:00:00','2020-06-30 00:00:00',4000,0);
/*!40000 ALTER TABLE `rental_order` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `rental_ordered_product`
--

DROP TABLE IF EXISTS `rental_ordered_product`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `rental_ordered_product` (
  `ordproductid` int NOT NULL AUTO_INCREMENT,
  `orderid` int NOT NULL,
  `productid` int NOT NULL,
  `quantity` int NOT NULL,
  PRIMARY KEY (`ordproductid`),
  KEY `orderid` (`orderid`),
  KEY `productid` (`productid`),
  CONSTRAINT `rental_ordered_product_ibfk_1` FOREIGN KEY (`orderid`) REFERENCES `rental_order` (`orderid`),
  CONSTRAINT `rental_ordered_product_ibfk_2` FOREIGN KEY (`productid`) REFERENCES `rental_product` (`productid`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `rental_ordered_product`
--

LOCK TABLES `rental_ordered_product` WRITE;
/*!40000 ALTER TABLE `rental_ordered_product` DISABLE KEYS */;
/*!40000 ALTER TABLE `rental_ordered_product` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `rental_producer_product`
--

DROP TABLE IF EXISTS `rental_producer_product`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `rental_producer_product` (
  `producerid` int NOT NULL,
  `productid` int NOT NULL,
  PRIMARY KEY (`producerid`,`productid`),
  KEY `productid` (`productid`),
  CONSTRAINT `rental_producer_product_ibfk_1` FOREIGN KEY (`producerid`) REFERENCES `user` (`userid`),
  CONSTRAINT `rental_producer_product_ibfk_2` FOREIGN KEY (`productid`) REFERENCES `rental_product` (`productid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `rental_producer_product`
--

LOCK TABLES `rental_producer_product` WRITE;
/*!40000 ALTER TABLE `rental_producer_product` DISABLE KEYS */;
INSERT INTO `rental_producer_product` VALUES (2,1),(2,2),(2,3),(2,4),(5,5),(5,6),(5,7),(5,8),(5,9);
/*!40000 ALTER TABLE `rental_producer_product` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `rental_product`
--

DROP TABLE IF EXISTS `rental_product`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `rental_product` (
  `productid` int NOT NULL AUTO_INCREMENT,
  `product_name` varchar(100) NOT NULL,
  `description` varchar(100) NOT NULL,
  `image` varchar(100) NOT NULL,
  `quantity` int NOT NULL,
  `price_scale` varchar(100) DEFAULT NULL,
  `regular_price` decimal(10,0) DEFAULT NULL,
  `product_rating` decimal(10,0) DEFAULT NULL,
  `product_review` varchar(100) DEFAULT NULL,
  `city` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`productid`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `rental_product`
--

LOCK TABLES `rental_product` WRITE;
/*!40000 ALTER TABLE `rental_product` DISABLE KEYS */;
INSERT INTO `rental_product` VALUES (1,'Tractor','Tractor Tractor TractorTractor','b9fe420c38397fc0.png',1,'Price/hour',2000,0,'','Chitradurga'),(2,'Golf cart','Golf cart','c1bf81d9c7c5f480.png',1,'Price/day',1000,0,'','Chitradurga'),(3,'Excavator','Excavator','98d83266b7874374.png',1,'Price/day',1500,0,'','Chitradurga'),(4,'Carpet cleaner','Carpet cleaner','034b7f1f27c42dd6.png',20,'Price/hour',1000,0,'','Chitradurga'),(5,'Small-breaker','Small-breaker','14920859cda7af80.png',1,'Price/day',1000,0,'','Davanagere'),(6,'Bicycle','Bicycle','',1,'Price/hour',5,0,'','novi'),(7,'Bicycle','Bicycle','',1,'Price/hour',5,0,'','novi'),(8,'Bicycle','Bicycle','',1,'Price/hour',5,0,'','novi'),(9,'Oraganic bicycle','Oraganic bicycle','',20,'Price/hour',15,0,'','Chitradurga');
/*!40000 ALTER TABLE `rental_product` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `rental_product_category`
--

DROP TABLE IF EXISTS `rental_product_category`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `rental_product_category` (
  `categoryid` int NOT NULL,
  `productid` int NOT NULL,
  PRIMARY KEY (`categoryid`,`productid`),
  KEY `productid` (`productid`),
  CONSTRAINT `rental_product_category_ibfk_1` FOREIGN KEY (`categoryid`) REFERENCES `rental_category` (`categoryid`),
  CONSTRAINT `rental_product_category_ibfk_2` FOREIGN KEY (`productid`) REFERENCES `rental_product` (`productid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `rental_product_category`
--

LOCK TABLES `rental_product_category` WRITE;
/*!40000 ALTER TABLE `rental_product_category` DISABLE KEYS */;
INSERT INTO `rental_product_category` VALUES (1,1),(1,2),(1,3),(2,4),(2,5),(1,6),(1,7),(1,8),(1,9);
/*!40000 ALTER TABLE `rental_product_category` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sale_transaction`
--

DROP TABLE IF EXISTS `sale_transaction`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `sale_transaction` (
  `transactionid` int NOT NULL AUTO_INCREMENT,
  `orderid` int NOT NULL,
  `transaction_date` datetime NOT NULL,
  `amount` decimal(10,0) NOT NULL,
  `cc_number` varchar(50) NOT NULL,
  `cc_type` varchar(50) NOT NULL,
  `response` varchar(50) NOT NULL,
  PRIMARY KEY (`transactionid`),
  KEY `orderid` (`orderid`),
  CONSTRAINT `sale_transaction_ibfk_1` FOREIGN KEY (`orderid`) REFERENCES `order` (`orderid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sale_transaction`
--

LOCK TABLES `sale_transaction` WRITE;
/*!40000 ALTER TABLE `sale_transaction` DISABLE KEYS */;
/*!40000 ALTER TABLE `sale_transaction` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user`
--

DROP TABLE IF EXISTS `user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `user` (
  `userid` int NOT NULL AUTO_INCREMENT,
  `fname` varchar(20) NOT NULL,
  `lname` varchar(30) NOT NULL,
  `password` varchar(60) NOT NULL,
  `address1` varchar(30) NOT NULL,
  `address2` varchar(20) NOT NULL,
  `city` varchar(20) NOT NULL,
  `state` varchar(20) NOT NULL,
  `country` varchar(20) NOT NULL,
  `zipcode` varchar(20) NOT NULL,
  `email` varchar(120) NOT NULL,
  `phone` varchar(20) NOT NULL,
  `isadmin` int NOT NULL,
  `image_file` varchar(200) NOT NULL,
  `farmdescription` varchar(500) NOT NULL,
  PRIMARY KEY (`userid`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user`
--

LOCK TABLES `user` WRITE;
/*!40000 ALTER TABLE `user` DISABLE KEYS */;
INSERT INTO `user` VALUES (1,'Guestuser609','guest609','084e0343a0486ff05530df6c705c8bb4','','','','','','','guestuser@gmail.com','',1,'6952a3c1c363fd28.jpg','Oraganic farm'),(2,'Manjula','Thimmareddy','ab64f5c1af67e191fb34d5b3f87c7902','10','Mahadevapura','Dispur','Assam','India','781005','manjujnv87@gmail.com','09986317317',1,'lady.png','Amid the wheat, amid the soft golden ears, moves the unseen wind. It moves my hair and sea of summer grass all the same. In these moments on the farm there is an eternity in each second, a joy that comes in the free birdsong and a steadiness to my heart and soul. And supporting all this is the humble Earth, that sweet rich brown that brings all this in concert with the sunshine. If I could wish for peace within this human body and all around, I could wish for no more.'),(3,'ravichandra','sereddy thipperudra reddy','63dd3e154ca6d948fc380fa576343ba6','450 S Peachtree pkwy','12','Chitradurga','Karnataka','India','56001','ravichandra.s.t@gmail.com','2623665056',1,'default.jpg','Oraganic farm'),(5,'rishik','shereddy','ab64f5c1af67e191fb34d5b3f87c7902','22587, Grove court','apt 102','Davanagere','Michigan','USA','90001','rishi@gmail.com','2623665056',1,'default.jpg','Oraganic farm'),(6,'SrinivasBhatt','Bhatt','97f974881b3726d9a77014b5f3b4d795','Mahadevapura','apt 102','Davanagere','Karnataka','India','781030','Srinivas@gmail.com','9008145345',1,'default.jpg','Oraganic farm'),(8,'amit','guest','084e0343a0486ff05530df6c705c8bb4','12 Jogimmati road','','Chitradurga','Karnataka','India','560034','amith@gmail.com','09986317318',999,'default.jpg','Oraganic farm'),(9,'shanti','guest','084e0343a0486ff05530df6c705c8bb4','34 Hiriyur 1st ccross','','Chitradurga','Karnataka','India','560034','shanti@gmail.com','8907896789',999,'default.jpg','Oraganic farm'),(10,'Guestuser609','guest','084e0343a0486ff05530df6c705c8bb4','15 dfjd','','Davanagere','Karnataka','India','781030','shiva@gmail.com','234567891',0,'6952a3c1c363fd28.jpg','Oraganic farm'),(11,'Guestuser609','guest','084e0343a0486ff05530df6c705c8bb4','22587 Grove court','','Bangalore','Karnataka','India','560001','lakshmi','2623665056',0,'6952a3c1c363fd28.jpg','Oraganic farm'),(12,'Guestuser609','guest','084e0343a0486ff05530df6c705c8bb4','12 Jogimmati road','','Chitradurga','Karnataka','India','577501','shashi@gmail.com','7890678906',0,'6952a3c1c363fd28.jpg','Oraganic farm'),(13,'Ravi','chandra','63dd3e154ca6d948fc380fa576343ba6','12 Jogimmati road','13','Chitradurga','Karnataka','India','577501','ravi@gmail.com','09986317318',0,'default.jpg','Oraganic farm'),(14,'ragini','bhatt','ac89a6101052100115630285edc36201','12 Jogimmati road','134','Davanagere','Karnataka','India','781030','ragini@gmail.com','09986345567',0,'default.jpg','Oraganic farm'),(15,'Lakshmi','reddy','1eaf7c068a250a38e3bab770053c14c3','12 Jogimmati road','134','Bangalore','Karnataka','India','560002','lakshmi@gmail.com','2623665089',0,'default.jpg','Oraganic farm'),(16,'aaru','pavan','e492b5418a7e12e3a64d7cef8e05510e','1 Jogimmati ','5th cross','Chitradurga','Karnataka','India','560034','aaru@gmail.com','34546576776',1,'6952a3c1c363fd28.jpg','Oraganic farm'),(17,'Manjula','Manjula','86f9ab6653b3b0151eef76b46ba2f9a5','10','Mahadevapura','Chitradurga','Karnataka','India','560034','manju@gmail.com','09986317317',2,'6952a3c1c363fd28.jpg','Oraganic farm'),(18,'Manjula','Manjula','a455598b821ac98fcccdcb395f541aed','10','Mahadevapura','Chitradurga','Karnataka','India','577501','lanju@gmail.com','09986317317',0,'338841ae27d0d84e.png','Oraganic farm'),(19,'ravichandra','ravichandra','9f42d5bdf1f00206df4b9093048d61b3','450 S Peachtree pkwy','23','Chitradurga','Karnataka','India','577501','chanda.s.t@gmail.com','2623665056',0,'chanda.s.t@gmail.com.png','Oraganic farm'),(20,'Rishik','Shereddy','ac4b0a568e8d3a14b521eae07006bc95','22587 Grove Ct','Apt102','Los Angeles','Michigan','USA','90001','Rishik2014@gmail.com','2456896534',1,'Rishik2014@gmail.com.jpg','Oraganic farm');
/*!40000 ALTER TABLE `user` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2020-07-07 22:59:46
