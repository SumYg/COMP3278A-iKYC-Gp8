-- phpMyAdmin SQL Dump
-- version 4.6.6deb5ubuntu0.5
-- https://www.phpmyadmin.net/
--
-- Host: sophia
-- Generation Time: Nov 15, 2021 at 10:50 PM
-- Server version: 5.7.35-0ubuntu0.18.04.1
-- PHP Version: 7.2.24-0ubuntu0.18.04.8

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `h3566726`
--

-- --------------------------------------------------------

--
-- Table structure for table `Account`
--

CREATE TABLE `Account` (
  `account_number` varchar(30) NOT NULL,
  `username` varchar(30) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `Credit`
--

CREATE TABLE `Credit` (
  `account_number` varchar(30) NOT NULL,
  `available_credit` decimal(9,2) NOT NULL,
  `remaining_credit` decimal(9,2) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `Customer`
--

CREATE TABLE `Customer` (
  `username` varchar(30) NOT NULL,
  `password` varchar(30) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `Investment`
--

CREATE TABLE `Investment` (
  `account_number` varchar(30) NOT NULL,
  `amount` decimal(9,2) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `Login_History`
--

CREATE TABLE `Login_History` (
  `time` datetime NOT NULL,
  `username` varchar(30) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `Saving`
--

CREATE TABLE `Saving` (
  `account_number` varchar(30) NOT NULL,
  `amount` decimal(9,2) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `Stock`
--

CREATE TABLE `Stock` (
  `stock_name` varchar(30) NOT NULL,
  `live_price` double NOT NULL,
  `percentage_change` varchar(30) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `Trade`
--

CREATE TABLE `Trade` (
  `stock_name` varchar(10) NOT NULL,
  `account_number` varchar(30) NOT NULL,
  `no_shares` int(11) NOT NULL,
  `history_profit` decimal(9,2) NOT NULL,
  `total_spend` decimal(9,2) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `Transaction`
--

CREATE TABLE `Transaction` (
  `transaction_id` varchar(30) NOT NULL,
  `amount` decimal(9,2) NOT NULL,
  `time` time NOT NULL,
  `date` date NOT NULL,
  `from_account` varchar(30) NOT NULL,
  `to_account` varchar(30) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `Account`
--
ALTER TABLE `Account`
  ADD PRIMARY KEY (`account_number`),
  ADD KEY `username` (`username`);

--
-- Indexes for table `Credit`
--
ALTER TABLE `Credit`
  ADD PRIMARY KEY (`account_number`);

--
-- Indexes for table `Customer`
--
ALTER TABLE `Customer`
  ADD PRIMARY KEY (`username`);

--
-- Indexes for table `Investment`
--
ALTER TABLE `Investment`
  ADD PRIMARY KEY (`account_number`);

--
-- Indexes for table `Login_History`
--
ALTER TABLE `Login_History`
  ADD PRIMARY KEY (`username`,`time`);

--
-- Indexes for table `Saving`
--
ALTER TABLE `Saving`
  ADD PRIMARY KEY (`account_number`);

--
-- Indexes for table `Stock`
--
ALTER TABLE `Stock`
  ADD PRIMARY KEY (`stock_name`);

--
-- Indexes for table `Trade`
--
ALTER TABLE `Trade`
  ADD PRIMARY KEY (`stock_name`,`account_number`),
  ADD KEY `account_number` (`account_number`);

--
-- Indexes for table `Transaction`
--
ALTER TABLE `Transaction`
  ADD PRIMARY KEY (`transaction_id`),
  ADD KEY `Transaction` (`from_account`),
  ADD KEY `to_account` (`to_account`);

--
-- Constraints for dumped tables
--

--
-- Constraints for table `Account`
--
ALTER TABLE `Account`
  ADD CONSTRAINT `Account_ibfk_1` FOREIGN KEY (`username`) REFERENCES `Customer` (`username`);

--
-- Constraints for table `Credit`
--
ALTER TABLE `Credit`
  ADD CONSTRAINT `Credit_ibfk_1` FOREIGN KEY (`account_number`) REFERENCES `Account` (`account_number`);

--
-- Constraints for table `Investment`
--
ALTER TABLE `Investment`
  ADD CONSTRAINT `Investment_ibfk_1` FOREIGN KEY (`account_number`) REFERENCES `Account` (`account_number`);

--
-- Constraints for table `Login_History`
--
ALTER TABLE `Login_History`
  ADD CONSTRAINT `Login_History_ibfk_1` FOREIGN KEY (`username`) REFERENCES `Customer` (`username`);

--
-- Constraints for table `Saving`
--
ALTER TABLE `Saving`
  ADD CONSTRAINT `Saving_ibfk_1` FOREIGN KEY (`account_number`) REFERENCES `Account` (`account_number`);

--
-- Constraints for table `Trade`
--
ALTER TABLE `Trade`
  ADD CONSTRAINT `Trade_ibfk_1` FOREIGN KEY (`stock_name`) REFERENCES `Stock` (`stock_name`),
  ADD CONSTRAINT `Trade_ibfk_2` FOREIGN KEY (`account_number`) REFERENCES `Investment` (`account_number`);

--
-- Constraints for table `Transaction`
--
ALTER TABLE `Transaction`
  ADD CONSTRAINT `Transaction_ibfk_1` FOREIGN KEY (`from_account`) REFERENCES `Account` (`account_number`),
  ADD CONSTRAINT `Transaction_ibfk_2` FOREIGN KEY (`to_account`) REFERENCES `Account` (`account_number`);

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
