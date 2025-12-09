-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: localhost
-- Generation Time: Dec 09, 2025 at 03:26 PM
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
-- Database: `hotel_system`
--

-- --------------------------------------------------------

--
-- Table structure for table `bookings`
--

CREATE TABLE `bookings` (
  `booking_id` int(11) NOT NULL,
  `guest_id` int(11) NOT NULL,
  `room_id` int(11) NOT NULL,
  `check_in_date` date NOT NULL,
  `check_out_date` date NOT NULL,
  `number_of_guests` int(11) DEFAULT 1,
  `booking_status` enum('confirmed','checked_in','checked_out','cancelled') DEFAULT 'confirmed'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `bookings`
--

INSERT INTO `bookings` (`booking_id`, `guest_id`, `room_id`, `check_in_date`, `check_out_date`, `number_of_guests`, `booking_status`) VALUES
(1, 1, 3, '2024-11-01', '2024-11-05', 2, 'checked_in'),
(2, 2, 5, '2024-11-03', '2024-11-07', 2, 'confirmed'),
(3, 3, 7, '2024-10-28', '2024-10-31', 3, 'checked_in'),
(4, 4, 1, '2024-11-05', '2024-11-08', 1, 'confirmed');

-- --------------------------------------------------------

--
-- Table structure for table `charges`
--

CREATE TABLE `charges` (
  `charge_id` int(11) NOT NULL,
  `booking_id` int(11) NOT NULL,
  `service_id` int(11) DEFAULT NULL,
  `description` varchar(255) NOT NULL,
  `amount` decimal(10,2) NOT NULL,
  `charge_date` date NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `charges`
--

INSERT INTO `charges` (`charge_id`, `booking_id`, `service_id`, `description`, `amount`, `charge_date`) VALUES
(1, 1, 1, 'Airport Pickup', 50.00, '2024-11-01'),
(2, 1, 4, 'Mini Bar Consumption', 15.00, '2024-11-02'),
(3, 3, 2, 'Spa Treatment', 100.00, '2024-10-29');

-- --------------------------------------------------------

--
-- Table structure for table `guests`
--

CREATE TABLE `guests` (
  `guest_id` int(11) NOT NULL,
  `first_name` varchar(100) NOT NULL,
  `last_name` varchar(100) NOT NULL,
  `email` varchar(150) DEFAULT NULL,
  `phone` varchar(20) DEFAULT NULL,
  `nationality` varchar(50) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `guests`
--

INSERT INTO `guests` (`guest_id`, `first_name`, `last_name`, `email`, `phone`, `nationality`) VALUES
(1, 'John', 'Smith', 'john.smith@email.com', '+63 956 5535 401', 'Filipino'),
(2, 'Emma', 'Johnson', 'emma.j@email.com', '+63 956 5535 401', 'Filipino'),
(3, 'Michael', 'Brown', 'michael.b@email.com', '+63 956 5535 401', 'Filipino'),
(4, 'Sarah', 'Davis', 'sarah.d@email.com', '+63 956 5535 401', 'Filipino'),
(5, 'David', 'Wilson', 'david.w@email.com', '+63 956 5535 401', 'Filipino');

-- --------------------------------------------------------

--
-- Table structure for table `guest_feedback`
--

CREATE TABLE `guest_feedback` (
  `feedback_id` int(11) NOT NULL,
  `guest_id` int(11) NOT NULL,
  `booking_id` int(11) DEFAULT NULL,
  `overall_rating` int(11) DEFAULT NULL CHECK (`overall_rating` between 1 and 5),
  `service_rating` int(11) DEFAULT NULL CHECK (`service_rating` between 1 and 5),
  `comments` text DEFAULT NULL,
  `feedback_date` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `guest_feedback`
--

INSERT INTO `guest_feedback` (`feedback_id`, `guest_id`, `booking_id`, `overall_rating`, `service_rating`, `comments`, `feedback_date`) VALUES
(1, 1, 1, 5, 5, 'Excellent service and beautiful room!', '2025-10-31 14:13:42'),
(2, 3, 3, 4, 4, 'Great stay, food was amazing', '2025-10-31 14:13:42');

-- --------------------------------------------------------

--
-- Table structure for table `guest_preferences`
--

CREATE TABLE `guest_preferences` (
  `preference_id` int(11) NOT NULL,
  `guest_id` int(11) NOT NULL,
  `preference_type` varchar(50) DEFAULT NULL,
  `preference_value` text DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `guest_preferences`
--

INSERT INTO `guest_preferences` (`preference_id`, `guest_id`, `preference_type`, `preference_value`) VALUES
(1, 1, 'Room Temperature', '22°C'),
(2, 1, 'Pillow Type', 'Firm'),
(3, 3, 'Dietary', 'Vegetarian options preferred');

-- --------------------------------------------------------

--
-- Table structure for table `housekeeping_tasks`
--

CREATE TABLE `housekeeping_tasks` (
  `task_id` int(11) NOT NULL,
  `room_id` int(11) NOT NULL,
  `task_type` enum('cleaning','inspection','turndown') DEFAULT 'cleaning',
  `task_status` enum('pending','in_progress','completed') DEFAULT 'pending',
  `assigned_to` varchar(100) DEFAULT NULL,
  `scheduled_date` date DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `housekeeping_tasks`
--

INSERT INTO `housekeeping_tasks` (`task_id`, `room_id`, `task_type`, `task_status`, `assigned_to`, `scheduled_date`) VALUES
(1, 6, 'cleaning', 'in_progress', 'Maria Garcia', '2024-10-31'),
(2, 1, 'inspection', 'pending', 'Maria Garcia', '2024-11-01'),
(3, 4, 'cleaning', 'completed', 'Anna Lee', '2024-10-30');

-- --------------------------------------------------------

--
-- Table structure for table `inventory_categories`
--

CREATE TABLE `inventory_categories` (
  `category_id` int(11) NOT NULL,
  `category_name` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `inventory_categories`
--

INSERT INTO `inventory_categories` (`category_id`, `category_name`) VALUES
(1, 'Cleaning Supplies'),
(2, 'Linens'),
(3, 'Toiletries'),
(4, 'Food Ingredients'),
(5, 'Beverages');

-- --------------------------------------------------------

--
-- Table structure for table `inventory_items`
--

CREATE TABLE `inventory_items` (
  `item_id` int(11) NOT NULL,
  `item_name` varchar(150) NOT NULL,
  `category_id` int(11) NOT NULL,
  `quantity_in_stock` decimal(10,2) DEFAULT 0.00,
  `unit` varchar(20) DEFAULT 'pcs',
  `minimum_quantity` decimal(10,2) DEFAULT 10.00,
  `unit_cost` decimal(10,2) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `inventory_items`
--

INSERT INTO `inventory_items` (`item_id`, `item_name`, `category_id`, `quantity_in_stock`, `unit`, `minimum_quantity`, `unit_cost`) VALUES
(1, 'Toilet Paper', 1, 500.00, 'rolls', 100.00, 0.50),
(2, 'Bed Sheets', 2, 200.00, 'pcs', 50.00, 15.00),
(3, 'Shampoo', 3, 150.00, 'bottles', 40.00, 2.00),
(4, 'Towels', 2, 300.00, 'pcs', 80.00, 8.00),
(5, 'Coffee Beans', 5, 50.00, 'kg', 10.00, 20.00),
(6, 'Rice', 4, 95.20, 'kg', 25.00, 3.00),
(7, 'Romaine Lettuce', 4, 50.00, 'kg', 15.00, 3.50),
(8, 'Caesar Dressing', 4, 30.00, 'liters', 10.00, 8.00),
(9, 'Parmesan Cheese', 4, 25.00, 'kg', 8.00, 12.00),
(10, 'Croutons', 4, 40.00, 'kg', 10.00, 4.00),
(11, 'Tomatoes', 4, 80.00, 'kg', 20.00, 2.50),
(12, 'Cream', 4, 45.00, 'liters', 15.00, 6.00),
(13, 'Onions', 4, 60.00, 'kg', 20.00, 1.50),
(14, 'Vegetable Stock', 4, 35.00, 'liters', 10.00, 4.50),
(15, 'Salmon Fillet', 4, 29.50, 'kg', 10.00, 25.00),
(16, 'Lemon', 4, 49.96, 'kg', 15.00, 1.00),
(17, 'Butter', 4, 39.96, 'kg', 12.00, 5.00),
(18, 'Herbs (Mixed)', 4, 24.98, 'kg', 8.00, 7.00),
(19, 'Beef Tenderloin', 4, 35.00, 'kg', 10.00, 30.00),
(20, 'Garlic', 4, 45.00, 'kg', 15.00, 2.00),
(21, 'Black Pepper', 4, 20.00, 'kg', 5.00, 8.00),
(22, 'Olive Oil', 4, 55.00, 'liters', 18.00, 10.00),
(23, 'Flour', 4, 100.00, 'kg', 30.00, 2.00),
(24, 'Cocoa Powder', 4, 30.00, 'kg', 10.00, 15.00),
(25, 'Sugar', 4, 80.00, 'kg', 25.00, 1.80),
(26, 'Eggs', 4, 120.00, 'pcs', 40.00, 0.50),
(27, 'Chocolate Chips', 4, 25.00, 'kg', 8.00, 12.00),
(28, 'Espresso Beans', 5, 40.00, 'kg', 12.00, 22.00),
(29, 'Milk', 5, 100.00, 'liters', 30.00, 3.50),
(30, 'Fresh Oranges', 4, 68.50, 'kg', 20.00, 4.00),
(31, 'Bread', 4, 60.00, 'loaves', 20.00, 2.50),
(32, 'Jam', 4, 35.00, 'jars', 10.00, 5.00),
(33, 'Bacon', 4, 40.00, 'kg', 12.00, 8.00),
(34, 'Sausages', 4, 35.00, 'kg', 10.00, 9.00),
(35, 'Salt', 4, 50.00, 'kg', 15.00, 1.00),
(36, 'Potatoes', 4, 90.00, 'kg', 25.00, 2.20),
(37, 'Vegetables (Mixed)', 4, 65.00, 'kg', 20.00, 4.50),
(38, 'Tea Bags', 5, 200.00, 'boxes', 50.00, 0.30),
(39, 'Mineral Water', 5, 150.00, 'bottles', 40.00, 1.00),
(40, 'Soft Drinks', 5, 100.00, 'cans', 30.00, 1.50);

-- --------------------------------------------------------

--
-- Table structure for table `inventory_transactions`
--

CREATE TABLE `inventory_transactions` (
  `transaction_id` int(11) NOT NULL,
  `item_id` int(11) NOT NULL,
  `transaction_type` enum('restock','usage','adjustment') NOT NULL,
  `quantity` decimal(10,2) NOT NULL,
  `transaction_date` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `inventory_transactions`
--

INSERT INTO `inventory_transactions` (`transaction_id`, `item_id`, `transaction_type`, `quantity`, `transaction_date`) VALUES
(1, 1, 'restock', 200.00, '2025-10-31 14:13:42'),
(2, 2, 'usage', 10.00, '2025-10-31 14:13:42'),
(3, 3, 'restock', 50.00, '2025-10-31 14:13:42'),
(4, 6, 'usage', 0.50, '2025-11-01 03:32:49'),
(5, 6, 'usage', 1.00, '2025-11-01 03:33:33'),
(6, 6, 'usage', 1.00, '2025-11-01 03:38:25'),
(7, 6, 'usage', 1.00, '2025-11-01 03:53:51'),
(8, 6, 'usage', 1.00, '2025-12-09 13:08:35'),
(9, 15, 'usage', -0.50, '2025-12-09 14:12:32'),
(10, 16, 'usage', -0.04, '2025-12-09 14:12:32'),
(11, 17, 'usage', -0.04, '2025-12-09 14:12:32'),
(12, 18, 'usage', -0.02, '2025-12-09 14:12:32'),
(13, 6, 'usage', -0.30, '2025-12-09 14:12:32'),
(14, 30, 'usage', -1.50, '2025-12-09 14:14:27');

-- --------------------------------------------------------

--
-- Table structure for table `loyalty_program`
--

CREATE TABLE `loyalty_program` (
  `loyalty_id` int(11) NOT NULL,
  `guest_id` int(11) NOT NULL,
  `membership_level` enum('bronze','silver','gold','platinum') DEFAULT 'bronze',
  `points_balance` int(11) DEFAULT 0,
  `member_since` date NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `loyalty_program`
--

INSERT INTO `loyalty_program` (`loyalty_id`, `guest_id`, `membership_level`, `points_balance`, `member_since`) VALUES
(1, 1, 'silver', 1500, '2023-06-15'),
(2, 2, 'bronze', 500, '2024-03-20'),
(3, 3, 'gold', 3500, '2022-01-10');

-- --------------------------------------------------------

--
-- Table structure for table `maintenance_requests`
--

CREATE TABLE `maintenance_requests` (
  `request_id` int(11) NOT NULL,
  `room_id` int(11) NOT NULL,
  `issue_type` varchar(100) NOT NULL,
  `description` text DEFAULT NULL,
  `priority` enum('low','medium','high','urgent') DEFAULT 'medium',
  `status` enum('pending','in_progress','completed') DEFAULT 'pending',
  `reported_date` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `maintenance_requests`
--

INSERT INTO `maintenance_requests` (`request_id`, `room_id`, `issue_type`, `description`, `priority`, `status`, `reported_date`) VALUES
(1, 2, 'Plumbing', 'Leaking faucet in bathroom', 'medium', 'pending', '2025-10-31 14:13:42'),
(2, 4, 'Electrical', 'Light fixture not working', 'high', 'in_progress', '2025-10-31 14:13:42');

-- --------------------------------------------------------

--
-- Table structure for table `menu_categories`
--

CREATE TABLE `menu_categories` (
  `category_id` int(11) NOT NULL,
  `category_name` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `menu_categories`
--

INSERT INTO `menu_categories` (`category_id`, `category_name`) VALUES
(1, 'Appetizers'),
(2, 'Main Course'),
(3, 'Desserts'),
(4, 'Beverages'),
(5, 'Breakfast');

-- --------------------------------------------------------

--
-- Table structure for table `menu_items`
--

CREATE TABLE `menu_items` (
  `menu_item_id` int(11) NOT NULL,
  `item_name` varchar(150) NOT NULL,
  `category_id` int(11) NOT NULL,
  `price` decimal(10,2) NOT NULL,
  `is_available` tinyint(1) DEFAULT 1
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `menu_items`
--

INSERT INTO `menu_items` (`menu_item_id`, `item_name`, `category_id`, `price`, `is_available`) VALUES
(1, 'Caesar Salad', 1, 221.00, 1),
(2, 'Tomato Soup', 1, 160.00, 1),
(3, 'Grilled Salmon', 2, 350.00, 1),
(4, 'Beef Steak', 2, 350.00, 1),
(5, 'Chocolate Cake', 3, 120.00, 1),
(6, 'Cappuccino', 4, 135.00, 1),
(7, 'Orange Juice', 4, 90.00, 1),
(8, 'Continental Breakfast', 5, 120.00, 1);

-- --------------------------------------------------------

--
-- Table structure for table `menu_item_ingredients`
--

CREATE TABLE `menu_item_ingredients` (
  `ingredient_id` int(11) NOT NULL,
  `menu_item_id` int(11) NOT NULL,
  `inventory_item_id` int(11) NOT NULL,
  `quantity_needed` decimal(10,2) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `menu_item_ingredients`
--

INSERT INTO `menu_item_ingredients` (`ingredient_id`, `menu_item_id`, `inventory_item_id`, `quantity_needed`) VALUES
(1, 1, 7, 0.15),
(2, 1, 8, 0.05),
(3, 1, 9, 0.03),
(4, 1, 10, 0.02),
(5, 2, 11, 0.20),
(6, 2, 12, 0.05),
(7, 2, 13, 0.03),
(8, 2, 14, 0.10),
(9, 3, 15, 0.25),
(10, 3, 16, 0.02),
(11, 3, 17, 0.02),
(12, 3, 18, 0.01),
(13, 3, 6, 0.15),
(14, 4, 19, 0.30),
(15, 4, 20, 0.01),
(16, 4, 21, 0.01),
(17, 4, 22, 0.02),
(18, 4, 36, 0.20),
(19, 5, 23, 0.10),
(20, 5, 24, 0.05),
(21, 5, 25, 0.08),
(22, 5, 26, 2.00),
(23, 5, 27, 0.05),
(24, 6, 28, 0.02),
(25, 6, 29, 0.15),
(26, 7, 30, 0.30),
(27, 8, 31, 0.10),
(28, 8, 32, 0.03),
(29, 8, 33, 0.05),
(30, 8, 34, 0.05),
(31, 8, 26, 2.00),
(32, 8, 7, 0.30);

-- --------------------------------------------------------

--
-- Table structure for table `order_items`
--

CREATE TABLE `order_items` (
  `order_item_id` int(11) NOT NULL,
  `order_id` int(11) NOT NULL,
  `menu_item_id` int(11) NOT NULL,
  `quantity` int(11) DEFAULT 1,
  `unit_price` decimal(10,2) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `order_items`
--

INSERT INTO `order_items` (`order_item_id`, `order_id`, `menu_item_id`, `quantity`, `unit_price`) VALUES
(1, 1, 3, 1, 28.00),
(2, 1, 6, 2, 5.00),
(3, 1, 7, 1, 6.00),
(4, 2, 4, 2, 35.00),
(5, 2, 1, 1, 12.00),
(6, 3, 2, 1, 160.00),
(7, 4, 3, 2, 350.00),
(8, 5, 1, 2, 220.00),
(9, 6, 1, 2, 220.00),
(10, 7, 4, 2, 350.00),
(11, 8, 3, 2, 350.00),
(12, 9, 7, 5, 90.00);

-- --------------------------------------------------------

--
-- Table structure for table `payments`
--

CREATE TABLE `payments` (
  `payment_id` int(11) NOT NULL,
  `booking_id` int(11) NOT NULL,
  `payment_method` enum('cash','credit_card','debit_card','mobile') NOT NULL,
  `amount` decimal(10,2) NOT NULL,
  `payment_date` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `payments`
--

INSERT INTO `payments` (`payment_id`, `booking_id`, `payment_method`, `amount`, `payment_date`) VALUES
(1, 1, 'credit_card', 200.00, '2024-10-31 16:00:00'),
(2, 3, 'credit_card', 500.00, '2024-10-27 16:00:00');

-- --------------------------------------------------------

--
-- Table structure for table `restaurant_orders`
--

CREATE TABLE `restaurant_orders` (
  `order_id` int(11) NOT NULL,
  `booking_id` int(11) DEFAULT NULL,
  `guest_id` int(11) DEFAULT NULL,
  `order_type` enum('dine_in','room_service','takeaway') DEFAULT 'dine_in',
  `total_amount` decimal(10,2) NOT NULL,
  `order_status` enum('pending','preparing','completed','cancelled') DEFAULT 'pending',
  `order_date` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `restaurant_orders`
--

INSERT INTO `restaurant_orders` (`order_id`, `booking_id`, `guest_id`, `order_type`, `total_amount`, `order_status`, `order_date`) VALUES
(1, 1, 1, 'room_service', 45.00, 'completed', '2025-10-31 14:13:42'),
(2, 3, 3, 'dine_in', 75.00, 'completed', '2025-10-31 14:13:42'),
(3, 1, 1, 'room_service', 160.00, 'pending', '2025-11-01 03:32:49'),
(4, 1, 1, 'dine_in', 700.00, 'pending', '2025-11-01 03:33:33'),
(5, 1, 1, 'dine_in', 440.00, 'pending', '2025-11-01 03:38:25'),
(6, 1, 1, 'room_service', 440.00, 'pending', '2025-11-01 03:53:51'),
(7, 1, 1, 'room_service', 700.00, 'pending', '2025-12-09 13:08:35'),
(8, 1, 1, 'dine_in', 700.00, 'pending', '2025-12-09 14:12:32'),
(9, 1, 1, 'room_service', 450.00, 'pending', '2025-12-09 14:14:27');

-- --------------------------------------------------------

--
-- Table structure for table `rooms`
--

CREATE TABLE `rooms` (
  `room_id` int(11) NOT NULL,
  `room_number` varchar(10) NOT NULL,
  `room_type_id` int(11) NOT NULL,
  `floor_number` int(11) DEFAULT NULL,
  `status` enum('available','occupied','cleaning','maintenance') DEFAULT 'available'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `rooms`
--

INSERT INTO `rooms` (`room_id`, `room_number`, `room_type_id`, `floor_number`, `status`) VALUES
(1, '101', 1, 1, 'available'),
(2, '102', 1, 1, 'available'),
(3, '201', 2, 2, 'occupied'),
(4, '202', 2, 2, 'available'),
(5, '301', 3, 3, 'available'),
(6, '302', 3, 3, 'cleaning'),
(7, '401', 4, 4, 'available'),
(8, '501', 5, 5, 'available');

-- --------------------------------------------------------

--
-- Table structure for table `room_types`
--

CREATE TABLE `room_types` (
  `room_type_id` int(11) NOT NULL,
  `type_name` varchar(50) NOT NULL,
  `base_rate` decimal(10,2) NOT NULL,
  `max_occupancy` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `room_types`
--

INSERT INTO `room_types` (`room_type_id`, `type_name`, `base_rate`, `max_occupancy`) VALUES
(1, 'Standard Single', 100.00, 1),
(2, 'Standard Double', 150.00, 2),
(3, 'Deluxe Suite', 250.00, 3),
(4, 'Executive Suite', 400.00, 4),
(5, 'Presidential Suite', 600.00, 6);

-- --------------------------------------------------------

--
-- Table structure for table `services`
--

CREATE TABLE `services` (
  `service_id` int(11) NOT NULL,
  `service_name` varchar(100) NOT NULL,
  `service_category` varchar(50) DEFAULT NULL,
  `price` decimal(10,2) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `services`
--

INSERT INTO `services` (`service_id`, `service_name`, `service_category`, `price`) VALUES
(1, 'Airport Transfer', 'Transportation', 50.00),
(2, 'Spa Massage', 'Spa', 100.00),
(3, 'Laundry Service', 'Housekeeping', 20.00),
(4, 'Mini Bar', 'Room Service', 15.00),
(5, 'Late Checkout', 'Front Desk', 40.00);

-- --------------------------------------------------------

--
-- Table structure for table `staff`
--

CREATE TABLE `staff` (
  `staff_id` int(11) NOT NULL,
  `username` varchar(50) NOT NULL,
  `first_name` varchar(100) NOT NULL,
  `last_name` varchar(100) NOT NULL,
  `email` varchar(150) NOT NULL,
  `password` varchar(255) DEFAULT NULL,
  `role` enum('admin','front_desk','housekeeping','maintenance','billing','restaurant','kitchen','manager') NOT NULL,
  `is_active` tinyint(1) DEFAULT 1
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `staff`
--

INSERT INTO `staff` (`staff_id`, `username`, `first_name`, `last_name`, `email`, `password`, `role`, `is_active`) VALUES
(1, 'admin', 'Admin', 'User', 'admin@hotel.com', 'admin123', 'admin', 1),
(2, 'frontdesk1', 'Sarah', 'Johnson', 'sarah@hotel.com', NULL, 'front_desk', 1),
(3, 'housekeeper1', 'Maria', 'Garcia', 'maria@hotel.com', NULL, 'housekeeping', 1),
(4, 'maintenance1', 'Mike', 'Wilson', 'mike@hotel.com', NULL, 'maintenance', 1),
(5, 'chef1', 'Gordon', 'Smith', 'gordon@hotel.com', NULL, 'kitchen', 1);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `bookings`
--
ALTER TABLE `bookings`
  ADD PRIMARY KEY (`booking_id`),
  ADD KEY `guest_id` (`guest_id`),
  ADD KEY `room_id` (`room_id`);

--
-- Indexes for table `charges`
--
ALTER TABLE `charges`
  ADD PRIMARY KEY (`charge_id`),
  ADD KEY `booking_id` (`booking_id`),
  ADD KEY `service_id` (`service_id`);

--
-- Indexes for table `guests`
--
ALTER TABLE `guests`
  ADD PRIMARY KEY (`guest_id`),
  ADD UNIQUE KEY `email` (`email`);

--
-- Indexes for table `guest_feedback`
--
ALTER TABLE `guest_feedback`
  ADD PRIMARY KEY (`feedback_id`),
  ADD KEY `guest_id` (`guest_id`),
  ADD KEY `booking_id` (`booking_id`);

--
-- Indexes for table `guest_preferences`
--
ALTER TABLE `guest_preferences`
  ADD PRIMARY KEY (`preference_id`),
  ADD KEY `guest_id` (`guest_id`);

--
-- Indexes for table `housekeeping_tasks`
--
ALTER TABLE `housekeeping_tasks`
  ADD PRIMARY KEY (`task_id`),
  ADD KEY `room_id` (`room_id`);

--
-- Indexes for table `inventory_categories`
--
ALTER TABLE `inventory_categories`
  ADD PRIMARY KEY (`category_id`);

--
-- Indexes for table `inventory_items`
--
ALTER TABLE `inventory_items`
  ADD PRIMARY KEY (`item_id`),
  ADD KEY `category_id` (`category_id`);

--
-- Indexes for table `inventory_transactions`
--
ALTER TABLE `inventory_transactions`
  ADD PRIMARY KEY (`transaction_id`),
  ADD KEY `item_id` (`item_id`);

--
-- Indexes for table `loyalty_program`
--
ALTER TABLE `loyalty_program`
  ADD PRIMARY KEY (`loyalty_id`),
  ADD UNIQUE KEY `guest_id` (`guest_id`);

--
-- Indexes for table `maintenance_requests`
--
ALTER TABLE `maintenance_requests`
  ADD PRIMARY KEY (`request_id`),
  ADD KEY `room_id` (`room_id`);

--
-- Indexes for table `menu_categories`
--
ALTER TABLE `menu_categories`
  ADD PRIMARY KEY (`category_id`);

--
-- Indexes for table `menu_items`
--
ALTER TABLE `menu_items`
  ADD PRIMARY KEY (`menu_item_id`),
  ADD KEY `category_id` (`category_id`);

--
-- Indexes for table `menu_item_ingredients`
--
ALTER TABLE `menu_item_ingredients`
  ADD PRIMARY KEY (`ingredient_id`),
  ADD KEY `menu_item_id` (`menu_item_id`),
  ADD KEY `inventory_item_id` (`inventory_item_id`);

--
-- Indexes for table `order_items`
--
ALTER TABLE `order_items`
  ADD PRIMARY KEY (`order_item_id`),
  ADD KEY `order_id` (`order_id`),
  ADD KEY `menu_item_id` (`menu_item_id`);

--
-- Indexes for table `payments`
--
ALTER TABLE `payments`
  ADD PRIMARY KEY (`payment_id`),
  ADD KEY `booking_id` (`booking_id`);

--
-- Indexes for table `restaurant_orders`
--
ALTER TABLE `restaurant_orders`
  ADD PRIMARY KEY (`order_id`),
  ADD KEY `booking_id` (`booking_id`),
  ADD KEY `guest_id` (`guest_id`);

--
-- Indexes for table `rooms`
--
ALTER TABLE `rooms`
  ADD PRIMARY KEY (`room_id`),
  ADD UNIQUE KEY `room_number` (`room_number`),
  ADD KEY `room_type_id` (`room_type_id`);

--
-- Indexes for table `room_types`
--
ALTER TABLE `room_types`
  ADD PRIMARY KEY (`room_type_id`);

--
-- Indexes for table `services`
--
ALTER TABLE `services`
  ADD PRIMARY KEY (`service_id`);

--
-- Indexes for table `staff`
--
ALTER TABLE `staff`
  ADD PRIMARY KEY (`staff_id`),
  ADD UNIQUE KEY `username` (`username`),
  ADD UNIQUE KEY `email` (`email`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `bookings`
--
ALTER TABLE `bookings`
  MODIFY `booking_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT for table `charges`
--
ALTER TABLE `charges`
  MODIFY `charge_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `guests`
--
ALTER TABLE `guests`
  MODIFY `guest_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT for table `guest_feedback`
--
ALTER TABLE `guest_feedback`
  MODIFY `feedback_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `guest_preferences`
--
ALTER TABLE `guest_preferences`
  MODIFY `preference_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `housekeeping_tasks`
--
ALTER TABLE `housekeeping_tasks`
  MODIFY `task_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `inventory_categories`
--
ALTER TABLE `inventory_categories`
  MODIFY `category_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT for table `inventory_items`
--
ALTER TABLE `inventory_items`
  MODIFY `item_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=41;

--
-- AUTO_INCREMENT for table `inventory_transactions`
--
ALTER TABLE `inventory_transactions`
  MODIFY `transaction_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=15;

--
-- AUTO_INCREMENT for table `loyalty_program`
--
ALTER TABLE `loyalty_program`
  MODIFY `loyalty_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `maintenance_requests`
--
ALTER TABLE `maintenance_requests`
  MODIFY `request_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `menu_categories`
--
ALTER TABLE `menu_categories`
  MODIFY `category_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT for table `menu_items`
--
ALTER TABLE `menu_items`
  MODIFY `menu_item_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;

--
-- AUTO_INCREMENT for table `menu_item_ingredients`
--
ALTER TABLE `menu_item_ingredients`
  MODIFY `ingredient_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=33;

--
-- AUTO_INCREMENT for table `order_items`
--
ALTER TABLE `order_items`
  MODIFY `order_item_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=13;

--
-- AUTO_INCREMENT for table `payments`
--
ALTER TABLE `payments`
  MODIFY `payment_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `restaurant_orders`
--
ALTER TABLE `restaurant_orders`
  MODIFY `order_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=10;

--
-- AUTO_INCREMENT for table `rooms`
--
ALTER TABLE `rooms`
  MODIFY `room_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;

--
-- AUTO_INCREMENT for table `room_types`
--
ALTER TABLE `room_types`
  MODIFY `room_type_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT for table `services`
--
ALTER TABLE `services`
  MODIFY `service_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT for table `staff`
--
ALTER TABLE `staff`
  MODIFY `staff_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `bookings`
--
ALTER TABLE `bookings`
  ADD CONSTRAINT `bookings_ibfk_1` FOREIGN KEY (`guest_id`) REFERENCES `guests` (`guest_id`) ON DELETE CASCADE,
  ADD CONSTRAINT `bookings_ibfk_2` FOREIGN KEY (`room_id`) REFERENCES `rooms` (`room_id`) ON DELETE CASCADE;

--
-- Constraints for table `charges`
--
ALTER TABLE `charges`
  ADD CONSTRAINT `charges_ibfk_1` FOREIGN KEY (`booking_id`) REFERENCES `bookings` (`booking_id`) ON DELETE CASCADE,
  ADD CONSTRAINT `charges_ibfk_2` FOREIGN KEY (`service_id`) REFERENCES `services` (`service_id`) ON DELETE SET NULL;

--
-- Constraints for table `guest_feedback`
--
ALTER TABLE `guest_feedback`
  ADD CONSTRAINT `guest_feedback_ibfk_1` FOREIGN KEY (`guest_id`) REFERENCES `guests` (`guest_id`) ON DELETE CASCADE,
  ADD CONSTRAINT `guest_feedback_ibfk_2` FOREIGN KEY (`booking_id`) REFERENCES `bookings` (`booking_id`) ON DELETE SET NULL;

--
-- Constraints for table `guest_preferences`
--
ALTER TABLE `guest_preferences`
  ADD CONSTRAINT `guest_preferences_ibfk_1` FOREIGN KEY (`guest_id`) REFERENCES `guests` (`guest_id`) ON DELETE CASCADE;

--
-- Constraints for table `housekeeping_tasks`
--
ALTER TABLE `housekeeping_tasks`
  ADD CONSTRAINT `housekeeping_tasks_ibfk_1` FOREIGN KEY (`room_id`) REFERENCES `rooms` (`room_id`) ON DELETE CASCADE;

--
-- Constraints for table `inventory_items`
--
ALTER TABLE `inventory_items`
  ADD CONSTRAINT `inventory_items_ibfk_1` FOREIGN KEY (`category_id`) REFERENCES `inventory_categories` (`category_id`) ON DELETE CASCADE;

--
-- Constraints for table `inventory_transactions`
--
ALTER TABLE `inventory_transactions`
  ADD CONSTRAINT `inventory_transactions_ibfk_1` FOREIGN KEY (`item_id`) REFERENCES `inventory_items` (`item_id`) ON DELETE CASCADE;

--
-- Constraints for table `loyalty_program`
--
ALTER TABLE `loyalty_program`
  ADD CONSTRAINT `loyalty_program_ibfk_1` FOREIGN KEY (`guest_id`) REFERENCES `guests` (`guest_id`) ON DELETE CASCADE;

--
-- Constraints for table `maintenance_requests`
--
ALTER TABLE `maintenance_requests`
  ADD CONSTRAINT `maintenance_requests_ibfk_1` FOREIGN KEY (`room_id`) REFERENCES `rooms` (`room_id`) ON DELETE CASCADE;

--
-- Constraints for table `menu_items`
--
ALTER TABLE `menu_items`
  ADD CONSTRAINT `menu_items_ibfk_1` FOREIGN KEY (`category_id`) REFERENCES `menu_categories` (`category_id`) ON DELETE CASCADE;

--
-- Constraints for table `menu_item_ingredients`
--
ALTER TABLE `menu_item_ingredients`
  ADD CONSTRAINT `menu_item_ingredients_ibfk_1` FOREIGN KEY (`menu_item_id`) REFERENCES `menu_items` (`menu_item_id`) ON DELETE CASCADE,
  ADD CONSTRAINT `menu_item_ingredients_ibfk_2` FOREIGN KEY (`inventory_item_id`) REFERENCES `inventory_items` (`item_id`) ON DELETE CASCADE;

--
-- Constraints for table `order_items`
--
ALTER TABLE `order_items`
  ADD CONSTRAINT `order_items_ibfk_1` FOREIGN KEY (`order_id`) REFERENCES `restaurant_orders` (`order_id`) ON DELETE CASCADE,
  ADD CONSTRAINT `order_items_ibfk_2` FOREIGN KEY (`menu_item_id`) REFERENCES `menu_items` (`menu_item_id`) ON DELETE CASCADE;

--
-- Constraints for table `payments`
--
ALTER TABLE `payments`
  ADD CONSTRAINT `payments_ibfk_1` FOREIGN KEY (`booking_id`) REFERENCES `bookings` (`booking_id`) ON DELETE CASCADE;

--
-- Constraints for table `restaurant_orders`
--
ALTER TABLE `restaurant_orders`
  ADD CONSTRAINT `restaurant_orders_ibfk_1` FOREIGN KEY (`booking_id`) REFERENCES `bookings` (`booking_id`) ON DELETE SET NULL,
  ADD CONSTRAINT `restaurant_orders_ibfk_2` FOREIGN KEY (`guest_id`) REFERENCES `guests` (`guest_id`) ON DELETE SET NULL;

--
-- Constraints for table `rooms`
--
ALTER TABLE `rooms`
  ADD CONSTRAINT `rooms_ibfk_1` FOREIGN KEY (`room_type_id`) REFERENCES `room_types` (`room_type_id`) ON DELETE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
