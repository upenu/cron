#!/bin/bash
# runs add_events.py and updates events from facebook data.

BASE_DIR=~/apps/myapp/

# activate venv
. $BASE_DIR/venv/bin/activate

python $BASE_DIR/cron/add_events.py
