-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: localhost
-- Generation Time: Apr 24, 2024 at 11:14 AM
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
('22CST233', 'Introduction to Computer Science', '2010icp1000', '5', 'This course provides an introduction to the fundamentals of computer science.', 42),
('CS201000', 'Data Structures and Algorithms', '2010icp1001', '5', 'This course covers advanced data structures and algorithms.', 42),
('CS301000', 'Database Management Systems', '2010icp1002', '5', 'This course explores the principles and techniques of database management systems.', 42),
('CS401000', 'Software Engineering', '2010icp1003', '5', 'This course covers the principles and practices of software engineering.', 42),
('CS501000', 'Machine Learning', '2010icp1004', '5', 'This course covers the theory and algorithms behind machine learning.', 42),
('CS601000', 'Artificial Intelligence', '2010icp1005', '5', 'This course explores the principles and techniques of artificial intelligence.', 42),
('CS701000', 'Computer Networks', '2010icp1006', '5', 'This course introduces the fundamentals of computer networks.', 38),
('CS801000', 'Operating Systems', '2010icp1007', '5', 'This course introduces the principles and components of operating systems.', 40),
('CS901000', 'Web Development', '2010icp1008', '5', 'This course covers the principles and techniques of web development.', 38);

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

--
-- Dumping data for table `enrollments`
--

INSERT INTO `enrollments` (`enrollment_id`, `student_id`, `course_code`, `enrollment_date`) VALUES
(1, '2022ucp1111', '22CST101', '2024-04-13'),
(4, '2022ucp1111', '22CST233', '2024-04-20'),
(5, '2022ucp1111', 'CS601000', '2024-04-24'),
(6, '2022ucp1111', 'CS701000', '2024-04-24');

-- --------------------------------------------------------

--
-- Table structure for table `grades`
--

