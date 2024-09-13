-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema mydb
-- -----------------------------------------------------
-- -----------------------------------------------------
-- Schema gabriel
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema gabriel
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `gabriel` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci ;
USE `gabriel` ;

-- -----------------------------------------------------
-- Table `gabriel`.`contratti`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `gabriel`.`contratti` (
  `ID` VARCHAR(8) NOT NULL,
  `Tipo` ENUM('Base', 'Gold', 'Premium') NULL DEFAULT NULL,
  PRIMARY KEY (`ID`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `gabriel`.`cmdb`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `gabriel`.`cmdb` (
  `Vendor` TEXT NULL DEFAULT NULL,
  `Software` TEXT NULL DEFAULT NULL,
  `Prodotto` TEXT NULL DEFAULT NULL,
  `Versione` TEXT NULL DEFAULT NULL,
  `Hostname` TEXT NULL DEFAULT NULL,
  `SDL` VARCHAR(8) NULL DEFAULT NULL,
  INDEX `SDL_idx` (`SDL` ASC) VISIBLE,
  INDEX `n_idx` (`SDL` ASC) VISIBLE,
  CONSTRAINT `FK_SDL_ID`
    FOREIGN KEY (`SDL`)
    REFERENCES `gabriel`.`contratti` (`ID`)
    ON DELETE SET NULL
    ON UPDATE CASCADE)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `gabriel`.`operatori`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `gabriel`.`operatori` (
  `ID` INT NOT NULL AUTO_INCREMENT,
  `Numero_Ticket` INT NULL DEFAULT '0',
  PRIMARY KEY (`ID`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `gabriel`.`problemi`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `gabriel`.`problemi` (
  `ID` INT NOT NULL AUTO_INCREMENT,
  `Operatore_ID` INT NULL DEFAULT NULL,
  `Timestamp` TIMESTAMP NULL DEFAULT NULL,
  `Hostname` VARCHAR(255) NULL DEFAULT NULL,
  `SDL` VARCHAR(8) NULL DEFAULT NULL,
  PRIMARY KEY (`ID`),
  INDEX `Operatore_ID` (`Operatore_ID` ASC) VISIBLE,
  INDEX `SDL` (`SDL` ASC) VISIBLE,
  CONSTRAINT `problemi_ibfk_1`
    FOREIGN KEY (`Operatore_ID`)
    REFERENCES `gabriel`.`operatori` (`ID`)
    ON DELETE SET NULL
    ON UPDATE CASCADE,
  CONSTRAINT `problemi_ibfk_2`
    FOREIGN KEY (`SDL`)
    REFERENCES `gabriel`.`contratti` (`ID`)
    ON DELETE SET NULL
    ON UPDATE CASCADE)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `gabriel`.`ticket`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `gabriel`.`ticket` (
  `ID` INT NOT NULL AUTO_INCREMENT,
  `Operatore_ID` INT NULL DEFAULT NULL,
  `Timestamp` TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP,
  `Hostname` VARCHAR(255) NULL DEFAULT NULL,
  `SDL` VARCHAR(8) NULL DEFAULT NULL,
  PRIMARY KEY (`ID`),
  INDEX `Operatore_ID` (`Operatore_ID` ASC) VISIBLE,
  INDEX `SDL` (`SDL` ASC) VISIBLE,
  CONSTRAINT `ticket_ibfk_1`
    FOREIGN KEY (`Operatore_ID`)
    REFERENCES `gabriel`.`operatori` (`ID`)
    ON DELETE SET NULL
    ON UPDATE CASCADE,
  CONSTRAINT `ticket_ibfk_2`
    FOREIGN KEY (`SDL`)
    REFERENCES `gabriel`.`contratti` (`ID`)
    ON DELETE SET NULL
    ON UPDATE CASCADE)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
USE `gabriel`;

DELIMITER $$
USE `gabriel`$$
CREATE
DEFINER=`root`@`localhost`
TRIGGER `gabriel`.`after_ticket_delete`
AFTER DELETE ON `gabriel`.`ticket`
FOR EACH ROW
BEGIN
    UPDATE operatori
    SET Numero_Ticket = Numero_Ticket - 1
    WHERE ID = OLD.Operatore_ID;
END$$

USE `gabriel`$$
CREATE
DEFINER=`root`@`localhost`
TRIGGER `gabriel`.`after_ticket_insert`
AFTER INSERT ON `gabriel`.`ticket`
FOR EACH ROW
BEGIN
    UPDATE operatori
    SET Numero_Ticket = Numero_Ticket + 1
    WHERE ID = NEW.Operatore_ID;
END$$

USE `gabriel`$$
CREATE
DEFINER=`root`@`localhost`
TRIGGER `gabriel`.`after_ticket_update`
AFTER UPDATE ON `gabriel`.`ticket`
FOR EACH ROW
BEGIN
    -- Diminuisce il numero di ticket per l'operatore precedente
    UPDATE operatori
    SET Numero_Ticket = Numero_Ticket - 1
    WHERE ID = OLD.Operatore_ID;

    -- Aumenta il numero di ticket per il nuovo operatore
    UPDATE operatori
    SET Numero_Ticket = Numero_Ticket + 1
    WHERE ID = NEW.Operatore_ID;
END$$


DELIMITER ;
