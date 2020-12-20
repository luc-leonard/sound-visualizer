###############################
# Configuration and variables #
###############################
VERSION=0.1.0
#################
# General goals #
#################
POETRY = poetry run
isort =  isort sound_visualizer tests
black = black sound_visualizer tests
#VERSION = `poetry run python get_version.py`

install:
	poetry install

docker_lint:
	flake8 sound_visualizer tests
	$(isort) --check-only --df
	$(black) --check --diff
	mypy .

format:
	$(POETRY) $(isort)
	$(POETRY) $(black)

lint:
	$(POETRY) flake8 sound_visualizer tests
	$(POETRY) $(isort) --check-only --df
	$(POETRY) $(black) --check --diff
	$(POETRY) mypy .

.PHONY: docker
docker:
	docker build  -f docker/Dockerfile_api -t lucleonard/sound-visualizer-api:$(VERSION) -t lucleonard/sound-visualizer-api:latest .
	docker build  -f docker/Dockerfile_worker -t lucleonard/sound-visualizer-worker:$(VERSION) -t lucleonard/sound-visualizer-worker:latest .
	docker build  -f docker/Dockerfile_front -t lucleonard/sound-visualizer-front:$(VERSION) -t lucleonard/sound-visualizer-front:latest .

publish:
	docker push lucleonard/sound-visualizer-web:$(VERSION)
	docker push lucleonard/sound-visualizer-web:latest

	docker push lucleonard/sound-visualizer-worker:$(VERSION)
	docker push lucleonard/sound-visualizer-worker:latest

run_web:
	gunicorn sound_visualizer.api.web.main_web:app --log-file -

run_worker:
	python sound_visualizer/api/worker/main_worker.py