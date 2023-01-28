.PHONY: help
help:
	@echo try 'make install'

.PHONY: install-poetry
install-poetry:
	@(which poetry || test -f ${HOME}/.local/bin/poetry) || (curl -sSL https://install.python-poetry.org | python3 -)

.PHONY: install
install:
	poetry install
	systemctl --user link ./media-keys.service
	systemctl --user daemon-reload
	systemctl --user enable --now media-keys.service

.PHONY: media-keys
media-keys:
	@bash -c "source .env && ${HOME}/.local/bin/poetry run python mpd_client/media_keys.py"
