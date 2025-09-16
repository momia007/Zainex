#!/bin/bash

DB_NAME="zainex_scout"
DUMP_FILE="backup_neon_clean.sql"
NEON_URL="postgresql://neondb_owner:npg_Xgh1SOkFdG0N@ep-orange-cell-addratno-pooler.c-2.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require"

echo "🚀 Iniciando sincronización desde Neon a entorno local..."

# Paso 1: Generar dump limpio desde Neon usando Docker
echo "📦 Generando dump limpio desde Neon..."
docker run --rm \
  -e PGPASSWORD='npg_Xgh1SOkFdG0N' \
  postgres:17 \
  pg_dump "$NEON_URL" \
  --no-owner \
  --no-privileges \
  -F p \
  > "$DUMP_FILE"

# Verificar que el dump se haya generado correctamente
if [ ! -s "$DUMP_FILE" ]; then
  echo "❌ Error: El archivo '$DUMP_FILE' está vacío o no se generó correctamente."
  exit 1
fi

echo "✅ Dump generado: $DUMP_FILE"

# Paso 2: Eliminar base local si existe
echo "🧨 Eliminando base local '$DB_NAME' si existe..."
sudo -u postgres dropdb --if-exists "$DB_NAME"

# Paso 3: Crear base vacía
echo "🧱 Creando base '$DB_NAME'..."
sudo -u postgres createdb "$DB_NAME"

# Paso 4: Restaurar el dump
echo "📥 Restaurando dump en base local..."
sudo -u postgres psql -d "$DB_NAME" -f "$DUMP_FILE"

# Paso 5: Verificar tablas importadas
echo "🔍 Verificando tablas en '$DB_NAME'..."
sudo -u postgres psql -d "$DB_NAME" -c "\dt"

echo "🎉 Sincronización completa. La base '$DB_NAME' está actualizada con datos desde Neon."
