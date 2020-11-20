#!/bin/bash

python3 -m venv app/venv
source app/venv/bin/activate
pip install -r requirements.txt
deactivate