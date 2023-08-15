-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Aug 12, 2023 at 08:13 AM
-- Server version: 10.4.28-MariaDB
-- PHP Version: 8.0.28

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `gersgarage`
--

-- --------------------------------------------------------

--
-- Table structure for table `admin`
--

CREATE TABLE `admin` (
  `admin_id` int(11) NOT NULL,
  `username` varchar(50) NOT NULL,
  `password` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `admin`
--

INSERT INTO `admin` (`admin_id`, `username`, `password`) VALUES
(1, 'gergrg', '2022480');

-- --------------------------------------------------------

--
-- Table structure for table `bookings`
--

CREATE TABLE `bookings` (
  `booking_id` int(11) NOT NULL,
  `customer_id` int(11) NOT NULL,
  `vehicle_id` int(11) NOT NULL,
  `service_id` int(11) NOT NULL,
  `booking_date` date NOT NULL,
  `user_comments` varchar(500) DEFAULT NULL,
  `licence_details` varchar(255) DEFAULT NULL,
  `mechanic_id` int(11) DEFAULT 1,
  `booking_status_id` int(11) DEFAULT 1
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `bookings`
--

INSERT INTO `bookings` (`booking_id`, `customer_id`, `vehicle_id`, `service_id`, `booking_date`, `user_comments`, `licence_details`, `mechanic_id`, `booking_status_id`) VALUES
(18, 29, 1, 1, '2023-08-16', 'test önemli', 'A123123123', 2, 4),
(20, 29, 1, 1, '2023-08-16', 'önemli', 'A123123123', 5, 1),
(40, 29, 1, 2, '2023-08-16', '', 'A123123123', 1, 1),
(41, 29, 1, 2, '2023-08-16', '', 'A123123123', 1, 1),
(42, 29, 1, 2, '2023-08-16', '', 'A123123123', 1, 1),
(43, 29, 1, 4, '2023-08-16', '', 'A123123123', 1, 1),
(44, 29, 1, 2, '2023-08-16', '', 'A123123123', 1, 1),
(45, 29, 1, 2, '2023-08-16', '', 'A123123123', 1, 1),
(47, 29, 1, 2, '2023-08-16', '', 'A123123123', 1, 1),
(50, 29, 1, 1, '2023-08-16', '', 'A123123123', 1, 1),
(51, 29, 1, 3, '2023-08-16', '', 'A123123123', 1, 1),
(52, 29, 1, 2, '2023-08-16', '', 'A123123123', 1, 1),
(53, 29, 1, 1, '2023-08-16', '', 'A123123123', 1, 1);

-- --------------------------------------------------------

--
-- Table structure for table `booking_status`
--

CREATE TABLE `booking_status` (
  `booking_status_id` int(11) NOT NULL,
  `status` varchar(50) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `booking_status`
--

INSERT INTO `booking_status` (`booking_status_id`, `status`) VALUES
(1, 'Booked'),
(2, 'In Service'),
(3, 'Fixed / Completed'),
(4, 'Collected'),
(5, 'Unrepairable / Scrapped');

-- --------------------------------------------------------

--
-- Table structure for table `customers`
--

CREATE TABLE `customers` (
  `customer_id` int(11) NOT NULL,
  `name` varchar(255) NOT NULL,
  `mobile_phone` varchar(20) NOT NULL,
  `email` varchar(255) DEFAULT NULL,
  `password` varchar(20) DEFAULT NULL,
  `surname` varchar(20) DEFAULT NULL,
  `username` varchar(50) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `customers`
--

INSERT INTO `customers` (`customer_id`, `name`, `mobile_phone`, `email`, `password`, `surname`, `username`) VALUES
(29, 'burak', '5332152222', 'brk95@hotmail.com', '1234', 'korkmaz', 'brk95'),
(30, '13', '5332152222', 'brk9512312@hotmail.com', '1234', 'korkmaz', '1234'),
(31, 'brk', '2222222', '23466@hotmail.com', '123', 's', 'ssss'),
(32, 'f', '53321522222', '9514brk@hotmail.com', '5000/add_userBrk', 'e', 'brk222232s');

-- --------------------------------------------------------

--
-- Table structure for table `garage_settings`
--

CREATE TABLE `garage_settings` (
  `setting_id` int(11) NOT NULL,
  `setting_name` varchar(100) NOT NULL,
  `setting_value` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `mechanics`
--

CREATE TABLE `mechanics` (
  `mechanic_id` int(11) NOT NULL,
  `name` varchar(255) NOT NULL,
  `surname` varchar(50) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `mechanics`
--

INSERT INTO `mechanics` (`mechanic_id`, `name`, `surname`) VALUES
(1, 'no mechanic', 'assigned'),
(2, 'Ricardi', 'Smith'),
(3, 'John', 'Lopez'),
(4, 'Jane', 'Smith'),
(5, 'Michael', 'Johnson'),
(6, 'Emily', 'Williams');

-- --------------------------------------------------------

--
-- Table structure for table `parts`
--

CREATE TABLE `parts` (
  `part_id` int(11) NOT NULL,
  `part_name` varchar(100) NOT NULL,
  `part_cost` decimal(10,2) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `parts`
--

INSERT INTO `parts` (`part_id`, `part_name`, `part_cost`) VALUES
(1, 'Power Steering Hose', 18.99),
(2, 'Cabin Air Filterr', 11.23),
(3, 'asdas', 38.00),
(4, 'Brake Rotor', 48.75),
(5, 'Wheel Bearing', 22.99),
(6, 'Control Arm', 39.50),
(7, 'Fuel Filter', 8.25),
(8, 'Oxygen Sensor', 54.99),
(9, 'Mass Air Flow Sensor', 72.25),
(11, 'Ignition Control Module', 28.99),
(12, 'Shock Absorber', 38.75),
(13, 'Strut Assembly', 72.99),
(14, 'Exhaust Manifold', 67.50),
(15, 'Fuel Injector', 45.25),
(16, 'Clutch Kit', 129.99),
(17, 'Transmission Filter', 17.50),
(18, 'Engine Mount', 22.99),
(19, 'Fuel Pump Relay', 12.25),
(20, 'Camshaft Position Sensor', 29.99),
(21, 'Fuel Pressure Regulator', 18.75),
(22, 'Serpentine Belt', 13.50),
(23, 'Steering Gear Box', 155.25),
(24, 'A/C Condenser', 76.50),
(25, 'A/C Evaporator Core', 89.99),
(26, 'A/C Expansion Valve', 22.25),
(27, 'Radiator Hose', 9.99),
(28, 'Throttle Position Sensor', 32.75),
(29, 'Wheel Hub Assembly', 58.50),
(30, 'Windshield Washer Pump', 14.25),
(31, 'Car Battery Terminal', 6.99),
(32, 'asdasd', 32.00),
(33, 'asdasd', 44.00),
(34, 'cola', 23.00);

-- --------------------------------------------------------

--
-- Table structure for table `parts_used`
--

CREATE TABLE `parts_used` (
  `part_used_id` int(11) NOT NULL,
  `booking_id` int(11) NOT NULL,
  `part_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `parts_used`
--

INSERT INTO `parts_used` (`part_used_id`, `booking_id`, `part_id`) VALUES
(4, 18, 1),
(5, 18, 4),
(6, 18, 1),
(7, 18, 6),
(8, 18, 1),
(9, 18, 6),
(10, 20, 1),
(11, 20, 3),
(12, 18, 8),
(13, 18, 6),
(14, 18, 7),
(15, 18, 6),
(16, 18, 6),
(17, 20, 18),
(18, 20, 20),
(19, 18, 31),
(20, 18, 33),
(21, 18, 31),
(22, 18, 33);

-- --------------------------------------------------------

--
-- Table structure for table `services`
--

CREATE TABLE `services` (
  `service_id` int(11) NOT NULL,
  `service_type` varchar(50) NOT NULL,
  `service_cost` decimal(10,2) NOT NULL,
  `workload` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `services`
--

INSERT INTO `services` (`service_id`, `service_type`, `service_cost`, `workload`) VALUES
(1, 'AnnualService', 100.00, 1),
(2, 'MajorService', 200.00, 2),
(3, 'Repair', 300.00, 1),
(4, 'MajorRepair', 400.00, 1);

-- --------------------------------------------------------

--
-- Table structure for table `vehicles`
--

CREATE TABLE `vehicles` (
  `vehicle_id` int(11) NOT NULL,
  `customer_id` int(11) NOT NULL,
  `vehicle_type` varchar(50) NOT NULL,
  `make` varchar(100) NOT NULL,
  `licence_details` varchar(20) NOT NULL,
  `engine_type` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `vehicles`
--

INSERT INTO `vehicles` (`vehicle_id`, `customer_id`, `vehicle_type`, `make`, `licence_details`, `engine_type`) VALUES
(1, 29, 'car', 'Ford', 'A123123123', 'diesel'),
(3, 29, 'car', 'Ford', 'A123123123', 'diesel'),
(4, 29, 'car', 'Ford', 'A123123123', 'diesel'),
(5, 29, 'other', 'Jeep', 'asdasdasd22', 'hybrid'),
(6, 29, 'car', 'Ford', 'A123123123222', 'hybrid'),
(7, 29, 'car', 'Ford', 'dsad', 'diesel'),
(8, 29, 'car', 'Ford', 'asd', 'diesel'),
(9, 29, 'other', 'Peugeot', 'ASDASD22221', 'diesel');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `admin`
--
ALTER TABLE `admin`
  ADD PRIMARY KEY (`admin_id`);

--
-- Indexes for table `bookings`
--
ALTER TABLE `bookings`
  ADD PRIMARY KEY (`booking_id`),
  ADD KEY `customer_id` (`customer_id`),
  ADD KEY `vehicle_id` (`vehicle_id`),
  ADD KEY `service_id` (`service_id`),
  ADD KEY `fk_mechanic` (`mechanic_id`),
  ADD KEY `booking_status_id` (`booking_status_id`);

--
-- Indexes for table `booking_status`
--
ALTER TABLE `booking_status`
  ADD PRIMARY KEY (`booking_status_id`);

--
-- Indexes for table `customers`
--
ALTER TABLE `customers`
  ADD PRIMARY KEY (`customer_id`);

--
-- Indexes for table `garage_settings`
--
ALTER TABLE `garage_settings`
  ADD PRIMARY KEY (`setting_id`);

--
-- Indexes for table `mechanics`
--
ALTER TABLE `mechanics`
  ADD PRIMARY KEY (`mechanic_id`);

--
-- Indexes for table `parts`
--
ALTER TABLE `parts`
  ADD PRIMARY KEY (`part_id`);

--
-- Indexes for table `parts_used`
--
ALTER TABLE `parts_used`
  ADD PRIMARY KEY (`part_used_id`),
  ADD KEY `booking_id` (`booking_id`),
  ADD KEY `part_id` (`part_id`);

--
-- Indexes for table `services`
--
ALTER TABLE `services`
  ADD PRIMARY KEY (`service_id`);

--
-- Indexes for table `vehicles`
--
ALTER TABLE `vehicles`
  ADD PRIMARY KEY (`vehicle_id`),
  ADD KEY `customer_id` (`customer_id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `admin`
--
ALTER TABLE `admin`
  MODIFY `admin_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `bookings`
--
ALTER TABLE `bookings`
  MODIFY `booking_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=54;

--
-- AUTO_INCREMENT for table `booking_status`
--
ALTER TABLE `booking_status`
  MODIFY `booking_status_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT for table `customers`
--
ALTER TABLE `customers`
  MODIFY `customer_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=33;

--
-- AUTO_INCREMENT for table `garage_settings`
--
ALTER TABLE `garage_settings`
  MODIFY `setting_id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `mechanics`
--
ALTER TABLE `mechanics`
  MODIFY `mechanic_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT for table `parts`
--
ALTER TABLE `parts`
  MODIFY `part_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=35;

--
-- AUTO_INCREMENT for table `parts_used`
--
ALTER TABLE `parts_used`
  MODIFY `part_used_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=23;

--
-- AUTO_INCREMENT for table `services`
--
ALTER TABLE `services`
  MODIFY `service_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT for table `vehicles`
--
ALTER TABLE `vehicles`
  MODIFY `vehicle_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=10;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `bookings`
--
ALTER TABLE `bookings`
  ADD CONSTRAINT `bookings_ibfk_1` FOREIGN KEY (`customer_id`) REFERENCES `customers` (`customer_id`),
  ADD CONSTRAINT `bookings_ibfk_2` FOREIGN KEY (`vehicle_id`) REFERENCES `vehicles` (`vehicle_id`),
  ADD CONSTRAINT `bookings_ibfk_3` FOREIGN KEY (`service_id`) REFERENCES `services` (`service_id`),
  ADD CONSTRAINT `bookings_ibfk_4` FOREIGN KEY (`booking_status_id`) REFERENCES `booking_status` (`booking_status_id`),
  ADD CONSTRAINT `fk_mechanic` FOREIGN KEY (`mechanic_id`) REFERENCES `mechanics` (`mechanic_id`);

--
-- Constraints for table `parts_used`
--
ALTER TABLE `parts_used`
  ADD CONSTRAINT `parts_used_ibfk_1` FOREIGN KEY (`booking_id`) REFERENCES `bookings` (`booking_id`),
  ADD CONSTRAINT `parts_used_ibfk_2` FOREIGN KEY (`part_id`) REFERENCES `parts` (`part_id`);

--
-- Constraints for table `vehicles`
--
ALTER TABLE `vehicles`
  ADD CONSTRAINT `vehicles_ibfk_1` FOREIGN KEY (`customer_id`) REFERENCES `customers` (`customer_id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
