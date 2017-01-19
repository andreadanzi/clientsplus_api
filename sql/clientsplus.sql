-- --------------------------------------------------------
-- Host:                         10.88.102.73
-- Versione server:              5.7.17 - MySQL Community Server (GPL)
-- S.O. server:                  Linux
-- HeidiSQL Versione:            9.1.0.4867
-- --------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8mb4 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;

-- Dump della struttura del database clientsplus
CREATE DATABASE IF NOT EXISTS `clientsplus` /*!40100 DEFAULT CHARACTER SET utf8 */;
USE `clientsplus`;


-- Dump della struttura di tabella clientsplus.datastructure
CREATE TABLE IF NOT EXISTS `datastructure` (
  `iddatastructure` int(11) NOT NULL AUTO_INCREMENT,
  `event_types_idevent_types` int(11) NOT NULL,
  `name` varchar(45) DEFAULT NULL,
  `type` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`iddatastructure`),
  KEY `fk_datastructure_event_types_idx` (`event_types_idevent_types`),
  CONSTRAINT `fk_datastructure_event_types` FOREIGN KEY (`event_types_idevent_types`) REFERENCES `event_types` (`idevent_types`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- L’esportazione dei dati non era selezionata.


-- Dump della struttura di tabella clientsplus.email
CREATE TABLE IF NOT EXISTS `email` (
  `idemail` int(11) NOT NULL AUTO_INCREMENT,
  `email_address` varchar(255) NOT NULL,
  `import_status` int(11) NOT NULL,
  `import_relations` text,
  `timestamp` datetime DEFAULT NULL,
  `import_date` datetime DEFAULT NULL,
  PRIMARY KEY (`idemail`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- L’esportazione dei dati non era selezionata.


-- Dump della struttura di tabella clientsplus.event_types
CREATE TABLE IF NOT EXISTS `event_types` (
  `idevent_types` int(11) NOT NULL AUTO_INCREMENT,
  `event_type_code` varchar(45) NOT NULL,
  `timestamp` datetime DEFAULT NULL,
  PRIMARY KEY (`idevent_types`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- L’esportazione dei dati non era selezionata.


-- Dump della struttura di tabella clientsplus.message
CREATE TABLE IF NOT EXISTS `message` (
  `idmessage` int(11) NOT NULL AUTO_INCREMENT,
  `intdate` int(11) DEFAULT NULL,
  `datetime` varchar(45) DEFAULT NULL,
  `email_address` varchar(45) DEFAULT NULL,
  `event_type_code` varchar(45) DEFAULT NULL,
  `datastructure_name` varchar(45) DEFAULT NULL,
  `datastructure_value` varchar(1024) DEFAULT NULL,
  `event_types_idevent_types` int(11) NOT NULL,
  `datastructure_iddatastructure` int(11) NOT NULL,
  `email_idemail` int(11) NOT NULL,
  `message_log_idmessage_log` int(11) NOT NULL,
  PRIMARY KEY (`idmessage`),
  KEY `fk_message_event_types1_idx` (`event_types_idevent_types`),
  KEY `fk_message_datastructure1_idx` (`datastructure_iddatastructure`),
  KEY `fk_message_email1_idx` (`email_idemail`),
  KEY `fk_message_message_log1` (`message_log_idmessage_log`),
  CONSTRAINT `fk_message_datastructure1` FOREIGN KEY (`datastructure_iddatastructure`) REFERENCES `datastructure` (`iddatastructure`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_message_email1` FOREIGN KEY (`email_idemail`) REFERENCES `email` (`idemail`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_message_event_types1` FOREIGN KEY (`event_types_idevent_types`) REFERENCES `event_types` (`idevent_types`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_message_message_log1` FOREIGN KEY (`message_log_idmessage_log`) REFERENCES `message_log` (`idmessage_log`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- L’esportazione dei dati non era selezionata.


-- Dump della struttura di tabella clientsplus.message_log
CREATE TABLE IF NOT EXISTS `message_log` (
  `idmessage_log` int(11) NOT NULL AUTO_INCREMENT,
  `timestamp` datetime DEFAULT NULL,
  `hashstring` varchar(1024) DEFAULT NULL,
  `by_email` varchar(255) NOT NULL,
  `when_timestamp` int(11) NOT NULL,
  `type_event` varchar(255) NOT NULL,
  `import_status` int(11) NOT NULL,
  `import_date` datetime NOT NULL,
  `payload` text,
  PRIMARY KEY (`idmessage_log`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- L’esportazione dei dati non era selezionata.
/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IF(@OLD_FOREIGN_KEY_CHECKS IS NULL, 1, @OLD_FOREIGN_KEY_CHECKS) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
