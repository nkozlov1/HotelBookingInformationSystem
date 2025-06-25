#!/usr/bin/env bash
set -euo pipefail

MIGR_DIR=${1:-migrations}
WORKDIR=$(mktemp -d)
PGURL="${DATABASE_URL}"

psql_cmd() { psql "$PGURL" -v ON_ERROR_STOP=1 "$@"; }
dump_schema() { pg_dump "$PGURL" --schema-only --no-owner --no-privileges; }

declare -A APPLIED

rollback_all() {
  (( ${#APPLIED[@]}==0 )) && return
  echo -e "Откатываем (${#APPLIED[@]})…"
  for v in $(printf '%s\n' "${!APPLIED[@]}" | sort -rn); do
      echo "V${v}"
      psql_cmd -f "${APPLIED[$v]}" || true
  done
}

trap 'rollback_all; exit 1' ERR
trap 'rollback_all' EXIT

echo "Проверка идемпотентности; миграции в $MIGR_DIR"


mapfile -t VERSIONS < <(find "$MIGR_DIR" -maxdepth 1 -type f -name 'V*__*.sql' \
                        ! -name '*_down.sql' \
                        | sed -E 's#.*/V([0-9]+)__.*#\1#' | sort -n)

if ((${#VERSIONS[@]}==0)); then
    echo "Не найдено ни одной миграции"; exit 1
fi

for V in "${VERSIONS[@]}"; do
    UP_FILE=$(ls "$MIGR_DIR"/V${V}__*.sql | grep -v '_down\.sql$' | head -n1)
    DOWN_FILE=$(ls "$MIGR_DIR"/U${V}__*.sql | head -n1)
    
    [[ -f "$DOWN_FILE" ]] || { echo "Для V$V нет down-скрипта"; continue; }

    echo -e "Версия V$V  (up: $(basename "$UP_FILE"),  down: $(basename "$DOWN_FILE"))"

    BASE=$(basename "$UP_FILE" .sql)
    SNAP1="$WORKDIR/${BASE}_1.sql"
    SNAP2="$WORKDIR/${BASE}_2.sql"
    
    psql_cmd -f "$UP_FILE"
    APPLIED["$V"]=$DOWN_FILE
    dump_schema > "$SNAP1"

    psql_cmd -f "$DOWN_FILE"
    unset 'APPLIED[$V]' 

    psql_cmd -f "$UP_FILE"
    APPLIED["$V"]=$DOWN_FILE
    dump_schema > "$SNAP2"

    if diff -u "$SNAP1" "$SNAP2" >/dev/null; then
        echo "$V идемпотентна"
    else
        echo " $V НЕ идемпотентна!"
        diff -u "$SNAP1" "$SNAP2" | head
        exit 1
    fi
    rm -f "$SNAP1" "$SNAP2"
done

echo -e "Все миграции идемпотентны!"
rm -rf "$WORKDIR"