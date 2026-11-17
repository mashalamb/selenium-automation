pipeline {
    agent any

    stages {
        stage('Build Test Container') {
            steps {
                sh 'docker build -t practice-login-tests:${BUILD_NUMBER} .'
            }
        }

        stage('Run Selenium Tests') {
            steps {
                sh '''
                    mkdir -p reports
                    docker run --rm --shm-size=2g \
                        -v "${WORKSPACE}/reports:/app/reports" \
                        practice-login-tests:${BUILD_NUMBER}
                '''
            }
        }
    }

    post {
        always {
            archiveArtifacts artifacts: 'reports/report.html', allowEmptyArchive: true
            sh 'docker rmi -f practice-login-tests:${BUILD_NUMBER} || true'
        }
    }
}
