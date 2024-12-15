#!/bin/bash

set -e

if [ ! -f /tmp/neo4j-imported ]; then
    neo4j-admin database load courseproject2024.db --from-path=/var/lib/neo4j/import --overwrite-destination
    touch /tmp/neo4j-imported
    chown neo4j:neo4j -R data/databases/courseproject2024.db
fi
