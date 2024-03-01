-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: localhost
-- Generation Time: Feb 24, 2024 at 12:34 PM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.0.30

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `AttendEase`
--

-- --------------------------------------------------------

--
-- Table structure for table `attendance`
--

CREATE TABLE `attendance` (
  `id` int(11) NOT NULL,
  `student_id` int(11) DEFAULT NULL,
  `student_name` varchar(255) DEFAULT NULL,
  `student_email` varchar(255) DEFAULT NULL,
  `student_reg_number` varchar(255) DEFAULT NULL,
  `date` date DEFAULT NULL,
  `time` time DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `attendance`
--

INSERT INTO `attendance` (`id`, `student_id`, `student_name`, `student_email`, `student_reg_number`, `date`, `time`) VALUES
(1, 10, 'Elon mask', 'elonmaskk@gmail.com', '0123456', '2024-02-24', '13:46:28'),
(2, 10, 'Elon mask', 'elonmaskk@gmail.com', '0123456', '2024-02-24', '13:46:29'),
(3, 10, 'Elon mask', 'elonmaskk@gmail.com', '0123456', '2024-02-24', '13:46:30'),
(4, 10, 'Elon mask', 'elonmaskk@gmail.com', '0123456', '2024-02-24', '13:46:30'),
(5, 10, 'Elon mask', 'elonmaskk@gmail.com', '0123456', '2024-02-24', '13:46:31'),
(6, 10, 'Elon mask', 'elonmaskk@gmail.com', '0123456', '2024-02-24', '13:46:31'),
(7, 10, 'Elon mask', 'elonmaskk@gmail.com', '0123456', '2024-02-24', '13:46:32'),
(8, 10, 'Elon mask', 'elonmaskk@gmail.com', '0123456', '2024-02-24', '13:46:32'),
(9, 10, 'Elon mask', 'elonmaskk@gmail.com', '0123456', '2024-02-24', '13:46:32'),
(10, 10, 'Elon mask', 'elonmaskk@gmail.com', '0123456', '2024-02-24', '13:46:33'),
(11, 10, 'Elon mask', 'elonmaskk@gmail.com', '0123456', '2024-02-24', '13:46:33'),
(12, 10, 'Elon mask', 'elonmaskk@gmail.com', '0123456', '2024-02-24', '13:46:34'),
(13, 10, 'Elon mask', 'elonmaskk@gmail.com', '0123456', '2024-02-24', '13:46:34'),
(14, 10, 'Elon mask', 'elonmaskk@gmail.com', '0123456', '2024-02-24', '13:46:35'),
(15, 10, 'Elon mask', 'elonmaskk@gmail.com', '0123456', '2024-02-24', '13:46:35'),
(16, 10, 'Elon mask', 'elonmaskk@gmail.com', '0123456', '2024-02-24', '13:46:36'),
(17, 10, 'Elon mask', 'elonmaskk@gmail.com', '0123456', '2024-02-24', '13:46:36'),
(18, 10, 'Elon mask', 'elonmaskk@gmail.com', '0123456', '2024-02-24', '13:46:37');

-- --------------------------------------------------------

--
-- Table structure for table `students`
--

CREATE TABLE `students` (
  `id` int(11) NOT NULL,
  `name` varchar(255) NOT NULL,
  `email` varchar(255) NOT NULL,
  `reg_number` varchar(255) NOT NULL,
  `image_paths` varchar(2048) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `students`
--

INSERT INTO `students` (`id`, `name`, `email`, `reg_number`, `image_paths`) VALUES
(10, 'Elon mask', 'elonmaskk@gmail.com', '0123456', '/tmp/tmp69zqr578/image_1.jpg,/tmp/tmp69zqr578/image_2.jpg,/tmp/tmp69zqr578/image_3.jpg'),
(11, 'elon mask', 'mask@gmail.com', '02216516', '/opt/lampp/htdocs/AttendEase/images/image_1.jpg,/opt/lampp/htdocs/AttendEase/images/image_2.jpg,/opt/lampp/htdocs/AttendEase/images/image_3.jpg'),
(12, 'namoma derick', 'derick@gmail.com', '4248924', '/opt/lampp/htdocs/AttendEase/images/image_1.jpg,/opt/lampp/htdocs/AttendEase/images/image_2.jpg,/opt/lampp/htdocs/AttendEase/images/image_3.jpg'),
(13, 'Elon mask', 'elonmaskk@gmail.com', '4248924', '/opt/lampp/htdocs/AttendEase/images/elon_mask.jpeg,/opt/lampp/htdocs/AttendEase/images/elon_mask.jpeg,/opt/lampp/htdocs/AttendEase/images/elon_mask.jpeg');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `attendance`
--
ALTER TABLE `attendance`
  ADD PRIMARY KEY (`id`),
  ADD KEY `fk_student` (`student_id`);

--
-- Indexes for table `students`
--
ALTER TABLE `students`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `attendance`
--
ALTER TABLE `attendance`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=19;

--
-- AUTO_INCREMENT for table `students`
--
ALTER TABLE `students`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=14;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `attendance`
--
ALTER TABLE `attendance`
  ADD CONSTRAINT `fk_student` FOREIGN KEY (`student_id`) REFERENCES `students` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
