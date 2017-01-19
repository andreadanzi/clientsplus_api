#!/bin/bash
docker run -it --rm -v /data/python/logs:/usr/src/app/logs --name running-app python-app