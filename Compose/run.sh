#!/bin/bash

redisCommander='redis-commander.yml'
jenkins='jenkins.yml'

docker-compose -f $redisCommander up
docker-compose -f $jenkins up

echo "--------------------------------------------------"