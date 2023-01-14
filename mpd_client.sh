#!/bin/bash

## MPD client with notifications
### This just wraps mpc and adds notify-send commands
### for when the track or volume is changed manually

export MPD_HOST=${MPD_HOST:-127.0.0.1}

notify() {
    notify-send -a mpd_client -t ${TIMEOUT:-1000} --transient "$*"
}

notify_play_state() {
    notify "$(echo -e "$(mpc | head -2 | tail -1 | cut -d " " -f 1)\n$(mpc current)")"
}

notify_currently_playing(){
    notify "$(echo -e "$(mpc current)\n$(mpc | head -2 | tail -1)")"
}

notify_volume() {
    notify "$(mpc volume)"
}

notify_random() {
    notify "$(mpc | grep -o "random: \w*")"
}

main() {
    case $1 in
        next)
            mpc next
            notify_currently_playing
            ;;
        prev)
            mpc prev;
            notify_currently_playing
            ;;
        cdprev)
            mpc cdprev;
            notify_currently_playing
            ;;
        volume)
            shift
            mpc volume $*
            TIMEOUT=500 notify_volume
            ;;
        toggle)
            mpc toggle
            TIMEOUT=2000 notify_play_state
            ;;
        random)
            shift
            mpc random $*
            notify_random
            ;;
        state)
            TIMEOUT=5000 notify_currently_playing
            ;;
        *)
            echo "Invalid command. Use next, prev, cdprev, volume, toggle, random, state."
            exit 1
            ;;
    esac
}

main $*
