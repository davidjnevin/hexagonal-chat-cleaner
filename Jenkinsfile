pipeline {
  agent any
  stages {
    stage('Checkout Code') {
      steps {
        git(url: 'https://github.com/davidjnevin/hexagonal-chat-cleaner', branch: 'main')
      }
    }

    stage('list files') {
      parallel {
        stage('list files') {
          steps {
            sh 'ls -la'
          }
        }

        stage('backend unit test') {
          steps {
            sh 'make build && make test'
          }
        }

      }
    }

  }
}