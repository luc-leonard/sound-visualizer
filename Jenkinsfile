pipeline {
	agent {
	  docker {
	  	image 'python:3.9-buster'
	    args '''-v $HOME/.pip:/pip-cache
	    		-e _IN_DOCKER=1
	          -v /var/run/docker.sock:/var/run/docker.sock
	          -v /usr/bin/docker:/usr/bin/docker
	          --network sound-visualizer-testing-network
	          '''
	   }
	}

    stages {
		stage('install deps') {
		  steps {
			sh 'pwd'
			sh 'ls -l'
			sh 'pip install --cache-dir /pip-cache -r requirements_dev.txt'
		  }
		}
		stage('Lint') {
				steps {
					sh 'make docker_lint'
				}
			}
		stage ('test') {
			steps {
				sh 'pytest'
			}
		}
		stage('build docker image') {
				steps {
					sh 'make docker-api docker-worker'
				}
		}
   }
}