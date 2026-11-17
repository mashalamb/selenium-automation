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
                    docker run --name test-run-${BUILD_NUMBER} --shm-size=2g practice-login-tests:${BUILD_NUMBER}
                '''
            }
        }
    }

    post {
        always {
            sh 'docker cp test-run-${BUILD_NUMBER}:/app/reports/report.html reports/report.html || true'
            archiveArtifacts artifacts: 'reports/report.html', allowEmptyArchive: true
            sh 'docker rm -f test-run-${BUILD_NUMBER} || true'
            sh 'docker rmi -f practice-login-tests:${BUILD_NUMBER} || true'
        }
    }
}
