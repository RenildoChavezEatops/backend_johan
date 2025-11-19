Proyecto Django + WebSockets + Docker
-
Este proyecto utiliza:

Django como backend

Daphne (ASGI) para manejo de HTTP y WebSockets

Redis como Channel Layer

PostgreSQL 15 como base de datos

Docker Compose para orquestación

Todo se levanta con un solo comando.

Requisitos previos
-
Asegúrate de tener instalado:

Docker

Docker Compose

1. Crear archivo .env

    Crea un archivo .env en la raíz del proyecto con la estructura del .env.example.

2. Levantar el proyecto con Docker

    Ejecuta:

    docker compose up --build
    
    Esto hace:
    
    Construye la imagen de Django.
    
    Inicia Redis y PostgreSQL.
    
    Espera a que la base de datos esté lista.
    
    Aplica migraciones automáticas.
    
    Inicia Daphne ASGI en 0.0.0.0:8001.

3. Acceso al backend

    Backend disponible en:
    
    http://localhost:8001
    
    Ejemplo del endpoint de registro:
    
    POST http://localhost:8001/api/users/register/

4. Verificar WebSockets

    Conéctate a:
    
    ws://localhost:8001/ws/chat/
    
    Puedes probar usando:
    
    websocat
    
    wscat
    
    Extensión "WebSocket Client" de VSCode
    
    Ejemplo con wscat:
    
    wscat -c ws://localhost:8001/ws/chat/


5. Entrar a un contenedor

    Contenedor Django
    
    docker exec -it django_app sh
    
    Contenedor PostgreSQL
    
    docker exec -it postgres_db bash
    
    Contenedor Redis
    
    docker exec -it redis_ws sh

6. Ver logs en tiempo real

    Todos los servicios:
    
    docker compose logs -f
    
    Solo Django:
    
    docker logs -f django_app
    
    Solo DB:
    
    docker logs -f postgres_db

7. Probar API con Postman

    Endpoint ejemplo: Registro de usuarios
    
    POST http://localhost:8001/api/users/register/
    
    Body (JSON):
    
    {
      "email": "test@example.com",
      "username": "testuser",
      "password": "12345678"
    }
    
    Respuesta esperada:
    
    {
    
        "email": "test@example.com",
        "username": "testuser"
    }

    Esto crea un usuario inactivo, en la consola de la aplicación de Django se mostrará el siguiente mensaje:
    
    Subject: Verifica tu correo
    
    django_app   | From: johan.jara@test
    
    django_app   | To: qwer_jv16@outlook.com
    
    django_app   | Date: Tue, 18 Nov 2025 12:18:17 -0000
    
    django_app   | Message-ID: <176346829708.1.14758019794033890896@718767defdc3>
    
    django_app   | 
    
    django_app   | Hola testuser, haz click aquí para verificar tu cuenta:
    
    django_app   | http://localhost:8001/api/auth/verify-email/?uid=1&token=czgcah-a4d703cd9b96f532ce0623c78fd31c33
    
    django_app   | -------------------------------------------------------------------------------
    
    Ingresar en el navegador la url para que el usuario se active


8. Estructura del Docker Compose

    Este proyecto usa los siguientes servicios:
    
    Servicio	Puerto	Descripción
    
    django_app	8001	Servidor ASGI con Daphne
    
    redis	6380 externo / 6379 interno	Channel Layer
    
    postgres_db	5433 externo / 5432 interno	Base de datos


9. EntryPoint (Daphne + Migraciones)

    El archivo entrypoint.sh ejecuta:
    
    Esperar DB
    
    Migrar
    
    Levantar servidor ASGI
