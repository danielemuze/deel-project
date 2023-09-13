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
        HELM_REGISTRY = "oci://registry-1.docker.io"
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
                    // Compute the PACKAGE_NAME dynamically based on Git branch and build number
                    def PACKAGE_NAME = "${CHART_NAME}-${env.BRANCH_NAME}-${BUILD_NUMBER}"
                    def APP_VERSION = sh(script: 'git describe --tags --always', returnStdout: true).trim()
                    def CHART_VERSION = "1.0.${BUILD_NUMBER}"

                    // Bundle the Helm chart
                    sh """
                    helm package deel-helm-chart --app-version=${APP_VERSION} --version=${CHART_VERSION}
                    echo ${DOCKER_PASS} | docker login -u ${DOCKER_USER} --password-stdin
                    helm push ${PACKAGE_NAME} ${HELM_REGISTRY}/${DOCKER_USER}
                    """
                }
            }
        }
    }

}