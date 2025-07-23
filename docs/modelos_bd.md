# Modelos de Base de Datos — Zainex

Este archivo documenta las tablas utilizadas en el módulo Scout de Zainex.

---

## Tabla `grupos`
Contiene la información estructural de cada grupo scout.

- `id_grupo` (INT, PK, AUTO_INCREMENT)
- `nombre_grupo` (VARCHAR)
- `num_grupo` (VARCHAR)
- `distrito_grupo` (VARCHAR)
- `zona_grupo` (VARCHAR)
- `creado_en_grupo` (TIMESTAMP)

---

## Tabla `usuarios`
Usuarios que acceden a la plataforma, vinculados (o no) a un grupo.

- `id_usuarios` (INT, PK, AUTO_INCREMENT)
- `id_grupo` (INT, FK a grupos)
- `dni_usuario` (VARCHAR, UNIQUE)
- `pass_usuario_hash` (VARCHAR)
- `rol_usuario` (ENUM: 'admin', 'colaborador')
- `super_admin` (BOOLEAN)
- `nombre_usuario` (VARCHAR)
- `apellido_usuario` (VARCHAR)
- `estado_usuario` (BOOLEAN)
- `creado_en_usuario` (TIMESTAMP)


## Tabla `miembros`
Miembros pertenecientes al grupo según la clave id_grupo
- `id_miembros` INT PRIMARY KEY AUTO_INCREMENT,
- `id_grupo`  INT NOT NULL,
- `dni_miembros`  VARCHAR(20) NOT NULL UNIQUE,
- `nombre_miembros`  VARCHAR(50) NOT NULL,
- `apellido_miembros`  VARCHAR(50) NOT NULL,
- `sexo_miembros`  ENUM('M', 'V', 'X', 'Otro')NOT NULL,
- `fecha_nac_miembros`  DATE NOT NULL,
- `nacionalidad_miembros`  ENUM('Argentina', 'Chile', 'Perú', 'Otro') NOT NULL,
- `religion_miembros`  ENUM('Catolico', 'Evangelista', 'Mormon', 'Judio', 'Budista', 'Otra') NOT NULL,
- `estado_civil_miembros`  ENUM('Soltero', 'Casado', 'Viudo', 'Concubinato', 'Otro') NOT NULL,
- `telefono_miembros`  VARCHAR(20),
- `direccion_miembros`  VARCHAR(100) NOT NULL,
- `mail_miembros`  VARCHAR(100),
- `fecha_afil_miembros`  DATE,
- `activo_miembros`  BOOLEAN DEFAULT TRUE,
- `creado_en_miembros`  TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
- `FOREIGN KEY`  (id_grupo) REFERENCES grupos(id_grupo) 


## Tabla funciones
Funciones disponibles para los miembros del grupo
- `id_funcion` INT PRIMARY KEY AUTO_INCREMENT,
- `nombre_funcion` VARCHAR(100) NOT NULL UNIQUE,
- `descripcion` TEXT


## Tabla funciones_miembro
Registrar todas las funciones que un miembro haya desempeñado a lo largo del tiempo dentro del grupo, permitiendo conservar su historial completo.
- `id_funcion_miembro`  INT PRIMARY KEY AUTO_INCREMENT,
- `id_miembro`  INT NOT NULL,
- `id_funcion`  INT NOT NULL,
- `desde_fecha`  DATE NOT NULL,
- `hasta_fecha`  DATE,
- `FOREIGN KEY`  (id_miembro) REFERENCES miembros(id_miembros),
- `FOREIGN KEY`  (id_funcion) REFERENCES funciones(id_funcion)


## Tabla movimientos
Registra cada movimiento contable del sistema, incluyendo ingresos y egresos de dinero, junto con sus detalles, comprobantes y trazabilidad de usuario.

- `id_mov` INT UNSIGNED AUTO_INCREMENT PRIMARY KEY
- `tipo_mov` ENUM('Ingreso', 'Egreso') NOT NULL
- `fecha_mov` DATE NOT NULL Fecha real en que se realizó el movimiento (no la fecha de registro).
- `detalle_mov` VARCHAR(100) Descripción breve del gasto o ingreso (comercio, motivo, etc.).
- `rubro_mov` ENUM('AFILIACIONES', 'ART. LIMPIEZA', 'CAMPAMENTOS', 'CAPACITACIONES', 'CUOTA',       'DONACIONES', 'EVENTOS', 'GASTOS OPERATIVOS', 'INDUMENTARIA', 'INVERSIONES', 'MANT. SEDE', 'MAT. Y UTILES', 'REDONDEO', 'REFRIGERIO', 'SERVICIOS') NOT NULL 
- `comprobante_mov` VARCHAR(50) Número de comprobante (factura, ticket, etc.).
- `url_comprob_mov` VARCHAR(255) Enlace al archivo digital del comprobante (imagen/PDF).
- `importe_mov` DECIMAL(10,2) NOT NULL
- `conciliado_mov` TINYINT(1) DEFAULT 0  - (0 = no conciliado, 1 = conciliado).
- `creado_en_mov` TIMESTAMP DEFAULT CURRENT_TIMESTAMP Fecha y hora de registro en el sistema.
- `creado_por_mov` INT Usuario que registró el movimiento.
- `FOREIGN KEY` (creado_por_mov) REFERENCES usuarios(id_usuarios)
- `conciliado_por_mov` INT Usuario que validó la conciliación del movimiento.
- `FOREIGN KEY` (conciliado_por_mov) REFERENCES usuarios(id_usuarios)
- `observaciones_mov` TEXT Notas adicionales sobre el movimiento (uso libre).


