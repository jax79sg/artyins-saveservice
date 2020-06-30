#!/bin/bash
docker rmi -f artyins-saveservice
mkdir -p dockerdev
sudo rm -r dockerdev/artyins-saveservice
rsync -r ../artyins-saveservice dockerdev/
docker build ./dockerdev/. --no-cache -t artyins-saveservice
