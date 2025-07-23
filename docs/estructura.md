# Estructura de Carpetas — Proyecto

Este proyecto está organizado de forma modular y escalable.

## `/app/`
Código fuente principal.

- `/routes/`: Rutas (endpoints) separadas por módulo.
- `/models/`: Estructuras de base de datos o clases ORM.
- `/utils/`: Funciones de utilidad (como generación de hashes).
- `config.py`: Variables globales y credenciales.

## `/templates/`
Archivos HTML si se utiliza Flask clásico con renderizado de servidor.

## `/static/`
Imágenes, CSS, JS — recursos estáticos.

## `/docs/`
Documentación técnica del sistema.

## `/tests/`
Pruebas unitarias o funcionales del backend.

## Archivos raíz
- `run.py`: Archivo principal para ejecutar la app.
- `requirements.txt`: Dependencias del proyecto.
- `.env`: Variables sensibles.
- `README.md`: Descripción general del proyecto.

