#!/bin/bash

gunicorn -c cloud_eval/gunicorn.conf.py server.main:app
sleep 10
python -m dsframework.base.cloud_eval.worker $1 $2
