use ecommerce;

CREATE TABLE `users` (
  `id` BIGINT PRIMARY KEY AUTO_INCREMENT,
  `full_name` varchar(255),
  `email` varchar(255) UNIQUE,
  `gender` varchar(20),
  `date_of_birth` date,
  `created_at` datetime,
  `user_type` ENUM('customer', 'merchant') DEFAULT 'customer'
);

CREATE TABLE `merchants` (
  `id` BIGINT PRIMARY KEY AUTO_INCREMENT,
  `admin_id` BIGINT,
  `merchant_name` varchar(255),
  `created_at` datetime
);

CREATE TABLE `categories` (
  `id` BIGINT PRIMARY KEY AUTO_INCREMENT,
  `cat_name` varchar(255),
  `parent_id` BIGINT
);

CREATE TABLE `products` (
  `id` BIGINT PRIMARY KEY AUTO_INCREMENT,
  `name` varchar(255),
  `merchant_id` BIGINT NOT NULL,
  `price` decimal(10,2),
  `status` varchar(20),
  `created_at` datetime,
  `category_id` BIGINT
);

CREATE TABLE `orders` (
  `id` BIGINT PRIMARY KEY AUTO_INCREMENT,
  `user_id` BIGINT NOT NULL,
  `status` varchar(20),
  `created_at` datetime
);

CREATE TABLE `order_items` (
  `id` BIGINT PRIMARY KEY AUTO_INCREMENT,
  `order_id` BIGINT,
  `product_id` BIGINT,
  `quantity` int
);

CREATE TABLE `carts` (
  `id` BIGINT PRIMARY KEY AUTO_INCREMENT,
  `user_id` BIGINT NOT NULL,
  `created_at` datetime,
  `updated_at` datetime,
  `is_active` BOOLEAN DEFAULT TRUE,
  FOREIGN KEY (`user_id`) REFERENCES `users`(`id`)
);

CREATE TABLE `cart_items` (
  `id` BIGINT PRIMARY KEY AUTO_INCREMENT,
  `cart_id` BIGINT NOT NULL,
  `product_id` BIGINT NOT NULL,
  `quantity` INT DEFAULT 1,
  FOREIGN KEY (`cart_id`) REFERENCES `carts`(`id`),
  FOREIGN KEY (`product_id`) REFERENCES `products`(`id`)
);


ALTER TABLE `orders` ADD FOREIGN KEY (`user_id`) REFERENCES `users` (`id`);

ALTER TABLE `order_items` ADD FOREIGN KEY (`order_id`) REFERENCES `orders` (`id`);

ALTER TABLE `order_items` ADD FOREIGN KEY (`product_id`) REFERENCES `products` (`id`);

ALTER TABLE `products` ADD FOREIGN KEY (`merchant_id`) REFERENCES `merchants` (`id`);

ALTER TABLE `products` ADD FOREIGN KEY (`category_id`) REFERENCES `categories` (`id`);

ALTER TABLE `categories` ADD FOREIGN KEY (`parent_id`) REFERENCES `categories` (`id`);

ALTER TABLE `merchants` ADD FOREIGN KEY (`admin_id`) REFERENCES `users` (`id`); 

-- ALTER TABLE `users` ADD COLUMN `user_type` ENUM('customer', 'merchant') DEFAULT 'customer';