pipeline{
    agent{
        label "jenkins-agent"
    }

    environment {
        APP_NAME = "deel-project"
        RELEASE = "1.0.0"
        DOCKER_USER = "danielemuze"
        DOCKER_PASS = 'docker-token'
        IMAGE_NAME = "${DOCKER_USER}" + "/" + "${APP_NAME}"
        IMAGE_TAG = "${RELEASE}-${BUILD_NUMBER}"
    }

    stages{
    
        stage("Cleanup Workspace"){
            steps {
                cleanWs()
            }
          
        }

        stage("Checkout from SCM"){
            steps {
                git branch: 'main', credentialsId: 'github-token', url: 'https://github.com/danielemuze/deel-project.git'
            }
          
        }

        stage("Build and Push Docker Image"){
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
          
        
    }  
   
}