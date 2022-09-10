#!/bin/bash
# Внимание при запуске контейнеров на винде необходимо line endings
#  в баш скриптах сменить с CRLF на LF иначе они не сработают
set -e
DB_NAME=unwind_db
DB_USER=unwind
DB_USER_PASS=password
psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" <<-EOSQL
    CREATE USER $DB_USER WITH PASSWORD '$DB_USER_PASS';
    CREATE DATABASE $DB_NAME WITH ENCODING = 'UTF8' CONNECTION LIMIT = -1 ;
    GRANT ALL PRIVILEGES ON DATABASE $DB_NAME TO $DB_USER ;
EOSQL
