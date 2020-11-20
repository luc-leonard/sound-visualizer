###############################
# Configuration and variables #
###############################



#################
# General goals #
#################
POETRY = poetry run
isort = $(POETRY) isort sound_visualizer tests
black = $(POETRY) black sound_visualizer tests


format:
	$(isort)
	$(black)

lint:
	$(POETRY) flake8 sound_visualizer tests
	$(isort) --check-only --df
	$(black) --check --diff
	$(POETRY) mypy .


docker:
	docker build . -t luc-leonard/sound-visualizer:latest


start_webserver:
	$(POETRY) gunicorn sound_visualizer.main_api:app
