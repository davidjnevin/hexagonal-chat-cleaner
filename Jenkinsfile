node {
    def app

    stage('Clone repository') {
        /* Let's make sure we have the repository cloned to our workspace */

        git branch: 'portainer-build', url: 'https://github.com/davidjnevin/hexagonal-chat-cleaner'
    }

    stage('List files') {
        /* This builds the actual image; synonymous to
         * docker build on the command line */

        sh 'ls -lta'
    }

	stage('Build image') {
		sh 'make build'
	}

}
