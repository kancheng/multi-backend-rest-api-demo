CREATE DATABASE IF NOT EXISTS smart_pantry
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;

CREATE USER IF NOT EXISTS 'smart_pantry_user'@'localhost' IDENTIFIED BY 'smart_pantry_pass';
GRANT ALL PRIVILEGES ON smart_pantry.* TO 'smart_pantry_user'@'localhost';
FLUSH PRIVILEGES;
