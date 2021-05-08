#!/bin/bash

export PYTHONPATH=$PYTHONPATH:$PWD

cd src || exit
export VALIDATION_CONFIG_PATH=$PWD/service/validation_config.yaml

gunicorn -w 1 -b 0.0.0.0:5000 main:app