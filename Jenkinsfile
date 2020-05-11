pipeline {
    agent any
    options {
        skipStagesAfterUnstable()
    }
    stages {
        stage('Build') {
            agent {
                docker {
                    image 'python:2-alpine'
                }
            }
            steps {
                sh 'python -m py_compile sources2/add2vals.py sources2/calc.py'
                stash(name: 'compiled-results', includes: 'sources2/*.py*')
            }
        }
        stage('Test') {
            agent {
                docker {
                    image 'qnib/pytest'
                }
            }
            steps {
                sh 'py.test --junit-xml test-reports/results.xml sources2/test_calc.py'
            }
            post {
                always {
                    junit 'test-reports/results.xml'
                }
            }
        }
        stage('Integration Test') {
            agent {
                docker {
                    image 'localstack/localstack:0.10.5'
                }
            }
            steps {
                sh '''
                    export SERVICES=s3
                    export AWS_ACCESS_KEY_ID=temp12345
                    export AWS_SECRET_ACCESS_KEY=temp12345
                    env
                    aws --version
                    aws '--endpoint-url=http://localhost:4572' s3 mb s3://mytestbucket
                    aws '--endpoint-url=http://localhost:4572' s3 ls
                '''
            }
        }
        stage('Deliver') {
            agent any
            environment {
                VOLUME = '$(pwd)/sources2:/src'
                IMAGE = 'cdrx/pyinstaller-linux:python2'
            }
            steps {
                dir(path: env.BUILD_ID) {
                    unstash(name: 'compiled-results')
                    sh "docker run --rm -v ${VOLUME} ${IMAGE} 'pyinstaller -F add2vals.py'"
                }
            }
            post {
                success {
                    archiveArtifacts "${env.BUILD_ID}/sources2/dist/add2vals"
                    sh "docker run --rm -v ${VOLUME} ${IMAGE} 'rm -rf build dist'"
                }
            }
        }
    }
}

