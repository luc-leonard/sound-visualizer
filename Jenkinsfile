pipeline {
	agent {docker {image 'python:3.9-buster'}}
    stages {
    stage('install deps') {
      steps {
      	sh 'pip install -r requirements.txt'
      }
    }
    stage('Lint') {
            steps {
                sh 'make format lint'
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
