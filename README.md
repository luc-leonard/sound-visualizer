# sound-visualiser (name to be determined)

sound-visualizer aims to procude 3d images (render or real time) of sound files. It will display the frequency domain. 
the 3rd dimension will be time.

Currently, it generates spectrogram of wholes track, as greyscale images. It can be used as a CLI tool, or as a web app. 

## Installation

You will need to have [Poetry](https://python-poetry.org/) installed.

```$ poetry install```


You can also use docker. There is an image on dockerhub [here](https://hub.docker.com/repository/docker/lucleonard/sound-visualizer)
You can also make your own image by using

```$ make docker```

## Usage
### as a web server

To deploy this app yourself, you will need a Google Cloud Engine account.
Specific environment variable must be set. See [this file](deployment_template/config.env)

The application has 2 layers: web and worker that communicates using Google PubSub

#### directly
run ```make web``` and ```make worker```  and go to http://localhost:5000
#### with docker

You can use this [docker-compose file](docker_files/docker-compose.yml). If the images are not on dockerhub you can
build them with ```make docker```

#### heroku
The application can be deployed on heroku. Procfile is provided

If you want to try it, it is also deployed at https://luc-leonard-sound-visualizer.herokuapp.com/

### as a CLI tool (NOT ACTIVELY MAINTENED)
#### the arguments
* --filename <filename>: the wav to analyse
* --frame_size: the size of the frames that will be used for the FFT transform. It should be a power of 2 such as 1024 or 2048
 You should make it higher if you want to analyse lower frequencies.
* --overlap_factor: how much the frames will overlap ? the more, the better, but the more memory it will use
* --start: where to start in the wav, in seconds
* --length: how much second of sound to analyse
* --low-cut:  this will ignore lower frequencies when displaying data
* --high-cut: this will ignore higher frequencies when displaying data
* --output-folder: where to output the images

```$ poetry run python sound_visualizer/cli/main.py <args>```


## Examples
![example_1](examples/example_new.png)


![example_2](examples/example_new_2.png)

## Contributing
For now, it is just a personal repository :) feel free to fork it anyway.
