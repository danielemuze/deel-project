pipeline {
    agent {
        label "jenkins-agent"
    }

    environment {
        APP_NAME = "deel-container"
        CHART_NAME = "deel-devops-helm-chart" 
        RELEASE = "1.0.0"
        DOCKER_USER = "danielemuze"
        DOCKER_PASS = 'docker-token'
        KUBECONFIG_TOKEN = credentials('kubeconfig-token') 
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
                    def APP_VERSION = "1.${RELEASE}.${BUILD_NUMBER}"
                    def CHART_VERSION = "1.0.${BUILD_NUMBER}"
                    def PACKAGE_NAME = "${CHART_NAME}-${CHART_VERSION}.tgz"
                    def DEST_PATH = './packaged-charts' // Destination directory to store packaged charts

                    // Create destination directory only if it doesn't exist
                    sh """
                    if [ ! -d \"${DEST_PATH}\" ]; then
                    mkdir ${DEST_PATH}
                    fi
                    """

                    // Bundle the Helm chart
                    withCredentials([string(credentialsId: 'helm-token', variable: 'HELM_PASS')]) {
                        sh """
                        helm package ${CHART_NAME} --app-version=${APP_VERSION} --version=${CHART_VERSION} -d ${DEST_PATH}
                        docker login -u ${HELM_USER} -p ${HELM_PASS}
                        helm push ${DEST_PATH}/${PACKAGE_NAME} ${HELM_REGISTRY}/${HELM_USER}
                        """
                    }
                }
            }
        }

        stage("Deploy Helm Chart to Kubernetes") {
            steps {
                script {
                    def KUBECONFIG_PATH = "/home/jenkins/.kubeconfig" 
                    def NAMESPACE = "default" 
                    def RELEASE_NAME = "deel-devops" 
                    def CHART_VERSION = "1.0.${BUILD_NUMBER}"

                    // Deploy the Helm chart
                    withCredentials([string(credentialsId: 'kubeconfig-token', variable: 'KUBECONFIG_TOKEN')]) {
                        sh """
                        export KUBECONFIG=${KUBECONFIG_PATH}
                        helm install ${RELEASE_NAME} ${HELM_REGISTRY}/${HELM_USER}/${CHART_NAME} --version ${CHART_VERSION} \\
                        --namespace ${NAMESPACE}
                        """
                    }
                }
            }
        }
    }

}