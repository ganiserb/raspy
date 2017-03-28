#!/usr/bin/env sh
tmux new-session -d -s monitor ;
tmux send-keys -t monitor "python3 /home/pi/raspy/temperature_reader.py" Enter

#tmux new-session -d -s my_session 'python3 /home/pi/raspy/temperature_reader.py'
