#!/bin/bash

## MPD client with notifications
### This just wraps mpc and adds notify-send commands
### for when the track or volume is changed manually

export MPD_HOST=${MPD_HOST:-127.0.0.1}

## Cache remembers the last loaded playlist so you can cycle them:
CACHE_DIR=${HOME}/.cache/enigmacurry_mpd_client
mkdir -p ${CACHE_DIR}

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

load_next_playlist() {
    ## Search the cache for the name of the last loaded playlist
    if [ -f ${CACHE_DIR}/last_playlist.txt ]; then
        total_playlists=$(mpc lsplaylists | wc -l)
        last_playlist=$(cat ${CACHE_DIR}/last_playlist.txt | head -1)
        playlist_num=$(mpc lsplaylists | grep -n "^${last_playlist}$" | head -1 | cut -d ":" -f 1)
        if (( "${playlist_num}" < "${total_playlists}" )); then
            playlist_num=$(( "${playlist_num}" + 1 ))
        else
            playlist_num=1
        fi
    else
        playlist_num=1
    fi
    next_playlist=$(mpc lsplaylists | sed -n "${playlist_num},${playlist_num} P")
    mpc clear
    mpc load "${next_playlist}"
    TIMEOUT=1500 notify "Loaded playlist: ${next_playlist}"
    echo "${next_playlist}" > ${CACHE_DIR}/last_playlist.txt
}

main() {
    set -eo pipefail
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
        next_playlist)
            load_next_playlist
            ;;
        *)
            echo "Invalid command. Use next, prev, cdprev, volume, toggle, random, state."
            exit 1
            ;;
    esac
}

main $*
