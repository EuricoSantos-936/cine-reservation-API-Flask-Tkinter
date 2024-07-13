pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                git 'https://github.com/EuricoSantos-936/cine-reservation-API-Flask-Tkinter.git'
            }
        }

        stage('Build') {
            steps {
                sh 'echo "Building the project..."'
            }
        }

        stage('Test') {
            steps {
                sh 'python3 -m unittest discover'
            }
        }

        stage('Deploy') {
            steps {
                sh 'echo "Deploying the application..."'
            }
        }
    }
}
