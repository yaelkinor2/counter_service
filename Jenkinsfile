pipeline {
    
    environment {
        counterServiceImage = 'counter-service'
    }
    
    agent any
    
    stages {
        
        stage('Prepare') {
            steps {
                // Cleaning workspace 
                cleanWs()
                
				script{
					// Job triggered automatically by git push to github repository
					if (params.BRANCH_NAME == null || params.BRANCH_NAME == '') {
						checkout scm
					}
					// Job triggered with BRANCH_NAME parameter 
					else {
						git branch: "${params.BRANCH_NAME}", url: "https://github.com/yaelkinor2/counter_service" 
					}
				}
            }
        }
  
        stage('Test') {
            steps {
				echo "Testing the application"
                sh "sudo python3 test.py"
            }
            post {
                always {junit skipPublishingChecks: true, testResults: 'test-reports/*.xml'}
            }
        }
  
        stage('Build'){
            steps {
				echo "Building the docker image"
                sh "sudo docker build -t ${counterServiceImage}:${BUILD_NUMBER} ."
            }
        }
    
        stage('Deploy')
        {
            steps {
				echo "Stopping and removing old container"
                sh "sudo docker stop counter-service && echo 'Container counter-service stopped' || echo 'Container counter-service does not exist'"
                sh "sudo docker rm -f counter-service && echo 'Container counter-service removed' || echo 'Container counter-service does not exist'"
            
                echo "Deploying and testing the new container"
				
				script {
					try {
						sh "sudo docker run -d -p 80:5000 --name counter-service '${counterServiceImage}:${BUILD_NUMBER}'"
						sh "sleep 5" 
						sh "curl --fail localhost/${counterServiceImage}"
						
					} catch (err) {
					
						echo err.getMessage()
						echo "Docker container deployment failed, deploying back the previous stable image."
						sh "sudo docker stop counter-service && echo 'Container counter-service stopped' || echo 'Container counter-service does not exist'"
						sh "sudo docker rm -f counter-service && echo 'Container counter-service removed' || echo 'Container counter-service does not exist'"
						sh "sudo docker run -d -p 80:5000 --name counter-service '${counterServiceImage}:latest'"
						sh "exit 1"
					}
				}
				
				// New docker container started and tested successfully so we tag the new images as latest
				sh "sudo docker tag ${counterServiceImage}:${BUILD_NUMBER} ${counterServiceImage}:latest"
            }
        }
    }
  
    post {
        always {
            echo "Pipeline completed"
        }
        success {                   
            echo "COUNTER-SERVICE APPLICATION IS UP AND RUNNING"
        }
        failure {
            echo "PIPELINE FAILED"
            error("Stopping...")
        }
    }
}