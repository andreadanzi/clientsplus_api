#!/bin/bash
docker exec -i $1 mysql -uroot -proot clientsplus < sql/clientsplus.sql
