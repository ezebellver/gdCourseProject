#!/bin/bash

set -e

if [ ! -f /tmp/neo4j-imported ]; then
    neo4j-admin database load courseproject2024.db --from-path=/var/lib/neo4j/import --overwrite-destination
    touch /tmp/neo4j-imported
fi
