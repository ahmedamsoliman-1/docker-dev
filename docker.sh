#!/bin/bash

# list container
docker ps -a

docker ps -a --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"
docker ps -a --format "table {{.Names}}"

# Delete exited container
docker stop $(docker ps -a -q --filter status=exited)
docker rm $(docker ps -a -q --filter status=exited)