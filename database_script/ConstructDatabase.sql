USE `sleipnir`;

CREATE TABLE IF NOT EXISTS `tenants` (
	`id` INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
  	`tenant_name` varchar(50) NOT NULL UNIQUE) DEFAULT CHARSET=utf8;

CREATE TABLE IF NOT EXISTS `users` (
	`id` INT NOT NULL AUTO_INCREMENT,
  	`username` varchar(50) NOT NULL UNIQUE,
  	`password` varchar(255) NOT NULL,
  	`email` varchar(100) NOT NULL UNIQUE,
    `tenant_id` INT NOT NULL,
	PRIMARY KEY (`id`),
    CONSTRAINT FK_tenants_users FOREIGN KEY (`tenant_id`) REFERENCES tenants(`id`)) DEFAULT CHARSET=utf8;
    
CREATE TABLE IF NOT EXISTS `rights` (
	`id` INT NOT NULL AUTO_INCREMENT,
  	`right` varchar(50) NOT NULL UNIQUE,
	PRIMARY KEY (`id`)) DEFAULT CHARSET=utf8;

CREATE TABLE IF NOT EXISTS `users_rights` (
	`id` INT NOT NULL AUTO_INCREMENT,
    `user_id` INT NOT NULL,
    `right_id` INT NOT NULL,
    PRIMARY KEY (`id`),
    CONSTRAINT FK_users_users_rights FOREIGN KEY (`user_id`) REFERENCES users(`id`),
    CONSTRAINT FK_rights_users_rights FOREIGN KEY (`right_id`) REFERENCES rights(`id`)) DEFAULT CHARSET=utf8;