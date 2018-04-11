#!/usr/bin/env bash

if [[ $1 = "docker" ]]; then
    containers=$(docker ps -q)
    all_containers=$(docker ps -a -q)
    images=$(docker images -q)
    networks=$(docker network ls -q)
    volumes=$(docker volume ls -q)

    echo Stop containers ...
    if [[ $containers != "" ]]; then docker stop $containers; fi

    echo Remove containers ...
    if [[ $all_containers != "" ]]; then docker rm -f $all_containers; fi

    echo Remove images ...
    if [[ $images != "" ]]; then docker rmi -f $images; fi

    echo Remove networks ...
    if [[ $networks != "" ]]; then docker network rm $networks; fi

    echo Remove volumes ...
    if [[ $volumes != "" ]]; then docker volume rm $volumes; fi

    echo Done
elif [[ $1 = "archive" ]]; then
    archive=~/Desktop/$(basename "$PWD").zip
    zip -rq $archive .
    echo $archive
else
    echo Unknown command
fi
