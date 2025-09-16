-- phpMyAdmin SQL Dump
-- version 5.2.1deb3
-- https://www.phpmyadmin.net/
--
-- Servidor: localhost:3306
-- Tiempo de generación: 27-08-2025 a las 02:45:13
-- Versión del servidor: 8.0.43-0ubuntu0.24.04.1
-- Versión de PHP: 8.3.6

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `zainex_scout`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `config_usuario`
--

CREATE TABLE `config_usuario` (
  `id_config` int UNSIGNED NOT NULL,
  `id_usuario` int DEFAULT NULL,
  `modo_oscuro` tinyint(1) DEFAULT '0'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `funciones`
--

CREATE TABLE `funciones` (
  `id_funcion` int NOT NULL,
  `nombre_funcion` varchar(100) NOT NULL,
  `abrev_funcion` varchar(3) NOT NULL,
  `descripcion` text
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `funciones_miembro`
--

CREATE TABLE `funciones_miembro` (
  `id_funcion_miembro` int NOT NULL,
  `id_miembro` int NOT NULL,
  `id_funcion` int NOT NULL,
  `desde_fecha` date NOT NULL,
  `hasta_fecha` date DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `grupos`
--

CREATE TABLE `grupos` (
  `id_grupo` int NOT NULL,
  `nombre_grupo` varchar(100) NOT NULL,
  `num_grupo` varchar(6) NOT NULL,
  `distrito_grupo` varchar(6) NOT NULL,
  `zona_grupo` varchar(6) NOT NULL,
  `creado_en_grupo` timestamp NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `miembros`
--

CREATE TABLE `miembros` (
  `id_miembros` int NOT NULL,
  `id_grupo` int NOT NULL,
  `dni_miembros` varchar(20) NOT NULL,
  `nombre_miembros` varchar(50) NOT NULL,
  `apellido_miembros` varchar(50) NOT NULL,
  `sexo_miembros` enum('M','V','X','Otro') NOT NULL,
  `fecha_nac_miembros` date NOT NULL,
  `nacionalidad_miembros` enum('Argentina','Chile','Perú','Otro') NOT NULL,
  `religion_miembros` enum('Catolico','Evangelista','Mormon','Judio','Budista','Otra') NOT NULL,
  `estado_civil_miembros` enum('Soltero','Casado','Viudo','Concubinato','Otro') NOT NULL,
  `telefono_miembros` varchar(20) DEFAULT NULL,
  `direccion_miembros` varchar(100) NOT NULL,
  `emergencia` varchar(200) DEFAULT NULL,
  `mail_miembros` varchar(100) DEFAULT NULL,
  `fecha_afil_miembros` date DEFAULT NULL,
  `activo_miembros` tinyint(1) DEFAULT '1',
  `creado_en_miembros` timestamp NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `movimientos`
--

CREATE TABLE `movimientos` (
  `id_mov` int UNSIGNED NOT NULL,
  `tipo_mov` enum('Ingreso','Egreso') NOT NULL,
  `fecha_mov` date NOT NULL,
  `detalle_mov` varchar(100) DEFAULT NULL,
  `rubro_mov` enum('AFILIACIONES','ART. LIMPIEZA','CAMPAMENTOS','CAPACITACIONES','CUOTA','DONACIONES','EVENTOS','GASTOS OPERATIVOS','INDUMENTARIA','INVERSIONES','MANT. SEDE','MAT. Y UTILES','REDONDEO','REFRIGERIO','SERVICIOS') NOT NULL,
  `comprobante_mov` varchar(50) DEFAULT NULL,
  `url_comprob_mov` varchar(255) DEFAULT NULL,
  `importe_mov` decimal(10,2) NOT NULL,
  `conciliado_mov` tinyint(1) DEFAULT '0',
  `creado_en_mov` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `creado_por_mov` int DEFAULT NULL,
  `conciliado_por_mov` int DEFAULT NULL,
  `observaciones_mov` text,
  `rama_id` int DEFAULT '0'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `ramas`
--

CREATE TABLE `ramas` (
  `id` int NOT NULL,
  `nombre` varchar(50) DEFAULT NULL,
  `porcentaje_libre` decimal(5,2) DEFAULT '10.00'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `usuarios`
--

CREATE TABLE `usuarios` (
  `id_usuarios` int NOT NULL,
  `id_grupo` int DEFAULT NULL,
  `dni_usuario` varchar(20) NOT NULL,
  `pass_usuario_hash` varchar(255) NOT NULL,
  `rol_usuario` enum('admin','colaborador') DEFAULT 'colaborador',
  `nombre_usuario` varchar(100) NOT NULL,
  `apellido_usuario` varchar(100) NOT NULL,
  `estado_usuario` tinyint(1) DEFAULT '1',
  `creado_en_usuario` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `super_admin` tinyint(1) DEFAULT '0',
  `modo_oscuro` tinyint(1) NOT NULL DEFAULT '0'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Volcado de datos para la tabla `usuarios`
--

INSERT INTO `usuarios` (`id_usuarios`, `id_grupo`, `dni_usuario`, `pass_usuario_hash`, `rol_usuario`, `nombre_usuario`, `apellido_usuario`, `estado_usuario`, `creado_en_usuario`, `super_admin`, `modo_oscuro`) VALUES
(1, NULL, '1', '$2b$12$F350cTN0v23LBxbV93EKMOX5JepyBv574QGdG7W9iU8YqbaDpCI5a', 'admin', 'Desarrollador', 'Zainex', 1, '2025-06-22 04:43:48', 1, 0),
(4, 1, '26851068', '$2b$12$5AVClXU00wWbocduztpWfucUve1ubwHDcEn/iZRgFcBILZNfQccYm', 'admin', 'Jose Martin', 'Chiappero', 1, '2025-07-14 05:09:48', 0, 0),
(6, 1, '31151477', '$2b$12$SaDtSixg88lTXpvgG1S8fejmnkno6rmuazvKxu5EsW/ZQyMqkaYCu', 'colaborador', 'Sole', 'Bilardo', 1, '2025-07-14 20:27:29', 0, 0);

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `config_usuario`
--
ALTER TABLE `config_usuario`
  ADD PRIMARY KEY (`id_config`),
  ADD KEY `id_usuario` (`id_usuario`);

--
-- Indices de la tabla `funciones`
--
ALTER TABLE `funciones`
  ADD PRIMARY KEY (`id_funcion`),
  ADD UNIQUE KEY `nombre_funcion` (`nombre_funcion`);

--
-- Indices de la tabla `funciones_miembro`
--
ALTER TABLE `funciones_miembro`
  ADD PRIMARY KEY (`id_funcion_miembro`),
  ADD KEY `id_miembro` (`id_miembro`),
  ADD KEY `id_funcion` (`id_funcion`);

--
-- Indices de la tabla `grupos`
--
ALTER TABLE `grupos`
  ADD PRIMARY KEY (`id_grupo`),
  ADD UNIQUE KEY `num_grupo` (`num_grupo`);

--
-- Indices de la tabla `miembros`
--
ALTER TABLE `miembros`
  ADD PRIMARY KEY (`id_miembros`),
  ADD UNIQUE KEY `dni_miembros` (`dni_miembros`),
  ADD KEY `id_grupo` (`id_grupo`);

--
-- Indices de la tabla `movimientos`
--
ALTER TABLE `movimientos`
  ADD PRIMARY KEY (`id_mov`),
  ADD KEY `fk_creador` (`creado_por_mov`),
  ADD KEY `fk_conciliador` (`conciliado_por_mov`);

--
-- Indices de la tabla `ramas`
--
ALTER TABLE `ramas`
  ADD PRIMARY KEY (`id`);

--
-- Indices de la tabla `usuarios`
--
ALTER TABLE `usuarios`
  ADD PRIMARY KEY (`id_usuarios`),
  ADD UNIQUE KEY `dni_usuario` (`dni_usuario`),
  ADD KEY `id_grupo` (`id_grupo`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `config_usuario`
--
ALTER TABLE `config_usuario`
  MODIFY `id_config` int UNSIGNED NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `funciones`
--
ALTER TABLE `funciones`
  MODIFY `id_funcion` int NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `funciones_miembro`
--
ALTER TABLE `funciones_miembro`
  MODIFY `id_funcion_miembro` int NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `grupos`
--
ALTER TABLE `grupos`
  MODIFY `id_grupo` int NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `miembros`
--
ALTER TABLE `miembros`
  MODIFY `id_miembros` int NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `movimientos`
--
ALTER TABLE `movimientos`
  MODIFY `id_mov` int UNSIGNED NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `usuarios`
--
ALTER TABLE `usuarios`
  MODIFY `id_usuarios` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- Restricciones para tablas volcadas
--

--
-- Filtros para la tabla `config_usuario`
--
ALTER TABLE `config_usuario`
  ADD CONSTRAINT `config_usuario_ibfk_1` FOREIGN KEY (`id_usuario`) REFERENCES `usuarios` (`id_usuarios`);

--
-- Filtros para la tabla `funciones_miembro`
--
ALTER TABLE `funciones_miembro`
  ADD CONSTRAINT `funciones_miembro_ibfk_1` FOREIGN KEY (`id_miembro`) REFERENCES `miembros` (`id_miembros`),
  ADD CONSTRAINT `funciones_miembro_ibfk_2` FOREIGN KEY (`id_funcion`) REFERENCES `funciones` (`id_funcion`);

--
-- Filtros para la tabla `miembros`
--
ALTER TABLE `miembros`
  ADD CONSTRAINT `miembros_ibfk_1` FOREIGN KEY (`id_grupo`) REFERENCES `grupos` (`id_grupo`);

--
-- Filtros para la tabla `movimientos`
--
ALTER TABLE `movimientos`
  ADD CONSTRAINT `fk_conciliador` FOREIGN KEY (`conciliado_por_mov`) REFERENCES `usuarios` (`id_usuarios`),
  ADD CONSTRAINT `fk_creador` FOREIGN KEY (`creado_por_mov`) REFERENCES `usuarios` (`id_usuarios`);

--
-- Filtros para la tabla `usuarios`
--
ALTER TABLE `usuarios`
  ADD CONSTRAINT `usuarios_ibfk_1` FOREIGN KEY (`id_grupo`) REFERENCES `grupos` (`id_grupo`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
