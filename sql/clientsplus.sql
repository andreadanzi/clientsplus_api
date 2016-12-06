-- phpMyAdmin SQL Dump
-- version 4.5.4.1deb2ubuntu2
-- http://www.phpmyadmin.net
--
-- Host: localhost
-- Creato il: Dic 06, 2016 alle 07:01
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
-- Struttura della tabella `datastructure`
--

CREATE TABLE `datastructure` (
  `iddatastructure` int(11) NOT NULL,
  `event_types_idevent_types` int(11) NOT NULL,
  `name` varchar(45) DEFAULT NULL,
  `type` varchar(45) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dump dei dati per la tabella `datastructure`
--

INSERT INTO `datastructure` (`iddatastructure`, `event_types_idevent_types`, `name`, `type`) VALUES
(21, 10, 'first_name', 'string'),
(22, 10, 'last_name', 'string'),
(23, 10, 'username', 'string'),
(24, 10, 'company', 'string'),
(25, 11, 'first_name', 'string'),
(26, 11, 'last_name', 'string'),
(27, 11, 'username', 'string'),
(28, 11, 'company', 'string'),
(29, 12, 'first_name', 'string'),
(30, 12, 'last_name', 'string'),
(31, 12, 'username', 'string'),
(32, 12, 'company', 'string'),
(33, 12, 'download', 'string'),
(34, 13, 'first_name', 'string'),
(35, 13, 'last_name', 'string'),
(36, 13, 'code', 'string'),
(37, 13, 'company', 'string'),
(38, 13, 'date', 'string');

-- --------------------------------------------------------

--
-- Struttura della tabella `email`
--

CREATE TABLE `email` (
  `idemail` int(11) NOT NULL,
  `email_address` varchar(255) NOT NULL,
  `import_status` int(11) NOT NULL,
  `import_relations` text,
  `timestamp` datetime DEFAULT NULL,
  `import_date` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dump dei dati per la tabella `email`
--

INSERT INTO `email` (`idemail`, `email_address`, `import_status`, `import_relations`, `timestamp`, `import_date`) VALUES
(3, 'andrea.dnz@gmail.com', 0, 'ND', '0000-00-00 00:00:00', '0000-00-00 00:00:00'),
(4, 'andrea@danzi.tn.com', 0, 'ND', '2016-12-03 08:43:19', '2016-12-03 08:54:14'),
(5, 'info@danzi.tn.com', 0, 'ND', '2016-12-03 08:43:19', '2016-12-03 09:42:00');

-- --------------------------------------------------------

--
-- Struttura della tabella `event_types`
--

CREATE TABLE `event_types` (
  `idevent_types` int(11) NOT NULL,
  `event_type_code` varchar(45) NOT NULL,
  `timestamp` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dump dei dati per la tabella `event_types`
--

INSERT INTO `event_types` (`idevent_types`, `event_type_code`, `timestamp`) VALUES
(10, 'registration', NULL),
(11, 'form_catalogo', '2016-12-03 08:43:19'),
(12, 'download', '2016-12-03 08:43:19'),
(13, 'corso', '2016-12-03 08:41:39');

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
(33, NULL, NULL, NULL, NULL, 'date', '14/05/2017', 13, 38, 5, 25),
(34, NULL, NULL, NULL, NULL, 'first_name', 'Andrea', 13, 34, 5, 26),
(35, NULL, NULL, NULL, NULL, 'last_name', 'Danzi', 13, 35, 5, 26),
(36, NULL, NULL, NULL, NULL, 'code', 'WX012', 13, 36, 5, 26),
(37, NULL, NULL, NULL, NULL, 'company', 'DANZI.TN', 13, 37, 5, 26),
(38, NULL, NULL, NULL, NULL, 'date', '14/05/2017', 13, 38, 5, 26),
(39, NULL, NULL, NULL, NULL, 'first_name', 'Andrea', 13, 34, 5, 27),
(40, NULL, NULL, NULL, NULL, 'last_name', 'Danzi', 13, 35, 5, 27),
(41, NULL, NULL, NULL, NULL, 'code', 'WX012', 13, 36, 5, 27),
(42, NULL, NULL, NULL, NULL, 'company', 'DANZI.TN', 13, 37, 5, 27),
(43, NULL, NULL, NULL, NULL, 'date', '14/05/2017', 13, 38, 5, 27),
(44, NULL, NULL, NULL, NULL, 'first_name', 'Andrea', 13, 34, 5, 28),
(45, NULL, NULL, NULL, NULL, 'last_name', 'Danzi', 13, 35, 5, 28),
(46, NULL, NULL, NULL, NULL, 'code', 'WX012', 13, 36, 5, 28),
(47, NULL, NULL, NULL, NULL, 'company', 'DANZI.TN', 13, 37, 5, 28),
(48, NULL, NULL, NULL, NULL, 'date', '14/05/2017', 13, 38, 5, 28),
(49, NULL, NULL, NULL, NULL, 'first_name', 'Andrea', 13, 34, 5, 29),
(50, NULL, NULL, NULL, NULL, 'last_name', 'Danzi', 13, 35, 5, 29),
(51, NULL, NULL, NULL, NULL, 'code', 'WX012', 13, 36, 5, 29),
(52, NULL, NULL, NULL, NULL, 'company', 'DANZI.TN', 13, 37, 5, 29),
(53, NULL, NULL, NULL, NULL, 'date', '14/05/2017', 13, 38, 5, 29),
(54, NULL, NULL, NULL, NULL, 'first_name', 'Andrea', 13, 34, 5, 30),
(55, NULL, NULL, NULL, NULL, 'last_name', 'Danzi', 13, 35, 5, 30),
(56, NULL, NULL, NULL, NULL, 'code', 'WX012', 13, 36, 5, 30),
(57, NULL, NULL, NULL, NULL, 'company', 'DANZI.TN', 13, 37, 5, 30),
(58, NULL, NULL, NULL, NULL, 'date', '14/05/2017', 13, 38, 5, 30);

-- --------------------------------------------------------

--
-- Struttura della tabella `message_log`
--

CREATE TABLE `message_log` (
  `idmessage_log` int(11) NOT NULL,
  `timestamp` datetime DEFAULT NULL,
  `hashstring` varchar(255) DEFAULT NULL,
  `by_email` varchar(255) NOT NULL,
  `when_timestamp` int(11) NOT NULL,
  `type_event` varchar(255) NOT NULL,
  `import_status` int(11) NOT NULL,
  `import_date` datetime NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dump dei dati per la tabella `message_log`
--

INSERT INTO `message_log` (`idmessage_log`, `timestamp`, `hashstring`, `by_email`, `when_timestamp`, `type_event`, `import_status`, `import_date`) VALUES
(22, '2016-12-03 08:42:31', 'e1202b8984827c0a6a53107501c29149', 'andrea.dnz@gmail.com', 1480750951, 'registration', 0, '2016-12-03 08:49:14'),
(23, '2016-12-03 08:43:19', 'cdadb041f74f712f43cd8dd4d55fe9ee', 'andrea@danzi.tn.com', 1480750999, 'form_catalogo', 0, '2016-12-03 08:54:14'),
(24, '2016-12-03 08:43:19', '4b12d7fe15a8eb7bf6eae0d8fd5d5ff4', 'info@danzi.tn.com', 1480750999, 'download', 0, '2016-12-03 09:42:00'),
(25, '2016-12-03 08:41:39', 'e2e9e453361dc4567212c68b568b7e20', 'info@danzi.tn.com', 1480750899, 'corso', 0, '2016-12-03 09:44:02'),
(26, '2016-12-03 08:39:59', '3b96f4cac0a570d12dfd60ff959b5022', 'info@danzi.tn.com', 1480750799, 'corso', 0, '2016-12-03 10:00:44'),
(27, '2016-12-03 08:36:39', '351d3d20cc466848cfbdc93b8b38ef32', 'info@danzi.tn.com', 1480750599, 'corso', 0, '2016-12-03 10:08:42'),
(28, '2016-12-03 05:53:19', '52df418d6b5f4f08ebe1425582808a6a', 'info@danzi.tn.com', 1480740799, 'corso', 0, '2016-12-05 10:21:37'),
(29, '2016-12-03 05:46:39', '229e6fb15a34675bef22506b7e5d5b0c', 'info@danzi.tn.com', 1480740399, 'corso', 0, '2016-12-05 10:53:53'),
(30, '2016-12-03 05:44:59', '223b0b988355a30fb555f807628e4a21', 'info@danzi.tn.com', 1480740299, 'corso', 0, '2016-12-05 10:55:10');

--
-- Indici per le tabelle scaricate
--

--
-- Indici per le tabelle `datastructure`
--
ALTER TABLE `datastructure`
  ADD PRIMARY KEY (`iddatastructure`),
  ADD KEY `fk_datastructure_event_types_idx` (`event_types_idevent_types`);

--
-- Indici per le tabelle `email`
--
ALTER TABLE `email`
  ADD PRIMARY KEY (`idemail`);

--
-- Indici per le tabelle `event_types`
--
ALTER TABLE `event_types`
  ADD PRIMARY KEY (`idevent_types`);

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
-- Indici per le tabelle `message_log`
--
ALTER TABLE `message_log`
  ADD PRIMARY KEY (`idmessage_log`);

--
-- AUTO_INCREMENT per le tabelle scaricate
--

--
-- AUTO_INCREMENT per la tabella `datastructure`
--
ALTER TABLE `datastructure`
  MODIFY `iddatastructure` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=39;
--
-- AUTO_INCREMENT per la tabella `email`
--
ALTER TABLE `email`
  MODIFY `idemail` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;
--
-- AUTO_INCREMENT per la tabella `event_types`
--
ALTER TABLE `event_types`
  MODIFY `idevent_types` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=14;
--
-- AUTO_INCREMENT per la tabella `message`
--
ALTER TABLE `message`
  MODIFY `idmessage` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=59;
--
-- AUTO_INCREMENT per la tabella `message_log`
--
ALTER TABLE `message_log`
  MODIFY `idmessage_log` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=31;
--
-- Limiti per le tabelle scaricate
--

--
-- Limiti per la tabella `datastructure`
--
ALTER TABLE `datastructure`
  ADD CONSTRAINT `fk_datastructure_event_types` FOREIGN KEY (`event_types_idevent_types`) REFERENCES `event_types` (`idevent_types`) ON DELETE NO ACTION ON UPDATE NO ACTION;

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
