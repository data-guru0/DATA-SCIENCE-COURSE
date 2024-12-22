pipeline {
    agent any

    environment {
        VENV_DIR = 'venv'
        DOCKERHUB_CREDENTIAL_ID = 'mlops-dockerhub'
        DOCKERHUB_REGISTRY = 'https://registry.hub.docker.com'
        DOCKERHUB_REPOSITORY = 'dataguru97/prediction-mlops-app'
    }
    
    stages {
        stage('Cloning from Github Repo') {
            steps {
                script {
                    // Cloning Github repo
                    echo 'Cloning from Github Repo.........'
                    checkout scmGit(branches: [[name: '*/main']], extensions: [], userRemoteConfigs: [[credentialsId: 'mlops-github-token', url: 'https://github.com/data-guru0/MLOPS-PROJECT.git']])
                }
            }
        }

        stage('Setup Virtual Environment') {
            steps {
                script {
                    // Setup Virtual Environment
                    echo 'Setup Virtual Environment.........'
                    sh '''
                        python -m venv ${VENV_DIR}
                        . ${VENV_DIR}/bin/activate
                        pip install --upgrade pip
                        pip install -e .
                    '''
                    
                }
            }
        }

        stage('Linting Code') {
            steps {
                script {
                    // Linting Code
                    echo 'Linting Code.........'
                    sh '''
                        set -e
                        . ${VENV_DIR}/bin/activate
                        pylint application.py main.py --output=pylint-report.txt --exit-zero || echo "Pylint stage completed"
                        flake8 application.py main.py --ignore=E501,E302 --output-file=flake8-report.txt || echo "Flake8 stage completed"
                        black application.py main.py || echo "Black stage completed"
                    '''
                    
                }
            }
        }

        stage('Trivy Scanning') {
            steps {
                script {
                    // Trivy Scanning
                    echo 'Trivy Scanning.........'
                    sh "trivy fs ./ --format table -o trivy-fs-report.html"
                }
            }
        }

        stage('Building Docker Image') {
            steps {
                script {
                    // Building Docker Image
                    echo 'Building Docker Image........'
                    dockerImage = docker.build("${DOCKERHUB_REPOSITORY}:latest")
                }
            }
        }

        stage('Scanning Docker Image') {
            steps {
                script {
                    // Scanning Docker Image
                    echo 'Scanning Docker Image........'
                    sh "trivy image ${DOCKERHUB_REPOSITORY}:latest --format table -o trivy-image-scan-report.html"
                }
            }
        }

        stage('Pushing Docker Image') {
            steps {
                script {
                    // Pushing Docker Image
                    echo 'Pushing Docker Image........'
                    docker.withRegistry("${DOCKERHUB_REGISTRY}" , "${DOCKERHUB_CREDENTIAL_ID}"){
                        dockerImage.push('latest')
                    }
                }
            }
        }

        stage('AWS Deployment') {
            steps {
                script {
                    // AWS Deployment
                    echo 'AWS Deployment........'
                    sh "aws ecs update-service --cluster dataguru_ecs --service dataguru_service --force-new-deployment"
                }
            }
        }


    }
}