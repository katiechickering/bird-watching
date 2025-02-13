-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema bird_watching_schema
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema bird_watching_schema
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `bird_watching_schema` DEFAULT CHARACTER SET utf8 ;
USE `bird_watching_schema` ;

-- -----------------------------------------------------
-- Table `bird_watching_schema`.`users`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `bird_watching_schema`.`users` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `first_name` VARCHAR(45) NULL,
  `last_name` VARCHAR(45) NULL,
  `email` VARCHAR(45) NULL,
  `password` VARCHAR(255) NULL,
  `created_at` DATETIME NULL,
  `updated_at` DATETIME NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `bird_watching_schema`.`sightings`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `bird_watching_schema`.`sightings` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `species` VARCHAR(45) NULL,
  `location` VARCHAR(45) NULL,
  `datetime` DATETIME NULL,
  `number` INT NULL,
  `description` LONGTEXT NULL,
  `created_at` DATETIME NULL,
  `updated_at` DATETIME NULL,
  `user_id` INT NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_sightings_users_idx` (`user_id` ASC) VISIBLE,
  CONSTRAINT `fk_sightings_users`
    FOREIGN KEY (`user_id`)
    REFERENCES `bird_watching_schema`.`users` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `bird_watching_schema`.`likes`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `bird_watching_schema`.`likes` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `like` INT NULL,
  `created_at` DATETIME NULL,
  `updated_at` DATETIME NULL,
  `user_id` INT NOT NULL,
  `sighting_id` INT NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_opinions_users1_idx` (`user_id` ASC) VISIBLE,
  INDEX `fk_opinions_sightings1_idx` (`sighting_id` ASC) VISIBLE,
  CONSTRAINT `fk_opinions_users1`
    FOREIGN KEY (`user_id`)
    REFERENCES `bird_watching_schema`.`users` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_opinions_sightings1`
    FOREIGN KEY (`sighting_id`)
    REFERENCES `bird_watching_schema`.`sightings` (`id`)
    ON DELETE CASCADE
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `bird_watching_schema`.`comments`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `bird_watching_schema`.`comments` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `content` LONGTEXT NULL,
  `created_at` DATETIME NULL,
  `updated_at` DATETIME NULL,
  `user_id` INT NOT NULL,
  `sighting_id` INT NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_comments_users1_idx` (`user_id` ASC) VISIBLE,
  INDEX `fk_comments_sightings1_idx` (`sighting_id` ASC) VISIBLE,
  CONSTRAINT `fk_comments_users1`
    FOREIGN KEY (`user_id`)
    REFERENCES `bird_watching_schema`.`users` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_comments_sightings1`
    FOREIGN KEY (`sighting_id`)
    REFERENCES `bird_watching_schema`.`sightings` (`id`)
    ON DELETE CASCADE
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
