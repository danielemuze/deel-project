pipeline {
    agent {
        label "jenkins-agent"
    }

    environment {
        APP_NAME = "deel-project"
        RELEASE = "1.0.0"
    }

    stages {
        stage("Cleanup Workspace") {
            steps {
                cleanWs()
            }
        }

        stage("Checkout from SCM") {
            steps {
                withCredentials([string(credentialsId: 'github-token', variable: 'GITHUB_TOKEN')]) {
                    git branch: 'main', credentialsId: 'github-token', url: 'https://github.com/danielemuze/deel-project.git'
                }
            }
        }

        stage("Build and Push Docker Image") {
            steps {
                script {
                    withCredentials([string(credentialsId: 'docker-username', variable: 'DOCKER_USER'), 
                                     string(credentialsId: 'docker-token', variable: 'DOCKER_PASS')]) {
                        def IMAGE_NAME = "${DOCKER_USER}/${APP_NAME}"
                        def IMAGE_TAG = "${RELEASE}-${BUILD_NUMBER}"

                        docker.withRegistry('', DOCKER_PASS) {
                            def docker_image = docker.build "${IMAGE_NAME}"
                            docker_image.push("${IMAGE_TAG}")
                            docker_image.push('latest')
                        }
                    }
                }
            }
        }
    }
}
