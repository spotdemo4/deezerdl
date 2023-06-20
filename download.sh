#!/bin/bash
songname="'$*'"
docker exec -it deezerdl /opt/venv/bin/python download.py $songname