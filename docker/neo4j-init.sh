#!/bin/bash

set -e

if [ ! -f /var/lib/neo4j/data/imported ]; then
    neo4j-admin database load courseproject2024.db --from-path=/var/lib/neo4j/import --overwrite-destination
    touch /var/lib/neo4j/data/imported
    chown neo4j:neo4j -R data/databases/courseproject2024.db
fi
