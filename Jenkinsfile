pipeline {
    agent any

    environment {
        PYTHON_PATH = 'C:\\Users\\Admin-BL\\AppData\\Local\\Programs\\Python\\Python312\\python.exe'
        PYTHON_SCRIPT_LOAD = 'scripts\\load_csv_to_gcp.py'
        PYTHON_SCRIPT_SUMMARY = 'scripts\\generate_summary.py'
        SUMMARY_FILE = 'summary.doc'
        EMAIL_RECIPIENT = 'srikarvanaparthy21@gmail.com'
    }

    stages {
        stage('Checkout Repository') {
            steps {
                git url: 'https://github.com/SrikarVanaparthy/Jenkins-usecase-2.git', branch: 'main'
            }
        }

        stage('List Files') {
            steps {
                bat "dir" // Lists files in current workspace
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
                    "${env.PYTHON_PATH}" "${env.PYTHON_SCRIPT_LOAD}"
                """
            }
        }

        stage('Generate Summary Report') {
            steps {
                bat """
                    "${env.PYTHON_PATH}" "${env.PYTHON_SCRIPT_SUMMARY}"
                """
            }
        }


        stage('Email Summary') {
            steps {
                script {
                    def summaryContent = readFile(env.SUMMARY_FILE)
                    emailext (
                        subject: "✅ Data Migrated Successfully to SQL Server",
                        body: """\
Data has been successfully migrated to the SQL Server.

You can find the final migration report below:

${summaryContent}
""",
                        to: "srikarvanaparthy21@gmail.com",
                        from: 'srikarvanaparthy@gmail.com',
                        attachmentsPattern: 'summary.doc',
                        mimeType: 'application/msword'
                    )
                }
            }
        }
    }

    post {
        failure {
            emailext (
                to: "srikarvanaparthy21@gmail.com",
                from: 'srikarvanaparthy@gmail.com',
                subject: "❌ GCP Upload Pipeline FAILED",
                body: """\
The Jenkins job has failed.

Job: ${env.JOB_NAME}
Build Number: ${env.BUILD_NUMBER}
URL: ${env.BUILD_URL}
"""
            )
        }
    }
}