CREATE TABLE `grades` (
  `grade_id` int(11) NOT NULL,
  `enrollment_id` int(11) NOT NULL,
  `grade` enum('AA','AB','BB','BC','CC','CD','DD','FF','FP') DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `grades`
--

INSERT INTO `grades` (`grade_id`, `enrollment_id`, `grade`) VALUES
(1, 1, 'BC'),
(2, 4, 'CC');

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
  `phone_number` bigint(10) DEFAULT NULL,
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
('2010icp1000', 'Nitish', 'Kumar', '1986-01-21', 'Male', '3, etc', 'nitish123@gmail.com', 8546729123, '2010-07-23', 'etc', 'etc', 203914, 'AB_plus'),
('2010icp1001', 'Priya', 'Sharma', '1988-05-15', 'Female', '456 Park Avenue, Mumbai', 'priya.sharma@example.com', 9876543210, '2010-09-10', 'Mumbai', 'Maharashtra', 400001, 'B_plus'),
('2010icp1002', 'Rahul', 'Singh', '1985-09-30', 'Male', '789 Elm Street, Delhi', 'rahul.singh@example.com', 7890123456, '2010-11-05', 'Delhi', 'Delhi', 110001, 'O_plus'),
('2010icp1003', 'Sunita', 'Patel', '1990-03-12', 'Female', '567 Oak Avenue, Chennai', 'sunita.patel@example.com', 7012345678, '2010-12-20', 'Chennai', 'Tamil Nadu', 600001, 'A_minus'),
('2010icp1004', 'Amit', 'Gupta', '1987-07-18', 'Male', '890 Pine Street, Kolkata', 'amit.gupta@example.com', 8765432109, '2011-02-15', 'Kolkata', 'West Bengal', 700001, 'B_minus'),
('2010icp1005', 'Anjali', 'Verma', '1989-11-25', 'Female', '234 Cedar Avenue, Hyderabad', 'anjali.verma@example.com', 9012345678, '2011-04-01', 'Hyderabad', 'Telangana', 500001, 'A_plus'),
('2010icp1006', 'Rajesh', 'Yadav', '1984-04-08', 'Male', '345 Maple Street, Pune', 'rajesh.yadav@example.com', 8901234567, '2011-06-10', 'Pune', 'Maharashtra', 411001, 'AB_minus'),
('2010icp1007', 'Pooja', 'Shah', '1983-10-02', 'Female', '678 Birch Avenue, Ahmedabad', 'pooja.shah@example.com', 7654321098, '2011-08-20', 'Ahmedabad', 'Gujarat', 380001, 'O_minus'),
('2010icp1008', 'Vivek', 'Kumar', '1982-12-17', 'Male', '456 Pine Street, Jaipur', 'vivek.kumar@example.com', 6789012345, '2011-10-30', 'Jaipur', 'Rajasthan', 302001, 'B_plus'),
('2010icp1009', 'Neha', 'Joshi', '1991-06-28', 'Female', '789 Elm Street, Lucknow', 'neha.joshi@example.com', 6543210987, '2011-12-05', 'Lucknow', 'Uttar Pradesh', 226001, 'A_plus');

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
  `student_phoneno` bigint(10) NOT NULL,
  `guardian_phoneno` bigint(10) NOT NULL,
  `sex` enum('Male','Female','Other') NOT NULL,
  `department_id` char(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `students`
--

INSERT INTO `students` (`student_id`, `first_name`, `middle_name`, `last_name`, `email`, `grad_level`, `address`, `city`, `state`, `address_pin`, `father_name`, `mother_name`, `dob`, `bloodgroup`, `doa`, `father_occ`, `mother_occ`, `student_phoneno`, `guardian_phoneno`, `sex`, `department_id`) VALUES
('2022ucp1000', 'Kanishk', 'd', 'Dhebana', 'dhebanakanishk@gmail.com', 'B_Tech', 'a', 'a', 'a', 123456, 'F', 'M', '2003-03-11', 'AB_minus', '2022-04-03', 'FO', 'MO', 9873246745, 8035234092, 'Male', '5'),
('2022ucp1111', 'Ayush', 'R', 'Raghav', 'ayushraghav@gmail.com', 'B_Tech', '12, Nandganv, Nath Ji ki Thadi, Niwaru Road, Jhotwara, Jaipur, Rajasthan', 'Jaipur', 'Rajasthan', 302012, 'A Raghav', 'M ', '2003-01-24', 'A_minus', '2021-07-22', 'Govt. Servant', 'Housewife', 9001155751, 9601755751, 'Male', '5'),
('2022ucp1112', 'Riya', 'S', 'Singh', 'riyasingh@gmail.com', 'B_Tech', '34, Radha Vihar, Raja Park', 'Mumbai', 'Maharashtra', 400001, 'A Singh', 'K Singh', '2003-03-15', 'B_plus', '2021-07-22', 'Businessman', 'Homemaker', 9002155751, 9602755751, 'Female', '5'),
('2022ucp1113', 'Rahul', 'M', 'Mehta', 'rahulmehta@gmail.com', 'B_Tech', '56, Shiv Colony, Shyam Nagar', 'Bangalore', 'Karnataka', 560001, 'V Mehta', 'R Mehta', '2002-12-05', 'AB_plus', '2021-07-22', 'Engineer', 'Teacher', 9003155751, 9603755751, 'Male', '5'),
('2022ucp1114', 'Sneha', 'K', 'Kapoor', 'snehakapoor@gmail.com', 'B_Tech', '78, Raja Park, Ajmer Road', 'Kolkata', 'West Bengal', 700001, 'A Kapoor', 'M Kapoor', '2003-05-20', 'B_minus', '2021-07-22', 'Doctor', 'Nurse', 9004155751, 9604755751, 'Female', '5'),
('2022ucp1115', 'Vivek', 'P', 'Patel', 'vivekpatel@gmail.com', 'B_Tech', '90, Vaishali Nagar', 'Chennai', 'Tamil Nadu', 600001, 'B Patel', 'D Patel', '2002-08-10', 'O_plus', '2021-07-22', 'Businessman', 'Homemaker', 9005155751, 9605755751, 'Male', '5'),
('2022ucp1116', 'Priya', 'A', 'Agarwal', 'priyaagarwal@gmail.com', 'B_Tech', '23, Mansarovar, New Sanganer Road', 'Hyderabad', 'Telangana', 500001, 'K Agarwal', 'S Agarwal', '2003-02-28', 'B_plus', '2021-07-22', 'Professor', 'Homemaker', 9006155751, 9606755751, 'Female', '5'),
('2022ucp1117', 'Aman', 'G', 'Gupta', 'amangupta@gmail.com', 'B_Tech', '45, Malviya Nagar', 'Pune', 'Maharashtra', 411001, 'S Gupta', 'A Gupta', '2002-10-18', 'A_plus', '2021-07-22', 'Engineer', 'Banker', 9007155751, 9607755751, 'Male', '5'),
('2022ucp1118', 'Anjali', 'J', 'Jain', 'anjalijain@gmail.com', 'B_Tech', '67, Jhotwara', 'Ahmedabad', 'Gujarat', 380001, 'V Jain', 'A Jain', '2003-04-12', 'AB_minus', '2021-07-22', 'Doctor', 'Nurse', 9008155751, 9608755751, 'Female', '5'),
('2022ucp1126', 'Kunal', 'S', 'Shah', 'kunalshah@gmail.com', 'B_Tech', '17, Vasant Vihar', 'New Delhi', 'Delhi', 110057, 'R Shah', 'N Shah', '2003-08-09', 'O_plus', '2021-07-22', 'Engineer', 'Homemaker', 9016155751, 9616755751, 'Male', '5'),
('2022ucp1127', 'Pooja', 'A', 'Agrawal', 'poojaagrawal@gmail.com', 'B_Tech', '25, Ashok Nagar', 'Indore', 'Madhya Pradesh', 452001, 'S Agrawal', 'R Agrawal', '2002-11-20', 'B_minus', '2021-07-22', 'Architect', 'Teacher', 9017155751, 9617755751, 'Female', '5'),
('2022ucp1128', 'Rahul', 'K', 'Khatri', 'rahulkhatri@gmail.com', 'B_Tech', '9, Shivaji Nagar', 'Nagpur', 'Maharashtra', 440001, 'A Khatri', 'K Khatri', '2003-04-15', 'AB_plus', '2021-07-22', 'Doctor', 'Nurse', 9018155751, 9618755751, 'Male', '5'),
('2022ucp1129', 'Neha', 'B', 'Bansal', 'nehabansal@gmail.com', 'B_Tech', '43, Civil Lines', 'Allahabad', 'Uttar Pradesh', 211001, 'R Bansal', 'S Bansal', '2002-09-12', 'A_plus', '2021-07-22', 'Entrepreneur', 'Homemaker', 9019155751, 9619755751, 'Female', '5'),
('2022ucp1130', 'Amit', 'G', 'Gupta', 'amitgupta@gmail.com', 'B_Tech', '56, Gokul Nagar', 'Ahmedabad', 'Gujarat', 380001, 'S Gupta', 'A Gupta', '2003-01-30', 'B_plus', '2021-07-22', 'Software Developer', 'Homemaker', 9020155751, 9620755751, 'Male', '5'),
('2022ucp1131', 'Priya', 'M', 'Mehra', 'priyamehra@gmail.com', 'B_Tech', '37, Nehru Nagar', 'Pune', 'Maharashtra', 411001, 'K Mehra', 'P Mehra', '2002-06-27', 'O_minus', '2021-07-22', 'Software Engineer', 'Teacher', 9021155751, 9621755751, 'Female', '5'),
('2022ucp1132', 'Rajesh', 'S', 'Sharma', 'rajeshsharma@gmail.com', 'B_Tech', '78, Malviya Nagar', 'Jaipur', 'Rajasthan', 302018, 'A Sharma', 'R Sharma', '2003-03-08', 'A_minus', '2021-07-22', 'Engineer', 'Homemaker', 9022155751, 9622755751, 'Male', '5'),
('2022ucp1133', 'Anjali', 'R', 'Rastogi', 'anjalirastogi@gmail.com', 'B_Tech', '15, Gomti Nagar', 'Lucknow', 'Uttar Pradesh', 226010, 'K Rastogi', 'S Rastogi', '2002-12-10', 'AB_plus', '2021-07-22', 'Doctor', 'Nurse', 9023155751, 9623755751, 'Female', '5'),
('2022ucp1134', 'Aryan', 'M', 'Malhotra', 'aryanmalhotra@gmail.com', 'B_Tech', '32, Vijay Nagar', 'Ghaziabad', 'Uttar Pradesh', 201001, 'R Malhotra', 'M Malhotra', '2003-05-22', 'B_minus', '2021-07-22', 'Entrepreneur', 'Homemaker', 9024155751, 9624755751, 'Male', '5'),
('2022ucp1135', 'Shreya', 'P', 'Pandey', 'shreyapandey@gmail.com', 'B_Tech', '24, Vikas Nagar', 'Kanpur', 'Uttar Pradesh', 208001, 'A Pandey', 'R Pandey', '2002-07-19', 'A_plus', '2021-07-22', 'Software Developer', 'Homemaker', 9025155751, 9625755751, 'Female', '5');

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
('2022ucp1111', 'student', 'scrypt:32768:8:1$3FQhFKvf8XCLOoh8$0b91c91bb878b83dd76542a4953b1697d2d9c80156cbf7e47d4d671c9b211c77f4963b949f8d03dc7a6b36f9dc2d5fc88565e262c7b0c50cfc45f2eb0c822ea2'),
('2010icp1000', 'instructor', 'scrypt:32768:8:1$GC8B9bfPnewwfZaV$2d02b2592ac6a3f633443d6bb03e847d99976e34c885a7f712c9e555d7f2d18750cf098a029fbf31056109a84b6c9bb8a5e29dff4f4d16a1793a3a3cd7df3c0e'),
('2022ucp1000', 'student', 'scrypt:32768:8:1$lZwlhLHj1kfghYs3$f56720b34610ddfb7811c7c70bdfbdb5f1aa9bfab3135632c778927bcf96690ea628ad3ae61d0f5aff19a95500dbaf4950da191bdf0272bf2e745d023d6dcf04');

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
  ADD PRIMARY KEY (`student_id`),
  ADD KEY `fk_department_id` (`department_id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `enrollments`
--
ALTER TABLE `enrollments`
  MODIFY `enrollment_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT for table `grades`
--
ALTER TABLE `grades`
  MODIFY `grade_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

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

--
-- Constraints for table `students`
--
ALTER TABLE `students`
  ADD CONSTRAINT `fk_department_id` FOREIGN KEY (`department_id`) REFERENCES `departments` (`department_id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
