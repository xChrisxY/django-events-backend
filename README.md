# 🎉 Event Management API

API RESTful para gestión de eventos desarrollada con **Django REST Framework** y autenticación **JWT**. Permite crear y administrar eventos, listas de artículos, imágenes, notas de audio y usuarios.

## 📋 Tabla de Contenidos

- [Descripción](#descripción)
- [Características](#características)
- [Tecnologías](#tecnologías)
- [Arquitectura](#arquitectura)
- [Requisitos Previos](#requisitos-previos)
- [Instalación](#instalación)
- [Configuración](#configuración)
- [Ejecución](#ejecución)
- [Autenticación JWT](#autenticación-jwt)
- [API Endpoints](#api-endpoints)
  - [Autenticación](#autenticación)
  - [Usuarios](#usuarios)
  - [Eventos](#eventos)
  - [Artículos](#artículos)
- [Modelos de Datos](#modelos-de-datos)
- [Ejemplos de Uso](#ejemplos-de-uso)
- [Estructura del Proyecto](#estructura-del-proyecto)
- [Pruebas](#pruebas)
- [Contribución](#contribución)
- [Licencia](#licencia)

## 📝 Descripción

Sistema completo para la gestión de eventos que permite:
- Creación y administración de eventos
- Gestión de participantes y organizadores
- Listas de artículos asociadas a eventos
- Subida de imágenes y notas de audio
- Autenticación segura mediante JWT
- Sistema de permisos granular

## ✨ Características

### Core
- ✅ CRUD completo de eventos
- ✅ Gestión de usuarios con autenticación JWT
- ✅ Listas de artículos por evento
- ✅ Subida de imágenes y archivos de audio
- ✅ Sistema de roles (organizador/participante)

### Seguridad
- ✅ Autenticación JWT (access/refresh tokens)
- ✅ Permisos personalizados por endpoint
- ✅ Validación de contraseñas
- ✅ Protección de rutas sensibles

### Multimedia
- ✅ Carga de imágenes para eventos
- ✅ Almacenamiento de notas de audio
- ✅ Soporte para múltiples formatos

## 🛠️ Tecnologías

- **Framework**: Django 5.1.7 + Django REST Framework
- **Autenticación**: JWT (djangorestframework-simplejwt)
- **Base de datos**: SQLite (desarrollo) / PostgreSQL (producción)
- **Multimedia**: Django FileField/ImageField
- **Logging**: Coloredlogs para desarrollo
- **Herramientas**: django-extensions

## 🏗️ Arquitectura

```
┌─────────────────────────────────────────────────────────────┐
│                         Cliente                              │
│                    (Web/Mobile App)                          │
└─────────────────────────┬───────────────────────────────────┘
                          │
┌─────────────────────────▼───────────────────────────────────┐
│                      Django REST API                         │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────────────┐  ┌─────────────────┐                  │
│  │   JWT Auth      │  │   Permissions   │                  │
│  └─────────────────┘  └─────────────────┘                  │
├─────────────────────────────────────────────────────────────┤
│                     URL Routing                              │
│  /api/v1/token/     /api/v1/events/     /api/v1/items/     │
└─────────────────────────────────────────────────────────────┘
                          │
┌─────────────────────────▼───────────────────────────────────┐
│                     Django Models                            │
├─────────────────────────────────────────────────────────────┤
│  ┌────────────┐  ┌────────────┐  ┌────────────┐           │
│  │   User     │  │   Event    │  │   Item     │           │
│  └────────────┘  └────────────┘  └────────────┘           │
│  ┌────────────┐  ┌────────────┐                            │
│  │ EventImage │  │ AudioNote  │                            │
│  └────────────┘  └────────────┘                            │
└─────────────────────────────────────────────────────────────┘
                          │
┌─────────────────────────▼───────────────────────────────────┐
│                      Base de Datos                           │
│                        SQLite                                │
└─────────────────────────────────────────────────────────────┘
```

## 📋 Requisitos Previos

- Python 3.8+
- pip
- virtualenv (recomendado)
- Git (opcional)

## 🚀 Instalación

1. **Clonar el repositorio**
```bash
git clone <url-del-repositorio>
cd event-management-api
```

2. **Crear y activar entorno virtual**
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# o
venv\Scripts\activate  # Windows
```

3. **Instalar dependencias**
```bash
pip install django djangorestframework djangorestframework-simplejwt django-extensions coloredlogs pillow
```

4. **Guardar dependencias (opcional)**
```bash
pip freeze > requirements.txt
```

5. **Realizar migraciones**
```bash
python manage.py makemigrations
python manage.py migrate
```

6. **Crear superusuario**
```bash
python manage.py createsuperuser
```

## ⚙️ Configuración

### Estructura de settings.py
El proyecto ya incluye configuración completa con:
- JWT Authentication
- Media files configuration
- Colored logs para desarrollo
- Permisos por defecto

### Variables de entorno recomendadas (para producción)
```bash
# config/settings.py
SECRET_KEY=your-secret-key-here
DEBUG=False
ALLOWED_HOSTS=your-domain.com
```

## 🎯 Ejecución

### Desarrollo
```bash
python manage.py runserver
```

El servidor se iniciará en `http://localhost:8000`

### Acceso a interfaces
- **API Root**: http://localhost:8000/api/v1/
- **Django Admin**: http://localhost:8000/admin/
- **JWT Endpoints**: http://localhost:8000/api/v1/token/

## 🔐 Autenticación JWT

### Obtener token
```http
POST /api/v1/token/
Content-Type: application/json

{
    "username": "usuario",
    "password": "contraseña"
}
```

**Respuesta:**
```json
{
    "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

### Refrescar token
```http
POST /api/v1/token/refresh
Content-Type: application/json

{
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

### Verificar token
```http
POST /api/v1/token/verify
Content-Type: application/json

{
    "token": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

## 📚 API Endpoints

### Autenticación

| Método | URL | Descripción | Permiso |
|--------|-----|-------------|---------|
| POST | `/api/v1/token/` | Obtener token JWT | AllowAny |
| POST | `/api/v1/token/refresh` | Refrescar token | AllowAny |
| POST | `/api/v1/token/verify` | Verificar token | AllowAny |

### Usuarios

| Método | URL | Descripción | Permiso |
|--------|-----|-------------|---------|
| POST | `/api/v1/users/register/` | Registrar nuevo usuario | AllowAny |
| GET | `/api/v1/users/profile/` | Ver perfil propio | IsAuthenticated |
| PUT | `/api/v1/users/update_profile/` | Actualizar perfil | IsAuthenticated |

### Eventos

| Método | URL | Descripción | Permiso |
|--------|-----|-------------|---------|
| GET | `/api/v1/events/` | Listar eventos del usuario | IsAuthenticated |
| POST | `/api/v1/events/` | Crear nuevo evento | IsAuthenticated |
| GET | `/api/v1/events/{id}/` | Ver detalle de evento | IsAuthenticated |
| PUT | `/api/v1/events/{id}/` | Actualizar evento | IsAuthenticated |
| DELETE | `/api/v1/events/{id}/` | Eliminar evento | IsAuthenticated |
| POST | `/api/v1/events/{id}/add_image/` | Añadir imagen | IsAuthenticated |
| POST | `/api/v1/events/{id}/add_note_audio/` | Añadir nota de audio | IsAuthenticated |
| GET | `/api/v1/events/{id}/item_list/` | Ver lista de artículos | IsAuthenticated |

### Artículos

| Método | URL | Descripción | Permiso |
|--------|-----|-------------|---------|
| GET | `/api/v1/items/?event_id={id}` | Listar artículos de evento | AllowAny |
| POST | `/api/v1/items/` | Crear artículo | IsAuthenticated |
| GET | `/api/v1/items/{id}/` | Ver detalle | AllowAny |
| PUT | `/api/v1/items/{id}/` | Actualizar | IsAuthenticated |
| DELETE | `/api/v1/items/{id}/` | Eliminar | IsAuthenticated |

## 💾 Modelos de Datos

### User (Django built-in)
```python
{
    "id": 1,
    "username": "juanperez",
    "email": "juan@email.com",
    "first_name": "Juan",
    "last_name": "Pérez"
}
```

### Event
```python
{
    "id": 1,
    "name": "Fiesta de Cumpleaños",
    "description": "Celebración de cumpleaños",
    "location": "Casa de Juan",
    "date": "2024-12-25",
    "time": "20:00:00",
    "organizer": {User},
    "participants": [User, User],
    "images": [EventImage],
    "audio_notes": [AudioNote]
}
```

### Item
```python
{
    "id": 1,
    "name": "Pastel",
    "responsible": {User},
    "status": "pending",
    "added_at": "2024-01-01T12:00:00Z",
    "updated_at": "2024-01-01T12:00:00Z"
}
```

## 💡 Ejemplos de Uso

### 1. Registro de usuario
```http
POST /api/v1/users/register/
Content-Type: application/json

{
    "username": "maria123",
    "email": "maria@email.com",
    "password": "Password123!",
    "password2": "Password123!",
    "first_name": "María",
    "last_name": "García"
}
```

### 2. Crear evento con autenticación
```http
POST /api/v1/events/
Authorization: Bearer <access_token>
Content-Type: application/json

{
    "name": "Fiesta de Fin de Año",
    "description": "Celebración de año nuevo",
    "location": "Plaza Principal",
    "date": "2024-12-31",
    "time": "22:00:00",
    "organizer_id": 1,
    "participants_ids": [2, 3]
}
```

### 3. Añadir imagen a evento
```http
POST /api/v1/events/1/add_image/
Authorization: Bearer <access_token>
Content-Type: multipart/form-data

image: [archivo]
caption: "Decoración de la fiesta"
```

### 4. Crear artículo para evento
```http
POST /api/v1/items/
Authorization: Bearer <access_token>
Content-Type: application/json

{
    "event_id": 1,
    "name": "Botanas",
    "responsible_id": 2
}
```

### 5. Filtrar artículos por evento
```http
GET /api/v1/items/?event_id=1
Authorization: Bearer <access_token>
```

## 📁 Estructura del Proyecto

```
event-management-api/
├── config/
│   ├── __init__.py
│   ├── settings.py           # Configuración principal
│   ├── urls.py               # URLs principales
│   ├── wsgi.py
│   └── asgi.py
├── apps/
│   ├── authentication/        # App de autenticación
│   │   ├── __init__.py
│   │   ├── serializers.py
│   │   ├── urls.py
│   │   ├── views.py
│   │   └── models.py
│   ├── event/                 # App de eventos
│   │   ├── __init__.py
│   │   ├── serializers.py
│   │   ├── urls.py
│   │   ├── views.py
│   │   └── models.py
│   └── item/                  # App de artículos
│       ├── __init__.py
│       ├── serializers.py
│       ├── urls.py
│       ├── views.py
│       └── models.py
├── media/                      # Archivos subidos
│   ├── event_images/
│   └── event_audio_notes/
├── manage.py
├── db.sqlite3
└── README.md
```

## 🧪 Pruebas

### Ejecutar pruebas
```bash
python manage.py test apps
```

### Pruebas específicas
```bash
python manage.py test apps.event.tests
python manage.py test apps.item.tests
python manage.py test apps.authentication.tests
```

### Ejemplo de prueba (event/tests.py)
```python
from django.test import TestCase
from django.contrib.auth.models import User
from apps.event.models import Event

class EventModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="12345")
        self.event = Event.objects.create(
            name="Test Event",
            location="Test Location",
            date="2024-12-31",
            time="20:00:00",
            organizer=self.user
        )
    
    def test_event_creation(self):
        self.assertEqual(self.event.name, "Test Event")
        self.assertEqual(self.event.organizer.username, "testuser")
```

## 🔒 Permisos

### Endpoints públicos
- GET /api/v1/items/ (solo con filtro event_id)
- POST /api/v1/users/register/

### Endpoints protegidos (requieren JWT)
- Todas las operaciones de escritura en eventos
- Gestión de artículos (POST, PUT, DELETE)
- Perfil de usuario

## 🤝 Contribución

1. Fork el proyecto
2. Crear rama feature (`git checkout -b feature/AmazingFeature`)
3. Commit cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abrir Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para más detalles.

---

## ✨ Mejoras Futuras

- [ ] Implementar paginación en listados
- [ ] Añadir búsqueda y filtros avanzados
- [ ] Implementar notificaciones por email
- [ ] Agregar tests de integración
- [ ] Documentar con Swagger/OpenAPI
- [ ] Implementar caché con Redis
- [ ] Migrar a PostgreSQL para producción
- [ ] Añadir rate limiting
- [ ] Implementar websockets para actualizaciones en tiempo real
- [ ] Agregar exportación de eventos a calendario

---

**Desarrollado con ❤️ usando Django REST Framework**
