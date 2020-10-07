#!/bin/sh

rsync -avP -e ssh --exclude=env/ --exclude=__pycache__ --exclude=log.txt . jayse@4hsl33p.team:borda_event