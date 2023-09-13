pipeline {
    agent {
        label "jenkins-agent"
    }

    environment {
        APP_NAME = "deel-container"
        CHART_NAME = "deel-helm-chart" 
        RELEASE = "1.0.0"
        DOCKER_USER = "danielemuze"
        DOCKER_PASS = 'docker-token'
        IMAGE_NAME = "${DOCKER_USER}/${APP_NAME}"
        IMAGE_TAG = "${RELEASE}-${BUILD_NUMBER}"
        HELM_EXPERIMENTAL_OCI = 1
    }

    stages {
        stage("Cleanup Workspace") {
            steps {
                cleanWs()
            }
        }

        stage("Checkout from SCM") {
            steps {
                git branch: 'main', credentialsId: 'github-token', url: 'https://github.com/danielemuze/deel-project.git'
            }
        }

        stage("Build and Push Docker Image") {
            steps {
                script {
                    docker.withRegistry('', DOCKER_PASS) {
                        docker_image = docker.build "${IMAGE_NAME}"
                    }

                    docker.withRegistry('', DOCKER_PASS) {
                        docker_image.push("${IMAGE_TAG}")
                        docker_image.push('latest')
                    }
                }
            }
        }

        stage("Bundle and Upload Helm Chart") {
            steps {
                script {
                    // Bundle the Helm chart
                    sh "helm package ${CHART_NAME} -d ./target"
                    // Log in to Docker Hub
                    sh "echo ${DOCKER_PASS} | helm registry login -u ${DOCKER_USER} --password-stdin"
                    // Push the Helm chart to Docker Hub as an OCI artifact
                    sh "helm chart save ./target/${CHART_NAME}-${RELEASE}.tgz ${DOCKER_USER}/${CHART_NAME}:${RELEASE}"
                    sh "helm chart push ${DOCKER_USER}/${CHART_NAME}:${RELEASE}"
                }
            }
        }
    }
}
