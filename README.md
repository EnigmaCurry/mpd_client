# mpd_client

This is a simple Music Player Daemon client, basically a thin wrapper
around `mpc` with Desktop notifications for manual track/volume
changes.

## Prerequisites

This is tested to be working on the following Linux distributions:

 * Arch Linux using i3wm
 * Ubuntu using Gnome

### Arch Linux

Gnome and other "big" desktop environment users will have
notifications already setup by default. i3wm users will need to
configure their [desktop
notifications](https://wiki.archlinux.org/title/Desktop_Notifications)
(and install a notifier like
[dunst](https://archlinux.org/packages/community/x86_64/dunst/)).

```
sudo pacman -S libnotify dunst
```

### Ubuntu

```
sudo apt update
sudo apt install -y mpc git
```

## Test desktop notifications

Before proceeding, test that desktop notifications are now working:

```
## This should popup a notification on your Desktop:
notify-send "Hello World!"
```

## Install

```
git clone https://github.com/EnigmaCurry/mpd_client.git \
    ~/git/vendor/enigmacurry/mpd_client
mkdir -p ~/bin
ln -sf ~/git/vendor/enigmacurry/mpd_client/mpd_client.sh \
    ~/bin/mpd_client.sh
```

## Config

The client is designed to be used entirely from keyboard shortcuts,
without any graphical interface. Desktop Notifications are used for
feedback to the user.

You can choose whatever keybindings you want, but here is a cheatsheet
for the suggested bindings:

| Keybinding            | Use                           |
|-----------------------|-------------------------------|
| `Win` + `=`           | volume +5                     |
| `Win` + `-`           | volume -5                     |
| `Win` + `Shift` + `=` | volume +1                     |
| `Win` + `Shift` + `-` | volume -1                     |
| `Win` + `[`           | previous track                |
| `Win` + `]`           | next track                    |
| `Win` + `Shift` + `[` | CD-player like previous track |
| `Win` + `Shift` + `]` | Toggle random play            |
| `Win` + `p`           | Toggle play/pause             |
| `Win` + `Shift` + `p` | Show current track playing    |
| `Win` + `Alt` + `p`   | Clear and load next playlist  |

### Set the MPD_HOST environment variable

Edit the configuration of your **login shell**, usually this is
`~/.profile`:

```
## Set MPD configuration in your ~/.profile:
# Set the IP address or host name of your (remote) MPD daemon:
# You can prefix a password@ , if your server requires it, eg. 
## export MPD_HOST=my_dumb_password@192.168.0.45
export MPD_HOST=127.0.0.1
```

You should log out of your desktop environment and log back in, so the
config is fully applied.

You can test that the connection works, using `mpc`:

```
## mpc uses the host as defined by MPD_HOST variable:
mpc status
```

If its working, this should print the status of your (remote) MPD
server.

### i3wm config

For [i3wm](https://i3wm.org/) users, use this config:

```
# mpd_client
bindsym $mod+equal exec "~/bin/mpd_client.sh volume +5"
bindsym $mod+Shift+equal exec "~/bin/mpd_client.sh volume +1"
bindsym $mod+minus exec "~/bin/mpd_client.sh volume -5"
bindsym $mod+Shift+minus exec "~/bin/mpd_client.sh volume -1"
bindsym $mod+bracketleft exec "~/bin/mpd_client.sh prev"
bindsym $mod+Shift+bracketleft exec "~/bin/mpd_client.sh cdprev"
bindsym $mod+bracketright exec "~/bin/mpd_client.sh next"
bindsym $mod+Shift+bracketright exec "~/bin/mpd_client.sh random"
bindsym $mod+p exec "~/bin/mpd_client.sh toggle"
bindsym $mod+Shift+p exec "~/bin/mpd_client.sh state"
bindsym $mod+Mod1+p exec "~/bin/mpd_client.sh next_playlist"
```

### Gnome config

Gnone doesn't have an easy config file to edit to add custom
shortcuts, but you can add them manually via the Gnome `Settings`
application:

 * In the settings, find `Keyboard`
 * Then find `View and Customize Shortcuts`
 * At the bottom of the list, find `Custom Shortcuts`.

Using the same commands as listed in the [i3wm config](#i3wm-config),
create a custom shortcut for each one:
 * Click the `Add Shortcut` button or `+` icon to add a shortcut.
 * Enter any descriptive name.
 * Enter the command, eg. `/home/USER/bin/mpd_client.sh volume +5`
   * Note that `~` expansion does not work here, so you have to
     pedantically specify the absolute path to the script.
 * Click `Set Shortcut` and then record the keyboard shortcut by
   pressing the desired keys.
 * Repeat for each shortcut you want.

Note: on Ubuntu Gnome, I experienced a problem attempting to bind
`Win` + `p`, apparently these single letter combinations are reserved
(It does not say there is a conflict.) You can try using another
adjacent non-letter key instead, eg `\`.
