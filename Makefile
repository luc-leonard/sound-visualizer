###############################
# Configuration and variables #
###############################



#################
# General goals #
#################
isort = isort sound_visualizer
black = black sound_visualizer


format:
	$(isort)
	$(black)

lint:
	flake8 sound_visualizer
	$(isort) --check-only --df
	$(black) --check --diff
	mypy .
