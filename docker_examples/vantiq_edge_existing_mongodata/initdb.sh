#!/bin/bash

# Restore from dump
mongorestore -u ars -p ars --db ars02 --drop --archive=/docker-entrypoint-initdb.d/mongodump_ars02
