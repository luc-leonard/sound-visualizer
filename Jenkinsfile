pipeline {
    agent  docker { image 'python:3.9' }

    stages {
    stage('Lint') {
            steps {
                echo 'Linting...'
            }
        }
        stage('Build') {
            steps {
                echo 'Building..'
            }
        }
        stage('Test') {
            steps {
                echo 'Testing..'
            }
        }
        stage('Deploy') {
            steps {
                echo 'Deploying....'
            }
        }
    }
}
