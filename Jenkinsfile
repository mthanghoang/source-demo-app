pipeline {
    agent any

    environment {
        DOCKER_USER = 'mthanghoang'             // Tên user Docker Hub
        DOCKER_PASSWORD = credentials('6bcfaa4d-ece4-42a2-bac2-563b7fffc5e2') // Credential id lưu password trên Jenkins
        CONFIG_REPO_URL = 'https://github.com/mthanghoang/demo-app.git'
        CONFIG_REPO_CRED = credentials('15aa9765-9bc0-4ded-96a1-4abdc11af4b0')    // Credential id để push repo config
    }

    stages {
        stage('Checkout source code') {
            steps {
                // Checkout source code của repo app
                git branch: 'main', url: 'https://github.com/mthanghoang/source-demo-app.git'
            }
        }

        stage('Build & Push Backend image') {
            steps {
                script {
                    // Login vào Docker Hub
                    sh "echo $DOCKER_PASSWORD | docker login -u $DOCKER_USER --password-stdin"
                    // Build image backend
                    sh "docker build -t $DOCKER_USER/demo-backend:${env.GIT_TAG_NAME} ./backend"
                    // Push image backend
                    sh "docker push $DOCKER_USER/demo-backend:${env.GIT_TAG_NAME}"
                }
            }
        }

        stage('Build & Push Frontend image') {
            steps {
                script {
                    sh "echo $DOCKER_PASSWORD | docker login -u $DOCKER_USER --password-stdin"
                    sh "docker build -t $DOCKER_USER/demo-frontend:${env.GIT_TAG_NAME} ./frontend"
                    sh "docker push $DOCKER_USER/demo-frontend:${env.GIT_TAG_NAME}"
                }
            }
        }

        stage('Update values in values.yaml in Config Repo') {
            steps {
                dir('my-app-config') {
                    // Checkout repo config
                    git branch: 'main', url: CONFIG_REPO_URL, credentialsId: CONFIG_REPO_CRED

                    // Sửa file values.yaml để update image tag
                    sh "sed -i 's/demo-backend:.*/demo-backend:${env.GIT_TAG_NAME}/' backend/values.yaml"
                    sh "sed -i 's/demo-frontend:.*/demo-frontend:${env.GIT_TAG_NAME}/' frontend/values.yaml"

                    // Commit & Push
                    // sh "git config user.name 'ci-bot' && git config user.email 'ci@example.com'"
                    sh "git add backend/values-prod.yaml"
                    sh "git add frontend/values-prod.yaml"
                    sh "git commit -m 'Update image tags to ${env.GIT_TAG_NAME}'"
                    sh "git push origin main"
                }
            }
        }
    }
}
