pipeline {
    agent any
    parameters {
        choice(name: 'BROWSER', choices: ['chrome', 'firefox', 'edge'], description: 'Browser to test')
        choice(name: 'MODULE', choices: ['tests', 'tests/module1_ecommerce', 'tests/module2_crossbrowser', 'tests/module3_datadriven'], description: 'Module to run')
    }
    stages {
        stage('Checkout') { steps { checkout scm } }
        stage('Install') {
            steps {
                sh 'python3 -m venv venv && . venv/bin/activate && pip install -r requirements.txt'
                sh '. venv/bin/activate && python testdata/make_excel_data.py'
            }
        }
        stage('Test') {
            steps {
                sh ". venv/bin/activate && pytest ${params.MODULE} --browser=${params.BROWSER} --headless --alluredir=reports/allure || true"
            }
        }
    }
    post {
        always {
            archiveArtifacts artifacts: 'reports/**', allowEmptyArchive: true
            publishHTML(target: [reportDir: 'reports', reportFiles: 'report.html', reportName: 'Test Report'])
        }
    }
}
