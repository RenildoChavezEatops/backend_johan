#!/bin/sh

echo "Esperando a la base de datos..."
/wait-for-it.sh db:5432 --timeout=30 --strict -- echo "Base de datos lista."

echo "Aplicando migraciones..."
python manage.py migrate --noinput

echo "Iniciando Daphne (ASGI)..."
exec daphne -b 0.0.0.0 -p 8001 config.asgi:application