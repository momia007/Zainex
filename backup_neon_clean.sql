--
-- PostgreSQL database dump
--

\restrict RGZpq5JjXEcLbqRw2XLfaGgWBV294xoVqcP7xhWw90w1UmCyBZWRDsFrQkUBGeM

-- Dumped from database version 17.5 (1b53132)
-- Dumped by pg_dump version 17.6 (Debian 17.6-1.pgdg13+1)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: estado_civil_enum; Type: TYPE; Schema: public; Owner: -
--

CREATE TYPE public.estado_civil_enum AS ENUM (
    'Soltero',
    'Casado',
    'Viudo',
    'Concubinato',
    'Otro'
);


--
-- Name: nacionalidad_enum; Type: TYPE; Schema: public; Owner: -
--

CREATE TYPE public.nacionalidad_enum AS ENUM (
    'Argentina',
    'Chile',
    'Perú',
    'Otro'
);


--
-- Name: religion_enum; Type: TYPE; Schema: public; Owner: -
--

CREATE TYPE public.religion_enum AS ENUM (
    'Catolico',
    'Evangelista',
    'Mormon',
    'Judio',
    'Budista',
    'Otra'
);


--
-- Name: rol_usuario_enum; Type: TYPE; Schema: public; Owner: -
--

CREATE TYPE public.rol_usuario_enum AS ENUM (
    'admin',
    'colaborador'
);


--
-- Name: rubro_mov_enum; Type: TYPE; Schema: public; Owner: -
--

CREATE TYPE public.rubro_mov_enum AS ENUM (
    'AFILIACIONES',
    'ART. LIMPIEZA',
    'CAMPAMENTOS',
    'CAPACITACIONES',
    'CUOTA',
    'DONACIONES',
    'EVENTOS',
    'GASTOS OPERATIVOS',
    'INDUMENTARIA',
    'INVERSIONES',
    'MANT. SEDE',
    'MAT. Y UTILES',
    'REDONDEO',
    'REFRIGERIO',
    'SERVICIOS'
);


--
-- Name: sexo_enum; Type: TYPE; Schema: public; Owner: -
--

CREATE TYPE public.sexo_enum AS ENUM (
    'M',
    'V',
    'X',
    'Otro'
);


--
-- Name: tipo_mov_enum; Type: TYPE; Schema: public; Owner: -
--

CREATE TYPE public.tipo_mov_enum AS ENUM (
    'Ingreso',
    'Egreso'
);


SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: config_usuario; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.config_usuario (
    id_config integer NOT NULL,
    id_usuario integer,
    modo_oscuro boolean DEFAULT false
);


--
-- Name: config_usuario_id_config_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.config_usuario_id_config_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: config_usuario_id_config_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.config_usuario_id_config_seq OWNED BY public.config_usuario.id_config;


--
-- Name: funciones; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.funciones (
    id_funcion integer NOT NULL,
    nombre_funcion character varying(100) NOT NULL,
    abrev_funcion character varying(3) NOT NULL,
    descripcion text
);


--
-- Name: funciones_id_funcion_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.funciones_id_funcion_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: funciones_id_funcion_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.funciones_id_funcion_seq OWNED BY public.funciones.id_funcion;


--
-- Name: funciones_miembro; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.funciones_miembro (
    id_funcion_miembro integer NOT NULL,
    id_miembro integer,
    id_funcion integer,
    desde_fecha date NOT NULL,
    hasta_fecha date
);


--
-- Name: funciones_miembro_id_funcion_miembro_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.funciones_miembro_id_funcion_miembro_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: funciones_miembro_id_funcion_miembro_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.funciones_miembro_id_funcion_miembro_seq OWNED BY public.funciones_miembro.id_funcion_miembro;


