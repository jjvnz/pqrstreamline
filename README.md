# PQRStreamline

## Descripción
PQRStreamline es una aplicación para gestionar solicitudes y usuarios con autenticación JWT y OAuth2.

## Configuración

1. Crea un archivo `.env` con las variables necesarias.
2. Instala las dependencias con `pip install -r requirements.txt`.
3. Ejecuta las migraciones con `alembic upgrade head`.
4. Corre el servidor con `uvicorn app.main:app --reload --port 8080`.

## Endpoints

- **POST /auth/token**: Autenticación de usuarios.
- **POST /users/create**: Crear un nuevo usuario.
- **GET /users/{user_id}**: Obtener información de un usuario.
- **POST /requests/create**: Crear una nueva solicitud.

```
pqrstreamline/
├── alembic/
│   ├── versions/
│   └── env.py
├── app/
│   ├── api/
│   │   ├── __init__.py
│   │   ├── auth.py  # Endpoints de autenticación y autorización
│   │   ├── users.py  # Endpoints relacionados con usuarios
│   │   ├── requests.py  # Endpoints relacionados con solicitudes
│   ├── auth/
│   │   ├── __init__.py
│   │   ├── jwt.py  # Lógica para JWT
│   │   ├── oauth2.py  # Lógica para OAuth2
│   ├── email/
│   │   ├── __init__.py
│   │   ├── email_service.py  # Lógica para el envío de correos electrónicos
│   ├── models.py  # Definición de modelos SQLAlchemy
│   ├── schemas.py  # Esquemas Pydantic para validación
│   ├── crud.py  # Funciones CRUD para la base de datos
│   ├── dependencies.py  # Dependencias comunes de la API
│   ├── database.py  # Configuración de la base de datos
│   ├── config.py  # Configuraciones generales de la aplicación
│   ├── utils.py  # Funciones utilitarias generales
│   ├── main.py  # Punto de entrada de la aplicación FastAPI
├── tests/  # Directorio para pruebas unitarias e integración
│   ├── __init__.py
│   ├── test_users.py
│   ├── test_requests.py
├── venv/  # Entorno virtual de Python
├── alembic.ini  # Configuración de Alembic para migraciones
├── .env  # Variables de entorno
├── Dockerfile  # Archivo Docker para contenedorización
├── requirements.txt  # Dependencias de Python
├── .gitignore  # Archivos y carpetas ignoradas por git
└── README.md  # Documentación del proyecto
```
