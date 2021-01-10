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
docker: docker-api docker-worker docker-front

docker-api:
	docker build  -f docker/Dockerfile_api -t lucleonard/sound-visualizer-api:$(VERSION) -t lucleonard/sound-visualizer-api:latest .

docker-worker:
	docker build  -f docker/Dockerfile_worker \
			--build-arg WORKER_MAIN=sound_visualizer/worker/fft_calculator/main_worker.py \
			-t lucleonard/sound-visualizer-worker:$(VERSION) -t lucleonard/sound-visualizer-worker:latest .

	docker build  -f docker/Dockerfile_worker \
			--build-arg WORKER_MAIN=sound_visualizer/worker/downloader/main_worker.py \
 			-t lucleonard/sound-visualizer-downloader:$(VERSION) -t lucleonard/sound-visualizer-downloader:latest .

docker-front:
	docker build  -f docker/Dockerfile_front -t lucleonard/sound-visualizer-front:$(VERSION) -t lucleonard/sound-visualizer-front:latest .

docker-test:
	docker build  -f docker/Dockerfile_tests -t lucleonard/sound-visualizer-tests:$(VERSION) -t lucleonard/sound-visualizer-tests:latest .


docker-push:
		docker build  -f docker/Dockerfile_front -t registry:5000/lucleonard/sound-visualizer-front:latest .
		docker image push registry:5000/lucleonard/sound-visualizer-front:latest

		docker build  -f docker/Dockerfile_front -t registry:5000/lucleonard/sound-visualizer-api:latest .
		docker image push registry:5000/lucleonard/sound-visualizer-api:latest

		docker build  -f docker/Dockerfile_front -t registry:5000/lucleonard/sound-visualizer-worker:latest .
		docker image push registry:5000/lucleonard/sound-visualizer-worker:latest

test: docker-test
	- docker network create -d bridge sound-visualizer-testing-network
	docker run --network sound-visualizer-testing-network  -v /var/run/docker.sock:/var/run/docker.sock -v /usr/bin/docker:/usr/bin/docker lucleonard/sound-visualizer-tests:latest
