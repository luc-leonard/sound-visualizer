# sound-visualiser (name to be determined)

sound-visualizer aims to procude 3d images (render or real time) of sound files. It will display the frequency domain. 
the 3rd dimension will be time.

Currently, it is able to generate 2d colored spectrograms, with each instrument being assigned a color. 

## Installation

You will need to have [Poetry](https://python-poetry.org/) installed.

```$ poetry install```


## Usage
The application is relatively complex to deploy.
if you juste want to have fun, you can go [here](https://sound-visualizer.projects.luc-leonard.fr/) to try it

### BACKEND

To deploy the backend, you will need: 
* Google Cloud Engine account (for the object storage).
* a RabbitMQ server: it is used so the various components of the backend can communicate
* a mongoDB server

use [this file](./deployment_template/config.env) as a template to make your own config file

run make docker to build the docker images

use the provided [docker compose file](./docker/docker-compose.yml)
```shell
  docker-compose -f docker-compose.yml up
```

### FRONTEND

You will need nodejs.
```shell
cd website
yarn serve
```

## Examples
![example_1](examples/example_new.png)


![example_2](examples/example_new_2.png)

## Contributing
For now, it is just a personal repository :) feel free to fork it anyway.
