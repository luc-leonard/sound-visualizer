pipeline {
	agent {
	  docker {
	    image 'python:3.9-buster'
	    args '''-v $HOME/.pip:/pip-cache
	          -v /var/run/docker.sock:/var/run/docker.sock \
	          -v /usr/bin/docker:/usr/bin/docker'''
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
		stage ('yarn build') {
		   agent {
			docker {
					image 'node:15'
					args '''-v $HOME/.node_module:/node_module
							-v /var/run/docker.sock:/var/run/docker.sock \
							-v /usr/bin/docker:/usr/bin/docker'''
					}
				}
			}
			steps {
				sh 'yarn build --mode production'
				sh 'make docker-front'
			}
	 	}
	}
}