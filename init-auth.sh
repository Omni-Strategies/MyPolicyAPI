#!/bin/bash
set -e

# Update pg_hba.conf to use md5/scram-sha-256 for all connections
cat > /var/lib/postgresql/data/pg_hba.conf <<EOF
# PostgreSQL Client Authentication Configuration
local   all             all                                     scram-sha-256
host    all             all             127.0.0.1/32            scram-sha-256
host    all             all             ::1/128                 scram-sha-256
host    all             all             0.0.0.0/0               md5
host    replication     all             127.0.0.1/32            scram-sha-256
host    replication     all             ::1/128                 scram-sha-256
host    replication     all             0.0.0.0/0               md5
EOF

chown postgres:postgres /var/lib/postgresql/data/pg_hba.conf
chmod 600 /var/lib/postgresql/data/pg_hba.conf
