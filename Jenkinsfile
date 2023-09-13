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
        HELM_USER = "danielemuze"
        HELM_PASS = credentials('docker-token')
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
                    def PACKAGE_NAME = "${CHART_NAME}-${env.BRANCH_NAME}-${BUILD_NUMBER}.tgz"
                    def APP_VERSION = "1.${RELEASE}.${BUILD_NUMBER}"
                    def CHART_VERSION = "1.0.${BUILD_NUMBER}"

                    sh """
                    echo ${PACKAGE_NAME}
                    echo ${APP_VERSION}
                    echo ${CHART_VERSION}
                    """

                    // Bundle the Helm chart
                    withCredentials([string(credentialsId: 'helm-token', variable: 'HELM_PASS')]) {
                    sh """
                    echo ${PACKAGE_NAME}
                    echo ${APP_VERSION}
                    echo ${CHART_VERSION}
                    helm package deel-helm-chart --app-version=\${APP_VERSION} --version=\${CHART_VERSION} \${CHART_NAME} -d ./
                    docker login -u \${DOCKER_USER} -p \${HELM_PASS}
                    helm push \${PACKAGE_NAME} \${HELM_REGISTRY}/\${DOCKER_USER}
                    """
                    }
                }
            }
        }
    }

}