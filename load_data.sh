#!/bin/bash
docker exec -i $1 mysql -uroot -proot < sql/clientsplus.sql
