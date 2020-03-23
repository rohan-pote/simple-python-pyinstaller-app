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
        stage('Checking out first') {
            agent {
                docker {
                    image 'qnib/pytest'
                }
            }
            steps {
                dir('sources') {
                    git(url: 'https://github.com/rohan-pote/simple-python-pyinstaller-app2.git', branch: 'master')
                }
            }
        }
        stage('Checkout Repo') {
            agent {
                docker {
                    image 'qnib/pytest'
                }
            }
            steps {
                sh 'mkdir -p sources'
                dir("sources")
                {
                    git branch: "master",
                    url: 'https://github.com/rohan-pote/simple-python-pyinstaller-app2.git'
                    sh 'py.test --junit-xml test-reports/results.xml sources/test_calc.py'
                }
            }
        }
        stage('Integration Test') {
            parallel {
                stage('Test Repo 1') {
                    agent {
                       docker {
                           image 'qnib/pytest'
                        }
                    }
                    steps {
                        sh 'mkdir -p sources'
                        dir("sources")
                        {
                            git branch: "master",
                            url: 'https://github.com/rohan-pote/simple-python-pyinstaller-app2.git'
                            sh 'py.test --junit-xml test-reports/results.xml sources/test_calc.py'
                        }
                    }
                }
                stage('Test repo 2') {
                    agent {
                       docker {
                           image 'qnib/pytest'
                        }
                    }
                    steps {
                       sh 'py.test --junit-xml test-reports/results.xml sources2/test_calc.py'
                    }
                }
                post {
                    always {
                        junit 'test-reports/results.xml'
                    }
                }
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
                    archiveArtifacts "${env.BUILD_ID}/sources/dist/add2vals"
                    sh "docker run --rm -v ${VOLUME} ${IMAGE} 'rm -rf build dist'"
                }
            }
        }
    }
}