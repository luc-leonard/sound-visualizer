###############################
# Configuration and variables #
###############################



#################
# General goals #
#################
isort = isort sound_visualizer tests
black = black sound_visualizer tests


format:
	$(isort)
	$(black)

lint:
	flake8 sound_visualizer tests
	$(isort) --check-only --df
	$(black) --check --diff
	mypy .
