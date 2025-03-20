pipeline {
    agent any
    

    environment {
        SCANNER_HOME= tool 'devops_backend'
    }

    stages {
        stage('git checkout') {
            steps {
                git branch: 'main', credentialsId: 'git-cred', url: 'https://github.com/anmol-c03/Devops_backend.git'
            }
        }

        stage('SonarQube Analysis') {
            steps {
                withSonarQubeEnv('devops_backend') {
                    sh '''
                        /var/lib/jenkins/tools/hudson.plugins.sonar.SonarRunnerInstallation/devops_backend/bin/sonar-scanner \
                        -Dsonar.projectKey=devops_backend \
                        -Dsonar.projectName="DevOps Backend" \
                        -Dsonar.sources=. \
                        -Dsonar.sourceEncoding=UTF-8
                    '''
                }
            }
        }
        
        stage('Build & Tag Docker Image') {
            steps {
               script {
                    withDockerRegistry(credentialsId: 'dockerhub-cred', toolName: 'docker') {
                            sh "docker build -t anizalmuseycai/backend:${BUILD_NUMBER} ."
                    }
               }
            }
        }
        
        stage('Docker Image Scan') {
            steps {
                sh "trivy image --format table -o trivy-image-report.html anizalmuseycai/backend:${BUILD_NUMBER} "
            }
        }
        
        stage('Push Docker Image') {
            steps {
               script {
                   withDockerRegistry(credentialsId: 'dockerhub-cred', toolName: 'docker') {
                            sh "docker push anizalmuseycai/backend:${BUILD_NUMBER}"
                    }
               }
            }
        }
        
        stage('run docker image') {
            steps {
                    sh """
                    # Ensure network exists
                    ssh azureuser@20.172.37.185 "docker network inspect my-network >/dev/null 2>&1 || docker network create my-network"
                    
                    # Check for and stop any existing backend container
                    ssh azureuser@20.172.37.185 "docker ps -q --filter name=backend | grep -q . && docker stop backend && docker rm backend|| echo 'No previous container found'"
                    
                    # Run the new container with a specific name
                    ssh azureuser@20.172.37.185 "docker run -d -p 80:80 --name backend --network my-network anizalmuseycai/backend:${BUILD_NUMBER}"
                """
            }
        }
    }
    post {
    always {
        script {
            def jobName = env.JOB_NAME
            def buildNumber = env.BUILD_NUMBER
            def pipelineStatus = currentBuild.result ?: 'UNKNOWN'
            def bannerColor = pipelineStatus.toUpperCase() == 'SUCCESS' ? 'green' : 'red'

            def body = """
                <html>
                <body>
                <div style="border: 4px solid ${bannerColor}; padding: 10px;">
                <h2>${jobName} - Build ${buildNumber}</h2>
                <div style="background-color: ${bannerColor}; padding: 10px;">
                <h3 style="color: white;">Pipeline Status: ${pipelineStatus.toUpperCase()}</h3>
                </div>
                <p>Check the <a href="${BUILD_URL}">console output</a>.</p>
                </div>
                </body>
                </html>
            """

            emailext (
                subject: "${jobName} - Build ${buildNumber} - ${pipelineStatus.toUpperCase()}",
                body: body,
                to: 'anmolchalise84@gmail.com',
                from: 'jenkins@example.com',
                replyTo: 'jenkins@example.com',
                mimeType: 'text/html',
                attachmentsPattern: 'trivy-image-report.html'
            )
        }
    }
}
    
}
