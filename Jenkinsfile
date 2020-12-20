pipeline {
	agent {
	  docker {
	    image 'python:3.9-buster'
	    args '-V $HOME/.pip:/pip-cache'
	   }
	}

    stages {
    stage('install deps') {
      steps {
        sh 'pwd'
      	sh 'ls -l'
      	sh 'pip install --cache-dir /pip-cache -r requirements.txt'
      }
    }
    stage('Lint') {
            steps {
                sh 'make docker_lint'
            }
        }
        stage('Test') {
            steps {
                sh 'pytest'
            }
        }
        stage('build') {
            steps {
                sh 'make docker'
            }
        }
    }
}
