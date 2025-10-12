#!/bin/bash
# Quick run script

cd "$(dirname "$0")"
source venv/bin/activate
python convert.py
