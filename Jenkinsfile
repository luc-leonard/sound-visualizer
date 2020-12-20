pipeline {
	agent {docker {image 'python-3.9'}}
    stages {
    stage('install deps') {
      steps {
      	pip install -r requirements.txt
      }
    }
    stage('Lint') {
            steps {
                poetry run make format lint
            }
        }
        stage('Test') {
            steps {
                poetry run pytest
            }
        }
        stage('build') {
            steps {
                make docker
            }
        }
    }
}
