#!/usr/bin/env bash
set -euo pipefail

PGHOST="${POSTGRES_HOST:-haproxy}"
PGPORT="${POSTGRES_PORT:-5001}"
PGUSER="${POSTGRES_USER:-myuser}"
PGDATABASE="${POSTGRES_DB:-postgres}"
PGPASSWORD="${POSTGRES_PASSWORD:-mypassword}"
export PGPASSWORD

BACKUP_DIR="${BACKUP_DIR:-/backups}"
KEEP="${BACKUP_RETENTION_COUNT:-10}"

mkdir -p "${BACKUP_DIR}"

STAMP=$(date +%Y%m%d_%H%M%S)
FILE="pg_${STAMP}.dump"
TARGET="${BACKUP_DIR}/${FILE}"

echo "[backup] $(date)  →  ${FILE}"

pg_dump -h "${PGHOST}" -p "${PGPORT}" -U "${PGUSER}" -d "${PGDATABASE}" \
  | gzip > "${TARGET}"

count=$(ls -1 "${BACKUP_DIR}"/pg_*.dump 2>/dev/null | wc -l)
if [ "${count}" -gt "${KEEP}" ]; then
  ls -1t "${BACKUP_DIR}"/pg_*.dump | tail -n +"$((KEEP+1))" | xargs -r rm -f
fi