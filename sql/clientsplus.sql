-- phpMyAdmin SQL Dump
-- version 4.5.4.1deb2ubuntu2
-- http://www.phpmyadmin.net
--
-- Host: localhost
-- Creato il: Dic 03, 2016 alle 09:45
-- Versione del server: 5.7.16-0ubuntu0.16.04.1
-- Versione PHP: 7.0.8-0ubuntu0.16.04.3

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `clientsplus`
--

-- --------------------------------------------------------

--
-- Struttura della tabella `message`
--

CREATE TABLE `message` (
  `idmessage` int(11) NOT NULL,
  `intdate` int(11) DEFAULT NULL,
  `datetime` varchar(45) DEFAULT NULL,
  `email_address` varchar(45) DEFAULT NULL,
  `event_type_code` varchar(45) DEFAULT NULL,
  `datastructure_name` varchar(45) DEFAULT NULL,
  `datastructure_value` varchar(45) DEFAULT NULL,
  `event_types_idevent_types` int(11) NOT NULL,
  `datastructure_iddatastructure` int(11) NOT NULL,
  `email_idemail` int(11) NOT NULL,
  `message_log_idmessage_log` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dump dei dati per la tabella `message`
--

INSERT INTO `message` (`idmessage`, `intdate`, `datetime`, `email_address`, `event_type_code`, `datastructure_name`, `datastructure_value`, `event_types_idevent_types`, `datastructure_iddatastructure`, `email_idemail`, `message_log_idmessage_log`) VALUES
(16, NULL, NULL, NULL, NULL, 'first_name', 'Andrea', 10, 21, 3, 22),
(17, NULL, NULL, NULL, NULL, 'last_name', 'Danzi', 10, 22, 3, 22),
(18, NULL, NULL, NULL, NULL, 'username', 'andrea.danzi', 10, 23, 3, 22),
(19, NULL, NULL, NULL, NULL, 'company', 'DANZI.TN', 10, 24, 3, 22),
(20, NULL, NULL, NULL, NULL, 'first_name', 'Andrea', 11, 25, 4, 23),
(21, NULL, NULL, NULL, NULL, 'last_name', 'Danzi', 11, 26, 4, 23),
(22, NULL, NULL, NULL, NULL, 'username', 'andrea.danzi', 11, 27, 4, 23),
(23, NULL, NULL, NULL, NULL, 'company', 'DANZI.TN', 11, 28, 4, 23),
(24, NULL, NULL, NULL, NULL, 'first_name', 'Andrea', 12, 29, 5, 24),
(25, NULL, NULL, NULL, NULL, 'last_name', 'Danzi', 12, 30, 5, 24),
(26, NULL, NULL, NULL, NULL, 'username', 'andrea.danzi', 12, 31, 5, 24),
(27, NULL, NULL, NULL, NULL, 'company', 'DANZI.TN', 12, 32, 5, 24),
(28, NULL, NULL, NULL, NULL, 'download', 'calcolo_viti.xls', 12, 33, 5, 24),
(29, NULL, NULL, NULL, NULL, 'first_name', 'Andrea', 13, 34, 5, 25),
(30, NULL, NULL, NULL, NULL, 'last_name', 'Danzi', 13, 35, 5, 25),
(31, NULL, NULL, NULL, NULL, 'code', 'WX012', 13, 36, 5, 25),
(32, NULL, NULL, NULL, NULL, 'company', 'DANZI.TN', 13, 37, 5, 25),
(33, NULL, NULL, NULL, NULL, 'date', '14/05/2017', 13, 38, 5, 25);

--
-- Indici per le tabelle scaricate
--

--
-- Indici per le tabelle `message`
--
ALTER TABLE `message`
  ADD PRIMARY KEY (`idmessage`),
  ADD KEY `fk_message_event_types1_idx` (`event_types_idevent_types`),
  ADD KEY `fk_message_datastructure1_idx` (`datastructure_iddatastructure`),
  ADD KEY `fk_message_email1_idx` (`email_idemail`),
  ADD KEY `fk_message_message_log1` (`message_log_idmessage_log`);

--
-- AUTO_INCREMENT per le tabelle scaricate
--

--
-- AUTO_INCREMENT per la tabella `message`
--
ALTER TABLE `message`
  MODIFY `idmessage` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=34;
--
-- Limiti per le tabelle scaricate
--

--
-- Limiti per la tabella `message`
--
ALTER TABLE `message`
  ADD CONSTRAINT `fk_message_datastructure1` FOREIGN KEY (`datastructure_iddatastructure`) REFERENCES `datastructure` (`iddatastructure`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  ADD CONSTRAINT `fk_message_email1` FOREIGN KEY (`email_idemail`) REFERENCES `email` (`idemail`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  ADD CONSTRAINT `fk_message_event_types1` FOREIGN KEY (`event_types_idevent_types`) REFERENCES `event_types` (`idevent_types`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  ADD CONSTRAINT `fk_message_message_log1` FOREIGN KEY (`message_log_idmessage_log`) REFERENCES `message_log` (`idmessage_log`) ON DELETE NO ACTION ON UPDATE NO ACTION;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
