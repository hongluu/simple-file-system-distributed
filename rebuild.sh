#!/bin/sh
docker-compose down
docker rmi -f $(docker images |grep 'simple-file-system-distributed_')
docker-compose up