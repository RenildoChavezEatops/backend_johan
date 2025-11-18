FROM python:3.12-slim

# Evitar buffering
ENV PYTHONUNBUFFERED=1

# Crear directorio
WORKDIR /app

# Instalar dependencias del sistema (por ejemplo psycopg2)
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copiar requirements
COPY requirements.txt .

# Instalar dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copiar proyecto
COPY . .

# Archivo que realiza migraciones de Django
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]

# Exponer puerto del servidor ASGI
EXPOSE 8001

# Comando para correr WebSockets + HTTP
CMD ["daphne", "-b", "0.0.0.0", "-p", "8001", "config.asgi:application"]
