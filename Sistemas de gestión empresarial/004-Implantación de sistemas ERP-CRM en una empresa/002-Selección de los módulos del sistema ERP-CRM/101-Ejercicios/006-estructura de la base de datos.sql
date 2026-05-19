CREATE DATABASE chatjocarsa;

USE chatjocarsa;

CREATE TABLE `chatjocarsa`.`usuarios` (`Identificador` INT NOT NULL AUTO_INCREMENT , `usuario` VARCHAR(255) NOT NULL , `contrasena` VARCHAR(255) NOT NULL , `nombre` VARCHAR(255) NOT NULL , `apellidos` VARCHAR(255) NOT NULL , `email` VARCHAR(255) NOT NULL , PRIMARY KEY (`Identificador`)) ENGINE = InnoDB;

INSERT INTO `usuarios` (`Identificador`, `usuario`, `contrasena`, `nombre`, `apellidos`, `email`) VALUES (NULL, 'jocarsa', 'jocarsa', 'Jose Vicente', 'Carratalá Sanchis', 'info@jocarsa.com');

CREATE TABLE `chatjocarsa`.`planes` (`Identificador` INT NOT NULL AUTO_INCREMENT , `nombre` VARCHAR(255) NOT NULL , `descripcion` TEXT NOT NULL , PRIMARY KEY (`Identificador`)) ENGINE = InnoDB;

INSERT INTO `planes` (`Identificador`, `nombre`, `descripcion`) VALUES (NULL, 'Ilimitado', 'Plan ilimitado');

-- creo tabla de planes y usuarios:
CREATE TABLE `chatjocarsa`.`usuariosyplanes` (`Identificador` INT NOT NULL AUTO_INCREMENT , `planes_nombre` INT NOT NULL , `usuarios_nombre` INT NOT NULL , PRIMARY KEY (`Identificador`)) ENGINE = InnoDB;

ALTER TABLE `usuariosyplanes` ADD CONSTRAINT `FKplanes` FOREIGN KEY (`planes_nombre`) REFERENCES `planes`(`Identificador`) ON DELETE RESTRICT ON UPDATE RESTRICT;

ALTER TABLE `usuariosyplanes` ADD CONSTRAINT `FKusuarios` FOREIGN KEY (`usuarios_nombre`) REFERENCES `usuarios`(`Identificador`) ON DELETE RESTRICT ON UPDATE RESTRICT;

-- inserto plan para el usuario

INSERT INTO `usuariosyplanes` (`Identificador`, `planes_nombre`, `usuarios_nombre`) VALUES (NULL, '1', '1');

CREATE TABLE `chatjocarsa`.`modelos` (`Identificador` INT NOT NULL AUTO_INCREMENT , `nombre` VARCHAR(255) NOT NULL , `modelo` VARCHAR(255) NOT NULL , `descripcion` TEXT NOT NULL , PRIMARY KEY (`Identificador`)) ENGINE = InnoDB;


INSERT INTO `modelos` (`Identificador`, `nombre`, `modelo`, `descripcion`) VALUES (NULL, 'llama3.1:8b-instruct-q4_0 ', 'llama3.1:8b-instruct-q4_0 ', 'llama3.1:8b-instruct-q4_0 ');

INSERT INTO `modelos` (`Identificador`, `nombre`, `modelo`, `descripcion`) VALUES (NULL, 'qwen2.5:7b-instruct-q4_0', 'qwen2.5:7b-instruct-q4_0', 'qwen2.5:7b-instruct-q4_0');

INSERT INTO `modelos` (`Identificador`, `nombre`, `modelo`, `descripcion`) VALUES (NULL, 'deepseek-r1:8b ', 'deepseek-r1:8b ', 'deepseek-r1:8b ');

INSERT INTO `modelos` (`Identificador`, `nombre`, `modelo`, `descripcion`) VALUES (NULL, 'qwen2.5:3b-instruct ', 'qwen2.5:3b-instruct ', 'qwen2.5:3b-instruct ');

INSERT INTO `modelos` (`Identificador`, `nombre`, `modelo`, `descripcion`) VALUES (NULL, 'llama3:latest ', 'llama3:latest ', 'llama3:latest ');

INSERT INTO `modelos` (`Identificador`, `nombre`, `modelo`, `descripcion`) VALUES (NULL, 'qwen2.5-coder:7b', 'qwen2.5-coder:7b', 'qwen2.5-coder:7b');

INSERT INTO `modelos` (`Identificador`, `nombre`, `modelo`, `descripcion`) VALUES (NULL, 'gemma2:9b-instruct-q4_0', 'gemma2:9b-instruct-q4_0', 'gemma2:9b-instruct-q4_0');

CREATE TABLE `chatjocarsa`.`conversaciones` (`Identificador` INT NOT NULL AUTO_INCREMENT , `usuario_nombre` INT NOT NULL , `modelo_nombre` INT NOT NULL , `fecha` DATETIME NOT NULL , PRIMARY KEY (`Identificador`)) ENGINE = InnoDB;

ALTER TABLE `conversaciones` ADD CONSTRAINT `FKusuariosnombre` FOREIGN KEY (`usuario_nombre`) REFERENCES `usuarios`(`Identificador`) ON DELETE RESTRICT ON UPDATE RESTRICT;

ALTER TABLE `conversaciones` ADD CONSTRAINT `FKmodelosnombre` FOREIGN KEY (`modelo_nombre`) REFERENCES `modelos`(`Identificador`) ON DELETE RESTRICT ON UPDATE RESTRICT;

INSERT INTO `conversaciones` (`Identificador`, `usuario_nombre`, `modelo_nombre`, `fecha`) VALUES (NULL, '1', '6', '2026-01-07 15:46:54.000000');

ALTER TABLE `conversaciones` ADD `descripcion` VARCHAR(255) NOT NULL AFTER `fecha`;

UPDATE `conversaciones` SET `descripcion` = 'Primera conversación' WHERE `conversaciones`.`Identificador` = 1;

