#!/usr/bin/env bash
set -e
export PYTHONPATH=".:$PYTHONPATH"
python3 -m adventure_forge.flywheel.loop run --cycles 10
