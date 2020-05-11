-- MySQL dump 10.13  Distrib 5.7.29, for Linux (x86_64)
--
-- Host: localhost    Database: timeTablingDb
-- ------------------------------------------------------
-- Server version	5.7.29

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `assignment`
--

DROP TABLE IF EXISTS `assignment`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `assignment` (
  `periodId` varchar(36) NOT NULL,
  `roomId` varchar(36) NOT NULL,
  `examId` varchar(45) DEFAULT NULL,
  KEY `fk_assignment_2_idx` (`roomId`),
  KEY `fk_assignment_3_idx` (`examId`),
  KEY `fk_assignment_1` (`periodId`),
  CONSTRAINT `fk_assignment_1` FOREIGN KEY (`periodId`) REFERENCES `periods` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_assignment_2` FOREIGN KEY (`roomId`) REFERENCES `rooms` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_assignment_3` FOREIGN KEY (`examId`) REFERENCES `exams` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `assignment`
--

LOCK TABLES `assignment` WRITE;
/*!40000 ALTER TABLE `assignment` DISABLE KEYS */;
/*!40000 ALTER TABLE `assignment` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `examPeriodRelation`
--

DROP TABLE IF EXISTS `examPeriodRelation`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `examPeriodRelation` (
  `examId` varchar(36) NOT NULL,
  `periodId` varchar(36) NOT NULL,
  KEY `fk_examPeriodRelation_2_idx` (`periodId`),
  KEY `fk_examPeriodRelation_1` (`examId`),
  CONSTRAINT `fk_examPeriodRelation_1` FOREIGN KEY (`examId`) REFERENCES `exams` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_examPeriodRelation_2` FOREIGN KEY (`periodId`) REFERENCES `periods` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `examPeriodRelation`
--

LOCK TABLES `examPeriodRelation` WRITE;
/*!40000 ALTER TABLE `examPeriodRelation` DISABLE KEYS */;
/*!40000 ALTER TABLE `examPeriodRelation` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `examRoomRelation`
--

DROP TABLE IF EXISTS `examRoomRelation`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `examRoomRelation` (
  `examId` varchar(36) NOT NULL,
  `roomId` varchar(36) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `examRoomRelation`
--

LOCK TABLES `examRoomRelation` WRITE;
/*!40000 ALTER TABLE `examRoomRelation` DISABLE KEYS */;
/*!40000 ALTER TABLE `examRoomRelation` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `exams`
--

DROP TABLE IF EXISTS `exams`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `exams` (
  `id` varchar(36) NOT NULL,
  `length` int(11) DEFAULT NULL,
  `alt` varchar(5) DEFAULT NULL,
  `minSize` int(11) DEFAULT '0',
  `maxRooms` int(11) DEFAULT NULL,
  `average` int(11) DEFAULT NULL,
  `examCode` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `exams`
--

LOCK TABLES `exams` WRITE;
/*!40000 ALTER TABLE `exams` DISABLE KEYS */;
INSERT INTO `exams` VALUES ('1',120,'False',217,2,1,'CAT 152'),('10',120,'False',850,5,1,'CSM 152'),('11',120,'False',100,1,1,'CSM 184'),('12',120,'False',31,1,1,'CSM 184'),('13',120,'False',790,4,1,'ECON 152'),('14',120,'False',174,1,1,'ECON 154'),('15',120,'False',95,1,1,'ENGL 152'),('16',120,'False',108,1,1,'ENGL 158'),('17',120,'False',60,1,1,'ENGL 164'),('18',120,'False',6,1,1,'ENGL 166'),('19',120,'False',32,1,1,'FC 182'),('2',120,'False',394,2,1,'CAT 154'),('20',120,'False',15,1,1,'FERF 152'),('21',120,'False',12,1,1,'FREF 154'),('22',120,'False',248,2,1,'FREF 156'),('23',120,'False',87,1,1,'GEOG 152'),('24',120,'False',171,1,1,'GEOG 154'),('25',120,'False',80,1,1,'GEOG 156'),('26',120,'False',9,1,1,'HIS 154'),('27',120,'False',55,1,1,'HIST 152'),('28',120,'False',29,1,1,'HIST 156'),('29',120,'False',112,1,1,'LING 152'),('3',120,'False',497,3,1,'CECAST COURSE'),('30',120,'False',100,1,1,'LING 154'),('31',120,'False',850,5,1,'MATH 154'),('32',120,'False',6,1,1,'POL 152'),('33',120,'False',38,1,1,'POL 156'),('34',120,'False',22,1,1,'RS 152'),('35',120,'False',29,1,1,'RS 154'),('36',120,'False',19,1,1,'RS 156'),('37',120,'False',4,1,1,'SOC 152'),('38',120,'False',182,1,1,'SOC 154'),('39',120,'False',59,1,1,'SOWK 156'),('4',120,'False',309,2,1,'CHIN 102'),('40',120,'False',70,1,1,'SOWK 158'),('41',125,'True',21,2,10,'CAT 151'),('42',125,'True',21,2,10,'IRAI ALL'),('5',120,'False',80,1,1,'CHIN 104'),('6',120,'False',800,4,1,'CHIN 106'),('7',120,'False',107,1,1,'COMS 152'),('8',120,'False',900,5,1,'COMS 154'),('9',120,'False',120,1,1,'COMS 156');
/*!40000 ALTER TABLE `exams` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `periods`
--

DROP TABLE IF EXISTS `periods`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `periods` (
  `id` varchar(36) NOT NULL,
  `length` int(11) NOT NULL,
  `day` varchar(20) NOT NULL,
  `time` varchar(20) NOT NULL,
  `penalty` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id_UNIQUE` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `periods`
--

LOCK TABLES `periods` WRITE;
/*!40000 ALTER TABLE `periods` DISABLE KEYS */;
INSERT INTO `periods` VALUES ('1',180,'2020-04-05 00:00:00','8.00am-11.00am',0),('10',180,'2020-07-05 00:00:00','8.00am-11.00am',0),('11',180,'2020-07-05 00:00:00','11.30am-2.30pm',0),('12',180,'2020-07-05 00:00:00','3.00pm-6.00pm',0),('13',180,'2020-08-05 00:00:00','8.00am-11.00am',0),('14',180,'2020-08-05 00:00:00','11.30am-2.30pm',0),('15',180,'2020-08-05 00:00:00','3.00pm-6.00pm',0),('16',180,'2020-09-05 00:00:00','8.00am-11.00am',0),('17',180,'2020-09-05 00:00:00','11.30am-2.30pm',0),('18',180,'2020-09-05 00:00:00','3.00pm-6.00pm',0),('19',180,'2020-10-05 00:00:00','8.00am-11.00am',0),('2',180,'2020-04-05 00:00:00','11.30am-2.30pm',1),('20',180,'2020-10-05 00:00:00','11.30am-2.30pm',0),('21',180,'2020-10-05 00:00:00','3.00pm-6.00pm',0),('3',180,'2020-04-05 00:00:00','3.00pm-6.00pm',0),('4',180,'2020-05-05 00:00:00','8.00am-11.00am',0),('5',180,'2020-05-05 00:00:00','11.30am-2.30pm',0),('6',180,'2020-05-05 00:00:00','3.00pm-6.00pm',0),('7',180,'2020-06-05 00:00:00','8.00am-11.00am',0),('8',180,'2020-06-05 00:00:00','11.30am-2.30pm',0),('9',180,'2020-06-05 00:00:00','3.00pm-6.00pm',0);
/*!40000 ALTER TABLE `periods` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `roomPeriodRelation`
--

DROP TABLE IF EXISTS `roomPeriodRelation`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `roomPeriodRelation` (
  `periodId` varchar(36) NOT NULL,
  `available` tinyint(1) NOT NULL DEFAULT '1',
  `roomId` varchar(36) DEFAULT NULL,
  `penalty` int(11) DEFAULT NULL,
  KEY `fk_roomPeriodRelation_2_idx` (`roomId`),
  KEY `fk_roomPeriodRelation_11` (`periodId`),
  CONSTRAINT `fk_roomPeriodRelation_11` FOREIGN KEY (`periodId`) REFERENCES `periods` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_roomPeriodRelation_22` FOREIGN KEY (`roomId`) REFERENCES `rooms` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `roomPeriodRelation`
--

LOCK TABLES `roomPeriodRelation` WRITE;
/*!40000 ALTER TABLE `roomPeriodRelation` DISABLE KEYS */;
/*!40000 ALTER TABLE `roomPeriodRelation` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `rooms`
--

DROP TABLE IF EXISTS `rooms`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `rooms` (
  `id` varchar(36) NOT NULL,
  `roomName` varchar(45) DEFAULT NULL,
  `size` int(11) unsigned zerofill DEFAULT NULL,
  `alt` int(11) unsigned zerofill DEFAULT NULL,
  `Coord_Longitude` varchar(45) DEFAULT NULL,
  `Coord_Latitude` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `rooms_UNIQUE` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `rooms`
--

LOCK TABLES `rooms` WRITE;
/*!40000 ALTER TABLE `rooms` DISABLE KEYS */;
INSERT INTO `rooms` VALUES ('1','EHC_101',00000000200,00000000210,'-1.56799','6.67554'),('10','NB_T5',00000000200,00000000210,'-1.56837','6.66759'),('11','NB_R1',00000000100,00000000105,'-1.56837','6.66759'),('12','NB_R2',00000000100,00000000105,'-1.56837','6.66759'),('13','OLD',00000000400,00000000420,'-1.57543','6.68383'),('2','EHC_102',00000000200,00000000210,'-1.56799','6.67554'),('3','EHC_201',00000000200,00000000210,'-1.56799','6.67554'),('4','EHC_EXT_A',00000000150,00000000160,'-1.56799','6.67554'),('5','EHC_EXT_B',00000000150,00000000160,'-1.56799','6.67554'),('6','NB_T1',00000000200,00000000210,'-1.56837','6.66759'),('7','NB_T2',00000000200,00000000210,'-1.56837','6.66759'),('8','NB_T3',00000000200,00000000210,'-1.56837','6.66759'),('9','NB_T4',00000000200,00000000210,'-1.56837','6.66759');
/*!40000 ALTER TABLE `rooms` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `student`
--

DROP TABLE IF EXISTS `student`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `student` (
  `id` varchar(36) NOT NULL,
  `examId` varchar(36) DEFAULT NULL,
  `periodId` varchar(36) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_student_1_idx` (`periodId`),
  KEY `fk_student_2_idx` (`examId`),
  CONSTRAINT `fk_student_1` FOREIGN KEY (`periodId`) REFERENCES `periods` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_student_2` FOREIGN KEY (`examId`) REFERENCES `exams` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `student`
--

LOCK TABLES `student` WRITE;
/*!40000 ALTER TABLE `student` DISABLE KEYS */;
INSERT INTO `student` VALUES ('1','10','23');
/*!40000 ALTER TABLE `student` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2020-05-11 18:06:16
