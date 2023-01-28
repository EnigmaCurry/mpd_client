.PHONY: help
help:
	@echo try 'make install'


.PHONY: install
install:
	poetry install

.PHONY: media-keys
media-keys:
	SNAPCAST_CLIENT=livingroom-amp INPUT_DEVICE=/dev/input/by-id/usb-Vaydeer_Vaydeer_Multimedia_Console-event-kbd poetry run python mpd_client/media_keys.py
