pipeline {
    agent any

    environment {
        PYTHON_PATH = 'C:\\Users\\Admin-BL\\AppData\\Local\\Programs\\Python\\Python312\\python.exe'
        PYTHON_SCRIPT_LOAD = 'scripts\\load_csv_to_gcp.py'
        PYTHON_SCRIPT_SUMMARY = 'scripts\\generate_summary.py'
        SUMMARY_FILE = 'upload_summary.txt'
        EMAIL_RECIPIENT = 'srikarvanaparthy@gmail.com'
    }

    stages {
        stage('Checkout Repository') {
            steps {
                git url: 'https://github.com/SrikarVanaparthy/Jenkins-usecase-2.git', branch: 'main'
            }
        }

        stage('Setup Python and Dependencies') {
            steps {
                bat """
                    "${env.PYTHON_PATH}" -m pip install --upgrade pip setuptools wheel
                    "${env.PYTHON_PATH}" -c "import pandas" || "${env.PYTHON_PATH}" -m pip install pandas
                    "${env.PYTHON_PATH}" -c "import pyodbc" || "${env.PYTHON_PATH}" -m pip install pyodbc
                """
            }
        }

        stage('Load CSV to GCP') {
            steps {
                bat """
                    "${env.PYTHON_PATH}" %PYTHON_SCRIPT_LOAD%
                """
            }
        }

        stage('Generate Summary Report') {
            steps {
                bat """
                    "${env.PYTHON_PATH}" %PYTHON_SCRIPT_SUMMARY%
                """
            }
        }

        stage('Send Email Notification') {
            steps {
                echo "Sending email notification for PR creation..."
                mail to: 'gogulanavateja1910@gmail.com',
                     subject: 'Pull Request Created: Test to Prod',
                     body: 'A pull request has been created to merge changes from the test branch to the prod branch.',
                     from: 'gogulateja92@gmail.com',
                     replyTo: 'gogulanavateja1910@gmail.com'
            }
        }
    }
}


