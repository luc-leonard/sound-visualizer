pipeline {
	agent any
    stages {
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
