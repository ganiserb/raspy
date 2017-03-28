#!/usr/bin/env sh
tmux new-session -d -s monitor
tmux send-keys -t monitor 'python3 /home/pi/raspy/temperature_reader.py'

tmux new-session -d -s server
tmux send-keys -t server 'export PYTHONPATH=${PYTHONPATH}:${HOME}/raspy && python3 /home/pi/raspy/server/server.py'

#tmux new-session -d -s my_session 'python3 /home/pi/raspy/temperature_reader.py'