--
-- Name: grupos; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.grupos (
    id_grupo integer NOT NULL,
    nombre_grupo character varying(100) NOT NULL,
    num_grupo character varying(6) NOT NULL,
    distrito_grupo character varying(6) NOT NULL,
    zona_grupo character varying(6) NOT NULL,
    creado_en_grupo timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


--
-- Name: grupos_id_grupo_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.grupos_id_grupo_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: grupos_id_grupo_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.grupos_id_grupo_seq OWNED BY public.grupos.id_grupo;


--
-- Name: miembros; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.miembros (
    id_miembros integer NOT NULL,
    id_grupo integer,
    dni_miembros character varying(20) NOT NULL,
    nombre_miembros character varying(50) NOT NULL,
    apellido_miembros character varying(50) NOT NULL,
    sexo_miembros public.sexo_enum NOT NULL,
    fecha_nac_miembros date NOT NULL,
    nacionalidad_miembros public.nacionalidad_enum NOT NULL,
    religion_miembros public.religion_enum NOT NULL,
    estado_civil_miembros public.estado_civil_enum NOT NULL,
    telefono_miembros character varying(20),
    direccion_miembros character varying(100) NOT NULL,
    emergencia character varying(200),
    mail_miembros character varying(100),
    fecha_afil_miembros date,
    activo_miembros boolean DEFAULT true,
    creado_en_miembros timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


--
-- Name: miembros_id_miembros_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.miembros_id_miembros_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: miembros_id_miembros_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.miembros_id_miembros_seq OWNED BY public.miembros.id_miembros;


--
-- Name: movimientos; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.movimientos (
    id_mov integer NOT NULL,
    tipo_mov public.tipo_mov_enum NOT NULL,
    fecha_mov date NOT NULL,
    detalle_mov character varying(100),
    rubro_mov public.rubro_mov_enum NOT NULL,
    comprobante_mov character varying(50),
    url_comprob_mov character varying(255),
    importe_mov numeric(10,2) NOT NULL,
    conciliado_mov boolean DEFAULT false,
    creado_en_mov timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    creado_por_mov integer,
    conciliado_por_mov integer,
    observaciones_mov text,
    rama_id integer
);


--
-- Name: movimientos_id_mov_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.movimientos_id_mov_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: movimientos_id_mov_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.movimientos_id_mov_seq OWNED BY public.movimientos.id_mov;


--
-- Name: ramas; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.ramas (
    id integer NOT NULL,
    nombre character varying(50),
    porcentaje_libre numeric(5,2) DEFAULT 10.00
);


--
-- Name: ramas_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.ramas_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: ramas_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.ramas_id_seq OWNED BY public.ramas.id;


--
-- Name: usuarios; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.usuarios (
    id_usuarios integer NOT NULL,
    id_grupo integer,
    dni_usuario character varying(20) NOT NULL,
    pass_usuario_hash character varying(255) NOT NULL,
    rol_usuario public.rol_usuario_enum DEFAULT 'colaborador'::public.rol_usuario_enum,
    nombre_usuario character varying(100) NOT NULL,
    apellido_usuario character varying(100) NOT NULL,
    estado_usuario boolean DEFAULT true,
    creado_en_usuario timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    super_admin boolean DEFAULT false,
    modo_oscuro boolean DEFAULT false
);


--
-- Name: usuarios_id_usuarios_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.usuarios_id_usuarios_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: usuarios_id_usuarios_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.usuarios_id_usuarios_seq OWNED BY public.usuarios.id_usuarios;


--
-- Name: config_usuario id_config; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.config_usuario ALTER COLUMN id_config SET DEFAULT nextval('public.config_usuario_id_config_seq'::regclass);


--
-- Name: funciones id_funcion; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.funciones ALTER COLUMN id_funcion SET DEFAULT nextval('public.funciones_id_funcion_seq'::regclass);


--
-- Name: funciones_miembro id_funcion_miembro; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.funciones_miembro ALTER COLUMN id_funcion_miembro SET DEFAULT nextval('public.funciones_miembro_id_funcion_miembro_seq'::regclass);


--
-- Name: grupos id_grupo; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.grupos ALTER COLUMN id_grupo SET DEFAULT nextval('public.grupos_id_grupo_seq'::regclass);


--
-- Name: miembros id_miembros; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.miembros ALTER COLUMN id_miembros SET DEFAULT nextval('public.miembros_id_miembros_seq'::regclass);


--
-- Name: movimientos id_mov; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.movimientos ALTER COLUMN id_mov SET DEFAULT nextval('public.movimientos_id_mov_seq'::regclass);


--
-- Name: ramas id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.ramas ALTER COLUMN id SET DEFAULT nextval('public.ramas_id_seq'::regclass);


--
-- Name: usuarios id_usuarios; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.usuarios ALTER COLUMN id_usuarios SET DEFAULT nextval('public.usuarios_id_usuarios_seq'::regclass);


--
-- Data for Name: config_usuario; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.config_usuario (id_config, id_usuario, modo_oscuro) FROM stdin;
\.


--
-- Data for Name: funciones; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.funciones (id_funcion, nombre_funcion, abrev_funcion, descripcion) FROM stdin;
\.


--
-- Data for Name: funciones_miembro; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.funciones_miembro (id_funcion_miembro, id_miembro, id_funcion, desde_fecha, hasta_fecha) FROM stdin;
\.


--
-- Data for Name: grupos; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.grupos (id_grupo, nombre_grupo, num_grupo, distrito_grupo, zona_grupo, creado_en_grupo) FROM stdin;
\.


--
-- Data for Name: miembros; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.miembros (id_miembros, id_grupo, dni_miembros, nombre_miembros, apellido_miembros, sexo_miembros, fecha_nac_miembros, nacionalidad_miembros, religion_miembros, estado_civil_miembros, telefono_miembros, direccion_miembros, emergencia, mail_miembros, fecha_afil_miembros, activo_miembros, creado_en_miembros) FROM stdin;
\.


--
-- Data for Name: movimientos; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.movimientos (id_mov, tipo_mov, fecha_mov, detalle_mov, rubro_mov, comprobante_mov, url_comprob_mov, importe_mov, conciliado_mov, creado_en_mov, creado_por_mov, conciliado_por_mov, observaciones_mov, rama_id) FROM stdin;
\.


--
-- Data for Name: ramas; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.ramas (id, nombre, porcentaje_libre) FROM stdin;
\.


--
-- Data for Name: usuarios; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.usuarios (id_usuarios, id_grupo, dni_usuario, pass_usuario_hash, rol_usuario, nombre_usuario, apellido_usuario, estado_usuario, creado_en_usuario, super_admin, modo_oscuro) FROM stdin;
1	\N	1	$2b$12$F350cTN0v23LBxbV93EKMOX5JepyBv574QGdG7W9iU8YqbaDpCI5a	admin	Desarrollador	Zainex	t	2025-08-28 05:00:02.993627	t	f
\.


--
-- Name: config_usuario_id_config_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.config_usuario_id_config_seq', 1, false);


--
-- Name: funciones_id_funcion_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.funciones_id_funcion_seq', 1, false);


--
-- Name: funciones_miembro_id_funcion_miembro_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.funciones_miembro_id_funcion_miembro_seq', 1, false);


--
-- Name: grupos_id_grupo_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.grupos_id_grupo_seq', 1, false);


--
-- Name: miembros_id_miembros_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.miembros_id_miembros_seq', 1, false);


--
-- Name: movimientos_id_mov_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.movimientos_id_mov_seq', 1, false);


--
-- Name: ramas_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.ramas_id_seq', 1, false);


--
-- Name: usuarios_id_usuarios_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.usuarios_id_usuarios_seq', 1, true);


--
-- Name: config_usuario config_usuario_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.config_usuario
    ADD CONSTRAINT config_usuario_pkey PRIMARY KEY (id_config);


--
-- Name: funciones_miembro funciones_miembro_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.funciones_miembro
    ADD CONSTRAINT funciones_miembro_pkey PRIMARY KEY (id_funcion_miembro);


--
-- Name: funciones funciones_nombre_funcion_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.funciones
    ADD CONSTRAINT funciones_nombre_funcion_key UNIQUE (nombre_funcion);


--
-- Name: funciones funciones_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.funciones
    ADD CONSTRAINT funciones_pkey PRIMARY KEY (id_funcion);


--
-- Name: grupos grupos_num_grupo_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.grupos
    ADD CONSTRAINT grupos_num_grupo_key UNIQUE (num_grupo);


--
-- Name: grupos grupos_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.grupos
    ADD CONSTRAINT grupos_pkey PRIMARY KEY (id_grupo);


--
-- Name: miembros miembros_dni_miembros_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.miembros
    ADD CONSTRAINT miembros_dni_miembros_key UNIQUE (dni_miembros);


--
-- Name: miembros miembros_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.miembros
    ADD CONSTRAINT miembros_pkey PRIMARY KEY (id_miembros);


--
-- Name: movimientos movimientos_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.movimientos
    ADD CONSTRAINT movimientos_pkey PRIMARY KEY (id_mov);


--
-- Name: ramas ramas_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.ramas
    ADD CONSTRAINT ramas_pkey PRIMARY KEY (id);


--
-- Name: usuarios usuarios_dni_usuario_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.usuarios
    ADD CONSTRAINT usuarios_dni_usuario_key UNIQUE (dni_usuario);


--
-- Name: usuarios usuarios_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.usuarios
    ADD CONSTRAINT usuarios_pkey PRIMARY KEY (id_usuarios);


--
-- Name: config_usuario config_usuario_id_usuario_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.config_usuario
    ADD CONSTRAINT config_usuario_id_usuario_fkey FOREIGN KEY (id_usuario) REFERENCES public.usuarios(id_usuarios);


--
-- Name: funciones_miembro funciones_miembro_id_funcion_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.funciones_miembro
    ADD CONSTRAINT funciones_miembro_id_funcion_fkey FOREIGN KEY (id_funcion) REFERENCES public.funciones(id_funcion);


--
-- Name: funciones_miembro funciones_miembro_id_miembro_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.funciones_miembro
    ADD CONSTRAINT funciones_miembro_id_miembro_fkey FOREIGN KEY (id_miembro) REFERENCES public.miembros(id_miembros);


--
-- Name: miembros miembros_id_grupo_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.miembros
    ADD CONSTRAINT miembros_id_grupo_fkey FOREIGN KEY (id_grupo) REFERENCES public.grupos(id_grupo);


--
-- Name: movimientos movimientos_conciliado_por_mov_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.movimientos
    ADD CONSTRAINT movimientos_conciliado_por_mov_fkey FOREIGN KEY (conciliado_por_mov) REFERENCES public.usuarios(id_usuarios);


--
-- Name: movimientos movimientos_creado_por_mov_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.movimientos
    ADD CONSTRAINT movimientos_creado_por_mov_fkey FOREIGN KEY (creado_por_mov) REFERENCES public.usuarios(id_usuarios);


--
-- Name: movimientos movimientos_rama_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.movimientos
    ADD CONSTRAINT movimientos_rama_id_fkey FOREIGN KEY (rama_id) REFERENCES public.ramas(id);


--
-- Name: usuarios usuarios_id_grupo_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.usuarios
    ADD CONSTRAINT usuarios_id_grupo_fkey FOREIGN KEY (id_grupo) REFERENCES public.grupos(id_grupo);


--
-- PostgreSQL database dump complete
--

\unrestrict RGZpq5JjXEcLbqRw2XLfaGgWBV294xoVqcP7xhWw90w1UmCyBZWRDsFrQkUBGeM

