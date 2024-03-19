pipeline {
  agent any

  stages {
    stage('Clone repository') {
      steps {
        timeout(time: 30, unit: 'SECONDS') { // Set 2-minute timeout
          git branch: 'portainer-build', url: 'https://github.com/davidjnevin/hexagonal-chat-cleaner'
		  echo "clone repository successful"
		  sh 'ls -la'
        }
      }
    }
    stage('Start with a fresh docker environment') {
      steps {
        timeout(time: 30, unit: 'SECONDS') { // Set 2-minute timeout
          sh 'echo "A fresh start"'
		  sh 'echo "Checking environment variables"'
		  sh './startup.sh'
		  sh 'docker ps -aq | xargs -r docker stop'
          sh 'docker network prune -f'
		  sh 'docker container prune -f'
          sh 'docker network create backend'
        }
      }
    }
    stage('Build image') {
      steps {
        timeout(time: 2, unit: 'MINUTES') { // Set 2-minute timeout
          sh 'make build'
          echo "Build successful"
        }
      }
    }
    // stage('Make migrations') {
    //   steps {
    //     timeout(time: 2, unit: 'MINUTES') { // Set 2-minute timeout
    //       sh 'docker container ls'
    //       sh 'make migrations'
    //       sh 'make migrate'
		  // echo "migrations successful"
    //     }
    //   }
    // }
    stage('Run image') {
      steps {
        timeout(time: 30, unit: 'SECONDS') { // Set 2-minute timeout
          sh returnStdout: true, script: 'docker compose -f $DOCKER_COMPOSE_FILE up -d'
          echo "run successful"
        }
      }
    }
    stage('Test image') {
      steps {
        timeout(time: 30, unit: 'SECONDS') { // Set 2-minute timeout
          sh 'make test'
        }
      }
    }
    stage('clean up docker residuals') {
      steps {
        timeout(time: 30, unit: 'SECONDS') { // Set 2-minute timeout
          sh 'docker system prune --volumes'
        }
      }
    }
  }

  post {
    always {
      echo 'One way or another, I have finished'
          sh 'make down && make clean-volumes'
          // sh 'docker system prune -a -f'
		  sh 'docker container prune -f'
          sh 'docker network prune -f'
    }
    success {
      echo 'Pipeline succeeded!'
    }
    unstable {
      echo 'Pipeline is unstable :/'
    }
    failure {
      echo 'Pipeline failed :('
    }
    changed {
      echo 'Pipeline state changed'
    }
  }
}

