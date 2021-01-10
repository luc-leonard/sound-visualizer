def boolean hasChangesIn(String module) {
  return !env.CHANGE_TARGET || sh(
    returnStatus: true,
    script: "git diff --name-only origin/${env.CHANGE_TARGET} ${env.GIT_COMMIT} | grep ^${module}/"
  ) == 0
}


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
		stage('PRE_BUILD') {
			steps {
				sh 'git config --add remote.origin.fetch +refs/heads/main:refs/remotes/origin/main'
				sh 'git fetch --no-tags'
			}
		}
	 	stage('ALL') {
	 		when {
	 			anyOf {
	 				 expression {
   						 return hasChangesIn('sound_visualizer')
  					}
					branch 'main'
	 			}
	 		}
			stages {
				stage('install deps') {
					steps {
						sh 'pwd'
						sh 'ls -l'
						sh 'pip install --cache-dir /pip-cache -r requirements_dev.txt'
						sh 'cp ./vendor/ffmpeg /bin/ffmpeg'
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
					when { branch 'main' }
					steps {
						sh 'make docker-api docker-worker'
					}
				}
				stage('deploy') {
					when { branch 'main' }
					steps {
						sh 'echo deploy'
					}
				}
			}
		}
	}
}