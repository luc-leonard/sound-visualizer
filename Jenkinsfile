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
	    args '''-v $HOME/.pip:/pip-cache \
	    		-e _IN_DOCKER=1 \
	          -v /var/run/docker.sock:/var/run/docker.sock \
	          -v /usr/bin/docker:/usr/bin/docker \
	          --network sound-visualizer-testing-network \
	          -e CAPROVER_PASS=$CAPROVER_PASS
	          '''
	   }
	}

	stages {
		stage('PRE_BUILD') {
			steps {
				// this allows us to reference trhe main branch
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
						sh 'apt-get update'
						sh 'apt-get install -y libsndfile-dev'
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
					when { branch 'main'}
					steps {
						sh 'make docker-api docker-worker'
					}
				}
				stage('deploy') {
					when { branch 'main'}
					steps {
						sh 'echo deploy'
						sh 'make docker-push'
						sh '''docker run caprover/cli-caprover:v2.1.1 caprover deploy --caproverUrl https://captain.projects.luc-leonard.fr \
						      --caproverPassword $CAPROVER_PASS \
						      --caproverApp sound-visualizer-api \
						      --imageName kimsufi.luc-leonard.fr:5000/lucleonard/sound-visualizer-api:latest'''
						sh '''docker run caprover/cli-caprover:v2.1.1 caprover deploy --caproverUrl https://captain.projects.luc-leonard.fr \
						      --caproverPassword $CAPROVER_PASS \
						      --caproverApp sound-visualizer-worker \
						      --imageName kimsufi.luc-leonard.fr:5000/lucleonard/sound-visualizer-worker:latest'''
					}
				}
			}
		}
	}
}