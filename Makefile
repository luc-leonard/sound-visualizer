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

docker_lint:
	POETRY =
	$(lint)

format:
	$(isort)
	$(black)

lint:
	$(POETRY) flake8 sound_visualizer tests
	$(isort) --check-only --df
	$(black) --check --diff
	$(POETRY) mypy .

.PHONY: docker
docker:
	docker build  -f docker/Dockerfile_web -t lucleonard/sound-visualizer-web:$(VERSION) -t lucleonard/sound-visualizer-web:latest .
	docker build  -f docker/Dockerfile_worker -t lucleonard/sound-visualizer-worker:$(VERSION) -t lucleonard/sound-visualizer-worker:latest .

publish:
	docker push lucleonard/sound-visualizer-web:$(VERSION)
	docker push lucleonard/sound-visualizer-web:latest

	docker push lucleonard/sound-visualizer-worker:$(VERSION)
	docker push lucleonard/sound-visualizer-worker:latest

run_web:
	gunicorn sound_visualizer.api.web.main_web:app --log-file -

run_worker:
	python sound_visualizer/api/worker/main_worker.py