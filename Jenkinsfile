
pipeline {
    agent any

    environment {
        IMAGE_NAME = 'tanvinewase/network-health-monitor'
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Test Python Files') {
            steps {
                sh '''
                    docker build -t network-health-monitor:test .
                    docker run --rm network-health-monitor:test \
                        python -m py_compile \
                        app.py monitor.py qos.py snmp_simulator.py
                '''
            }
        }

        stage('Build Docker Image') {
            steps {
                sh '''
                    docker build -t ${IMAGE_NAME}:${BUILD_NUMBER} .
                '''
            }
        }

        stage('Push to Docker Hub') {
            steps {
                withCredentials([
                    usernamePassword(
                        credentialsId: 'dockerhub-creds',
                        usernameVariable: 'DOCKERHUB_USER',
                        passwordVariable: 'DOCKERHUB_TOKEN'
                    )
                ]) {
                    sh '''
                        echo "$DOCKERHUB_TOKEN" | docker login \
                            --username "$DOCKERHUB_USER" \
                            --password-stdin

                        docker push ${IMAGE_NAME}:${BUILD_NUMBER}

                        docker logout
                    '''
                }
            }
        }
    }
}
