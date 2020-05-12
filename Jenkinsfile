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
//         stage('Test') {
//             agent {
//                 docker {
//                     image 'qnib/pytest'
//                 }
//             }
//             steps {
//                 sh 'py.test --junit-xml test-reports/results.xml sources2/test_calc.py'
//             }
//             post {
//                 always {
//                     junit 'test-reports/results.xml'
//                 }
//             }
//         }
        stage('Integration Test') {
            agent {
                docker {
                    image 'python:2-alpine'
                }
            }
            steps {
                sh '''
                    pip install localstack --user
                    pip install awscli
                    export SERVICES=s3
                    export AWS_ACCESS_KEY_ID=temp123456
                    export AWS_SECRET_ACCESS_KEY=temp123456
                    export PORT_WEB_UI=8080
                    export DATA_DIR=/tmp/localstack/data
                    export DEBUG=1
                    export AWS_DEFAULT_REGION=us-east-1
                    env
                    aws --version
                    localstack start
                    aws configure set default.s3.addressing_style path
                    aws --debug --endpoint-url=http://localhost:4566 s3api create-bucket --bucket testbucket --region us-west-1
                    aws --debug --endpoint-url=http://localhost:4566 s3 ls
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

