pipeline {
    agent none 
    stages {
        stage('Build') { 
            agent {
                docker {
                    image 'python:3-alpine' 
                }
            }
            steps {
                sh 'python -m py_compile src/bot.py src/configD.py src/utils.py src/ViveOrange.py' 
                stash(name: 'compiled-results', includes: 'src/*.py*') 
            }
        }
    }
}