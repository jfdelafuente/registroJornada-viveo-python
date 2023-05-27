pipeline {
	environment {
		registry = "jfdelafuente/viveorange"
		registryCredential = 'dockerhub_id'
		dockerImage = ''
	}
	agent none
	options {
		skipStagesAfterUnstable()
	}
	stages {
		stage('Build') {
			agent {
				docker {
					image 'python:3-alpine'
				}
			}
			steps {
				sh 'python -m py_compile src/bot.py src/ViveOrange.py src/configD.py src/utils.py'
				stash(name: 'compiled-results', includes: 'src/*.py*')
			}
		}
		stage('Test') {
			agent {
				docker {
					image 'qnib/pytest'
				}
			}
			steps {
				sh 'py.test --junit-xml test-reports/results.xml src/test_vive.py'
			}
			post {
				always {
					junit 'test-reports/results.xml'
				}
			}
		}
		stage('Deliver') {
            agent any
            environment {
                VOLUME = '$(pwd)/src:/src'
                IMAGE = 'cdrx/pyinstaller-linux:python3'
            }
            steps {
                dir(path: env.BUILD_ID) {
                    unstash(name: 'compiled-results')
                    sh "docker run --rm -v ${VOLUME} ${IMAGE} 'pyinstaller -F bot.py'"
                }
            }
            post {
                success {
                    archiveArtifacts "${env.BUILD_ID}/src/dist/add2vals"
                    sh "docker run --rm -v ${VOLUME} ${IMAGE} 'rm -rf build dist'"
                }
            }
        }
	}
}