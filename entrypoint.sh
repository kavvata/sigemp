#!/bin/env bash

while true; do
    glpi-agent --server http://localhost:8000/ativos/inventory/
    sleep 300
done
