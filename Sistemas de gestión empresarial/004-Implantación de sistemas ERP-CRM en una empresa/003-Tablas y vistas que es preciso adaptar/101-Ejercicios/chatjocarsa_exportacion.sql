-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Servidor: localhost
-- Tiempo de generación: 07-01-2026 a las 19:02:45
-- Versión del servidor: 8.0.44-0ubuntu0.24.04.2
-- Versión de PHP: 8.3.6

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `chatjocarsa`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `conversaciones`
--

CREATE TABLE `conversaciones` (
  `Identificador` int NOT NULL,
  `usuario_nombre` int NOT NULL,
  `modelo_nombre` int NOT NULL,
  `fecha` datetime NOT NULL,
  `descripcion` varchar(255) COLLATE utf8mb4_spanish_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_spanish_ci;

--
-- Volcado de datos para la tabla `conversaciones`
--

INSERT INTO `conversaciones` (`Identificador`, `usuario_nombre`, `modelo_nombre`, `fecha`, `descripcion`) VALUES
(1, 1, 6, '2026-01-07 15:46:54', 'Primera conversación');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `modelos`
--

CREATE TABLE `modelos` (
  `Identificador` int NOT NULL,
  `nombre` varchar(255) COLLATE utf8mb4_spanish_ci NOT NULL,
  `modelo` varchar(255) COLLATE utf8mb4_spanish_ci NOT NULL,
  `descripcion` text COLLATE utf8mb4_spanish_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_spanish_ci;

--
-- Volcado de datos para la tabla `modelos`
--

INSERT INTO `modelos` (`Identificador`, `nombre`, `modelo`, `descripcion`) VALUES
(1, 'llama3.1:8b-instruct-q4_0 ', 'llama3.1:8b-instruct-q4_0 ', 'llama3.1:8b-instruct-q4_0 '),
(2, 'qwen2.5:7b-instruct-q4_0', 'qwen2.5:7b-instruct-q4_0', 'qwen2.5:7b-instruct-q4_0'),
(3, 'deepseek-r1:8b ', 'deepseek-r1:8b ', 'deepseek-r1:8b '),
(4, 'qwen2.5:3b-instruct ', 'qwen2.5:3b-instruct ', 'qwen2.5:3b-instruct '),
(5, 'llama3:latest ', 'llama3:latest ', 'llama3:latest '),
(6, 'qwen2.5-coder:7b', 'qwen2.5-coder:7b', 'qwen2.5-coder:7b'),
(7, 'gemma2:9b-instruct-q4_0', 'gemma2:9b-instruct-q4_0', 'gemma2:9b-instruct-q4_0');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `planes`
--

CREATE TABLE `planes` (
  `Identificador` int NOT NULL,
  `nombre` varchar(255) COLLATE utf8mb4_spanish_ci NOT NULL,
  `descripcion` text COLLATE utf8mb4_spanish_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_spanish_ci;

--
-- Volcado de datos para la tabla `planes`
--

INSERT INTO `planes` (`Identificador`, `nombre`, `descripcion`) VALUES
(1, 'Ilimitado', 'Plan ilimitado');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `usuarios`
--

CREATE TABLE `usuarios` (
  `Identificador` int NOT NULL,
  `usuario` varchar(255) COLLATE utf8mb4_spanish_ci NOT NULL,
  `contrasena` varchar(255) COLLATE utf8mb4_spanish_ci NOT NULL,
  `nombre` varchar(255) COLLATE utf8mb4_spanish_ci NOT NULL,
  `apellidos` varchar(255) COLLATE utf8mb4_spanish_ci NOT NULL,
  `email` varchar(255) COLLATE utf8mb4_spanish_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_spanish_ci;

--
-- Volcado de datos para la tabla `usuarios`
--

INSERT INTO `usuarios` (`Identificador`, `usuario`, `contrasena`, `nombre`, `apellidos`, `email`) VALUES
(1, 'jocarsa', 'jocarsa', 'Jose Vicente', 'Carratalá Sanchis', 'info@jocarsa.com');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `usuariosyplanes`
--

CREATE TABLE `usuariosyplanes` (
  `Identificador` int NOT NULL,
  `planes_nombre` int NOT NULL,
  `usuarios_nombre` int NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_spanish_ci;

--
-- Volcado de datos para la tabla `usuariosyplanes`
--

INSERT INTO `usuariosyplanes` (`Identificador`, `planes_nombre`, `usuarios_nombre`) VALUES
(1, 1, 1);

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `conversaciones`
--
ALTER TABLE `conversaciones`
  ADD PRIMARY KEY (`Identificador`),
  ADD KEY `FKusuariosnombre` (`usuario_nombre`),
  ADD KEY `FKmodelosnombre` (`modelo_nombre`);

--
-- Indices de la tabla `modelos`
--
ALTER TABLE `modelos`
  ADD PRIMARY KEY (`Identificador`);

--
-- Indices de la tabla `planes`
--
ALTER TABLE `planes`
  ADD PRIMARY KEY (`Identificador`);

--
-- Indices de la tabla `usuarios`
--
ALTER TABLE `usuarios`
  ADD PRIMARY KEY (`Identificador`);

--
-- Indices de la tabla `usuariosyplanes`
--
ALTER TABLE `usuariosyplanes`
  ADD PRIMARY KEY (`Identificador`),
  ADD KEY `FKplanes` (`planes_nombre`),
  ADD KEY `FKusuarios` (`usuarios_nombre`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `conversaciones`
--
ALTER TABLE `conversaciones`
  MODIFY `Identificador` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT de la tabla `modelos`
--
ALTER TABLE `modelos`
  MODIFY `Identificador` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

--
-- AUTO_INCREMENT de la tabla `planes`
--
ALTER TABLE `planes`
  MODIFY `Identificador` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT de la tabla `usuarios`
--
ALTER TABLE `usuarios`
  MODIFY `Identificador` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT de la tabla `usuariosyplanes`
--
ALTER TABLE `usuariosyplanes`
  MODIFY `Identificador` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- Restricciones para tablas volcadas
--

--
-- Filtros para la tabla `conversaciones`
--
ALTER TABLE `conversaciones`
  ADD CONSTRAINT `FKmodelosnombre` FOREIGN KEY (`modelo_nombre`) REFERENCES `modelos` (`Identificador`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  ADD CONSTRAINT `FKusuariosnombre` FOREIGN KEY (`usuario_nombre`) REFERENCES `usuarios` (`Identificador`) ON DELETE RESTRICT ON UPDATE RESTRICT;

--
-- Filtros para la tabla `usuariosyplanes`
--
ALTER TABLE `usuariosyplanes`
  ADD CONSTRAINT `FKplanes` FOREIGN KEY (`planes_nombre`) REFERENCES `planes` (`Identificador`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  ADD CONSTRAINT `FKusuarios` FOREIGN KEY (`usuarios_nombre`) REFERENCES `usuarios` (`Identificador`) ON DELETE RESTRICT ON UPDATE RESTRICT;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
