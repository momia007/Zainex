app/
│
├── routes/
│   ├── rutas_usuarios.py      # Rutas para crear/listar usuarios
│   ├── rutas_grupos.py        # Rutas para grupos: alta, verificación, etc.
│   ├── rutas_miembros.py      # Rutas para miembros: listado, alta, edición
│   ├── rutas_funciones.py     # Rutas para funciones (solo super_admin)
│   └── rutas_home.py          # Ruta del dashboard principal
│
├── servicios/
│   ├── servicio_usuarios.py   # Funciones SQL para usuarios
│   ├── servicio_grupos.py     # Funciones SQL para grupos
│   ├── servicio_miembros.py   # Funciones SQL para miembros
│   └── servicio_funciones.py  # Funciones SQL para funciones
│
├── validaciones/
│   └── validaciones.py        # Validaciones comunes: campos, contraseñas, etc.
│
├── utils/
│   └── permisos.py            # Decorador requiere_rol y helpers de sesión
│
├── templates/
│   ├── nvo_usuario.html
│   ├── nvo_grupo.html
│   ├── miembros.html
│   ├── nvo_miembro.html
│   └── home.html
│
├── config/
│   └── conectar_db.py         # Conexión a MySQL u otras configs
│
└── app.py                     # Arranque principal donde se registran Blueprints
