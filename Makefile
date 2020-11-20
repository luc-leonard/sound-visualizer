###############################
# Configuration and variables #
###############################



#################
# General goals #
#################
POETRY = poetry run
isort = $(POETRY) isort sound_visualizer tests
black = $(POETRY) black sound_visualizer tests
VERSION = `poetry run python get_version.py`

install:
	poetry install

format:
	$(isort)
	$(black)

lint:
	$(POETRY) flake8 sound_visualizer tests
	$(isort) --check-only --df
	$(black) --check --diff
	$(POETRY) mypy .


docker:
	docker build . -t lucleonard/sound-visualizer:$(VERSION)

publish:
	docker push lucleonard/sound-visualizer:$(VERSION)

start_webserver: install
	$(POETRY) gunicorn sound_visualizer.main_api:app
