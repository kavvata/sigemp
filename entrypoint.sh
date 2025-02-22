#!/bin/env bash

while true; do
    glpi-agent --server http://host.docker.internal:8000/ativos/inventory/
    sleep 300
done
