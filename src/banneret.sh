#!/usr/bin/env bash

echo Stop containers ...
docker stop `docker ps -q`

echo Remove containers ...
docker rm `docker ps -a -q`

echo Remove images ...
docker rmi -f `docker images -q`

echo Remove networks ...
docker network rm `docker network ls -q`

echo Remove volumes ...
docker volume rm `docker volume ls -q`

echo Done
