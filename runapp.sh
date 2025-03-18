#!/bin/bash

cd ./server

sudo docker build -t chatapp .
sudo docker run -d -p 8080:8080 chatapp