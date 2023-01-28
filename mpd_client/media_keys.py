#!/bin/env python3

import os
import subprocess
from threading import Timer
import asyncio

from evdev import InputDevice, categorize, ecodes
from evdev.ecodes import EV_KEY as EV_KeyboardEvent, ecodes as event_codes
import snapcast.control


def __require_env_vars(*env_vars):
    missing_vars = []
    for var in env_vars:
        if len(os.environ.get(var, "")) == 0:
            missing_vars.append(var)
    if len(missing_vars) > 0:
        raise AssertionError(
            f"Missing environment variables: {', '.join(missing_vars)}"
        )


## Required environment variables:
__require_env_vars("INPUT_DEVICE", "MPD_HOST", "SNAPCAST_HOST", "SNAPCAST_CLIENT")
INPUT_DEVICE = os.environ["INPUT_DEVICE"]
MPD_HOST = os.environ["MPD_HOST"]
SNAPCAST_HOST = os.environ["SNAPCAST_HOST"]
SNAPCAST_CLIENT = os.environ["SNAPCAST_CLIENT"]
VOLUME_SENSITIVITY = os.environ.get("VOLUME_SENSITIVITY", 3)

CURRENT_ALT_MODE = 0


def __subprocess_run(*args, **kwargs):
    print(f"##$ {args[0]}")
    return subprocess.run(*args, **kwargs)


def __trigger_alt_mode():
    """
    Set global CURRENT_ALT_MODE=1, then set CURRENT_ALT_MODE=0 after 1s elapsed.
    """
    global CURRENT_ALT_MODE
    CURRENT_ALT_MODE = 1
    Timer(1, __reset_alt_mode).start()


def __reset_alt_mode():
    global CURRENT_ALT_MODE
    CURRENT_ALT_MODE = 0


def mute():
    """
    Mute button is repurposed as a leader key, and not as an actual mute switch

    Press the mute button quickly before pressing another key to perform an alternate action.
    """
    __trigger_alt_mode()


def volume_up(snapcast_client):
    """
    Raise snapcast client volume
    """
    pass


def volume_down(snapcast_client):
    """
    Lower snapcast client volume
    """
    pass


def previous_track():
    """
    MPD previous track
    """
    if CURRENT_ALT_MODE == 1:
        __subprocess_run(("mpc", "clear"), capture_output=True)
        __subprocess_run(("mpc", "load", "Groove Salad Classic"), capture_output=True)
        __subprocess_run(("mpc", "play"), capture_output=True)
    else:
        __subprocess_run(("mpc", "prev"), capture_output=True)


def next_track():
    """
    MPD next track
    """
    if CURRENT_ALT_MODE == 1:
        __subprocess_run(("mpc", "clear"), capture_output=True)
        __subprocess_run(("mpc", "load", "Whomps"), capture_output=True)
        __subprocess_run(("mpc", "play"), capture_output=True)
    else:
        __subprocess_run(("mpc", "next"), capture_output=True)


def play_pause():
    """
    MPD play/pause toggle
    """
    if CURRENT_ALT_MODE == 1:
        __subprocess_run(("mpc", "clear"), capture_output=True)
        __subprocess_run(("mpc", "load", "Drone Zone"), capture_output=True)
        __subprocess_run(("mpc", "play"), capture_output=True)
    else:
        __subprocess_run(("mpc", "toggle"), capture_output=True)


async def keyboard_event_listener(snapcast_client):
    dev = InputDevice(INPUT_DEVICE)
    # print("## Finding ALSA device ...")
    # if __subprocess_run(("amixer", "sget", ALSA_MIXER_CONTROL)).returncode != 0:
    #     print(f"Could not find the ALSA device named {repr(ALSA_MIXER_CONTROL)}")
    #     print("Try finding the actual device name by running 'amixer'")
    #     print("Set the device name as the env var ALSA_MIXER_CONTROL")
    #     raise AssertionError(
    #         f"Could not find an ALSA control named {ALSA_MIXER_CONTROL}"
    #     )
    # print("## Found ALSA device")
    print("## Testing MPD connection")
    if __subprocess_run(("mpc", "status")).returncode != 0:
        print(
            "Could not connect to MPD. Try (re)setting the MPD_HOST environment variable."
        )
    print("")
    print("## Watching for keyboard events ...")
    async for event in dev.async_read_loop():
        ## poll for keyboard key down events only:
        if event.type == EV_KeyboardEvent and event.value == 1:
            if event.code == event_codes["KEY_MUTE"]:
                mute()
            if event.code == event_codes["KEY_VOLUMEUP"]:
                await snapcast_client.set_volume(
                    min(100, snapcast_client.volume + VOLUME_SENSITIVITY)
                )
            elif event.code == event_codes["KEY_VOLUMEDOWN"]:
                await snapcast_client.set_volume(
                    max(0, snapcast_client.volume - VOLUME_SENSITIVITY)
                )
            elif event.code == event_codes["KEY_PREVIOUSSONG"]:
                previous_track()
            elif event.code == event_codes["KEY_PLAYPAUSE"]:
                play_pause()
            elif event.code == event_codes["KEY_NEXTSONG"]:
                next_track()


async def media_keys():
    loop = asyncio.get_event_loop()
    snapcast_server = await snapcast.control.create_server(loop, SNAPCAST_HOST)
    for snapcast_client in snapcast_server.clients:
        if snapcast_client.friendly_name == SNAPCAST_CLIENT:
            break
    else:
        raise RuntimeError(f"Could not find snapcast client: {SNAPCAST_CLIENT}")

    keyboard_listener_task = asyncio.create_task(
        keyboard_event_listener(snapcast_client)
    )
    await keyboard_listener_task
    loop.run_forever()


def main():
    asyncio.run(media_keys())


if __name__ == "__main__":
    main()
