-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: localhost
-- Generation Time: Apr 04, 2024 at 08:36 PM
-- Server version: 10.4.28-MariaDB
-- PHP Version: 8.2.4

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `StudentManagementSystem`
--

-- --------------------------------------------------------

--
-- Table structure for table `courses`
--

CREATE TABLE `courses` (
  `course_code` char(8) NOT NULL,
  `course_name` varchar(100) NOT NULL,
  `instructor_id` char(11) NOT NULL,
  `department_id` char(11) NOT NULL,
  `description` text NOT NULL,
  `credit_hours` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `courses`
--

INSERT INTO `courses` (`course_code`, `course_name`, `instructor_id`, `department_id`, `description`, `credit_hours`) VALUES
('22CST101', 'Cricket', '2010icp1000', '5', 'Nothing', 42),
('22CST103', 'Soccer', '2010icp1000', '4', 'Nothing Again', 30);

-- --------------------------------------------------------

--
-- Table structure for table `departments`
--

CREATE TABLE `departments` (
  `department_id` char(11) NOT NULL,
  `department_name` varchar(100) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `departments`
--

INSERT INTO `departments` (`department_id`, `department_name`) VALUES
('4', 'Chemical Engineering'),
('1', 'Civil Engineering'),
('5', 'Computer Science and Engineering'),
('2', 'Electrical Engineering'),
('3', 'Mechanical Engineering');

-- --------------------------------------------------------

--
-- Table structure for table `enrollments`
--

CREATE TABLE `enrollments` (
  `enrollment_id` int(11) NOT NULL,
  `student_id` char(11) NOT NULL,
  `course_code` char(8) NOT NULL,
  `enrollment_date` date DEFAULT curdate()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Table structure for table `grades`
--

CREATE TABLE `grades` (
  `grade_id` int(11) NOT NULL,
  `enrollment_id` int(11) NOT NULL,
  `grade` enum('AA','AB','BB','BC','CC','CD','DD','FF','FP') DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Table structure for table `instructors`
--

CREATE TABLE `instructors` (
  `instructor_id` char(11) NOT NULL,
  `first_name` varchar(50) NOT NULL,
  `last_name` varchar(50) NOT NULL,
  `dob` date DEFAULT NULL,
  `sex` enum('Male','Female','Other') DEFAULT NULL,
  `address` text DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL,
  `phone_number` varchar(20) DEFAULT NULL,
  `doj` date DEFAULT NULL,
  `city` varchar(50) NOT NULL,
  `state` varchar(50) NOT NULL,
  `address_pin` int(6) NOT NULL,
  `bloodgroup` enum('A_plus','A_minus','B_plus','B_minus','AB_plus','AB_minus','O_plus','O_minus') DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `instructors`
--

INSERT INTO `instructors` (`instructor_id`, `first_name`, `last_name`, `dob`, `sex`, `address`, `email`, `phone_number`, `doj`, `city`, `state`, `address_pin`, `bloodgroup`) VALUES
('2010icp1000', 'Nitish', 'Kumar', '1986-01-21', 'Male', '3, etc', 'nitish123@gmail.com', '9546729123', '2010-07-23', 'etc', 'etc', 203914, 'AB_plus');

-- --------------------------------------------------------

--
-- Table structure for table `students`
--

CREATE TABLE `students` (
  `student_id` char(11) NOT NULL,
  `first_name` varchar(45) NOT NULL,
  `middle_name` varchar(45) DEFAULT NULL,
  `last_name` varchar(45) NOT NULL,
  `email` varchar(50) NOT NULL,
  `degree_name` varchar(100) NOT NULL,
  `grad_level` enum('B_Tech','M_Tech','PHD') NOT NULL,
  `address` text NOT NULL,
  `city` varchar(50) NOT NULL,
  `state` varchar(50) NOT NULL,
  `address_pin` int(6) NOT NULL,
  `father_name` varchar(100) NOT NULL,
  `mother_name` varchar(100) NOT NULL,
  `dob` date NOT NULL,
  `bloodgroup` enum('A_plus','A_minus','B_plus','B_minus','AB_plus','AB_minus','O_plus','O_minus') DEFAULT NULL,
  `doa` date NOT NULL,
  `father_occ` varchar(100) NOT NULL,
  `mother_occ` varchar(100) NOT NULL,
  `student_phoneno` bigint(20) NOT NULL,
  `guardian_phoneno` bigint(20) NOT NULL,
  `sex` enum('Male','Female','Other') NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `students`
--

INSERT INTO `students` (`student_id`, `first_name`, `middle_name`, `last_name`, `email`, `degree_name`, `grad_level`, `address`, `city`, `state`, `address_pin`, `father_name`, `mother_name`, `dob`, `bloodgroup`, `doa`, `father_occ`, `mother_occ`, `student_phoneno`, `guardian_phoneno`, `sex`) VALUES
('2022ucp1111', 'Ayush', 'R', 'Raghav', 'ayushraghav@gmail.com', 'Computer Science and Engineering', 'B_Tech', '12, Nandganv, Nath Ji ki Thadi, Niwaru Road, Jhotwara, Jaipur, Rajasthan', 'Jaipur', 'Rajasthan', 302012, 'A Raghav', 'M ', '2003-01-24', 'A_minus', '2021-07-22', 'Govt. Servant', 'Housewife', 999887700, 7725921000, 'Male'),
('2022ucp1504', 'Rohit', 'R.', 'Jangid', 'rorojangid@gmail.com', 'Computer Science and Engineering', 'B_Tech', 'Nothing ', 'Nothing', 'Nothing', 123234, 'Father of Rohit', 'Mother of Rohit', '2003-04-17', 'AB_plus', '2023-07-25', 'father oc', 'mother oc', 8888000011, 7799331313, 'Male');

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `user_id` char(11) NOT NULL,
  `user_type` enum('admin','student','instructor') NOT NULL,
  `user_password_hash` varchar(256) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`user_id`, `user_type`, `user_password_hash`) VALUES
('12345678901', 'admin', 'scrypt:32768:8:1$E55KMZTGGyy5LJh3$db3c92f4a13ed82bb319ba4c74ad3d64b60b65d6f6152479ef44124fb5617b29663789aa0d1c4dae44263e88b1ac0a616f66fa1f6cfdc5acd4c928742c271083'),
('s1234567890', 'student', 'scrypt:32768:8:1$JWaFVgOPWXHhoGDP$cb96c57a03c79122a0f31798c1b8f9d68d20a8a60ce7f0cd26b36c28c6697b1a5ada71bd869a33ac1f218fab358bb6fab2d61a8f02943353b568bd6357bb3d3a'),
('i1234567890', 'instructor', 'scrypt:32768:8:1$To1Xlhp0txJi6Fy1$48cff40a535ff49b091ec5adf8c8eceb61d763e2824094885d5ba12049a4d0948c2aa2574609678f749b136672a0df06f494a4389e9cbf2ae785c9469eb66ffa'),
('2022ucp1111', 'student', 'scrypt:32768:8:1$3FQhFKvf8XCLOoh8$0b91c91bb878b83dd76542a4953b1697d2d9c80156cbf7e47d4d671c9b211c77f4963b949f8d03dc7a6b36f9dc2d5fc88565e262c7b0c50cfc45f2eb0c822ea2'),
('2010icp1000', 'instructor', 'scrypt:32768:8:1$GC8B9bfPnewwfZaV$2d02b2592ac6a3f633443d6bb03e847d99976e34c885a7f712c9e555d7f2d18750cf098a029fbf31056109a84b6c9bb8a5e29dff4f4d16a1793a3a3cd7df3c0e'),
('2022ucp1504', 'student', 'scrypt:32768:8:1$7zlLx2Qa4JoHdH0M$bff77b9048a04413b755c865643e642565ec84eb7941d123874c7b26a6ecac6a03209fc502140287c0112cceb704af857507a3e11fd6c316b360e2e97b9a8c97');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `courses`
--
ALTER TABLE `courses`
  ADD PRIMARY KEY (`course_code`),
  ADD KEY `fk_instructors` (`instructor_id`),
  ADD KEY `fk_departments` (`department_id`);

--
-- Indexes for table `departments`
--
ALTER TABLE `departments`
  ADD PRIMARY KEY (`department_id`),
  ADD UNIQUE KEY `DepartmentName` (`department_name`);

--
-- Indexes for table `enrollments`
--
ALTER TABLE `enrollments`
  ADD PRIMARY KEY (`enrollment_id`),
  ADD KEY `student_id` (`student_id`),
  ADD KEY `course_code` (`course_code`);

--
-- Indexes for table `grades`
--
ALTER TABLE `grades`
  ADD PRIMARY KEY (`grade_id`),
  ADD KEY `fk_enrollments` (`enrollment_id`);

--
-- Indexes for table `instructors`
--
ALTER TABLE `instructors`
  ADD PRIMARY KEY (`instructor_id`);

--
-- Indexes for table `students`
--
ALTER TABLE `students`
  ADD PRIMARY KEY (`student_id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `enrollments`
--
ALTER TABLE `enrollments`
  MODIFY `enrollment_id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `grades`
--
ALTER TABLE `grades`
  MODIFY `grade_id` int(11) NOT NULL AUTO_INCREMENT;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `courses`
--
ALTER TABLE `courses`
  ADD CONSTRAINT `fk_departments` FOREIGN KEY (`department_id`) REFERENCES `departments` (`department_id`),
  ADD CONSTRAINT `fk_instructors` FOREIGN KEY (`instructor_id`) REFERENCES `instructors` (`instructor_id`);

--
-- Constraints for table `enrollments`
--
ALTER TABLE `enrollments`
  ADD CONSTRAINT `enrollments_ibfk_1` FOREIGN KEY (`student_id`) REFERENCES `students` (`student_id`),
  ADD CONSTRAINT `enrollments_ibfk_2` FOREIGN KEY (`course_code`) REFERENCES `courses` (`course_code`);

--
-- Constraints for table `grades`
--
ALTER TABLE `grades`
  ADD CONSTRAINT `fk_enrollments` FOREIGN KEY (`enrollment_id`) REFERENCES `enrollments` (`enrollment_id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
