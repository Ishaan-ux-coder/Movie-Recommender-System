#!/bin/bash
# Exit on error
set -o errexit

pip install -r requirements.txt
python rebuild_pickles.py
