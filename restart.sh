#!/bin/sh

echo "----" >> log.txt
echo "RESTART START" >> log.txt
echo $(date) >> log.txt
docker-compose down && docker-compose up -d --build
echo $(date) >> log.txt
echo "RESTART DONE" >> log.txt
echo "----" >> log.txt