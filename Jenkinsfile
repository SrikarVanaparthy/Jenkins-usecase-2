pipeline {
    agent any

    environment {
        PYTHON_PATH = 'C:\\Users\\Admin-BL\\AppData\\Local\\Programs\\Python\\Python312\\python.exe'
        PYTHON_SCRIPT_LOAD = 'scripts\\load_csv_to_gcp.py'
        PYTHON_SCRIPT_SUMMARY = 'scripts\\generate_summary.py'
        SUMMARY_FILE = 'upload_summary.txt'
        EMAIL_RECIPIENT = 'srikarvanaparthy21@gmail.com'
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

        stage('Email Summary') {
            steps {
                script {
                    // Create a summary file using echo (simulate output)
                    bat """
                        echo Data has been successfully migrated to the SQL Server. > ${env.SUMMARY_FILE}
                        echo. >> ${env.SUMMARY_FILE}
                        echo Timestamp: %DATE% %TIME% >> ${env.SUMMARY_FILE}
                        echo Pipeline: ${env.JOB_NAME} >> ${env.SUMMARY_FILE}
                        echo Build Number: ${env.BUILD_NUMBER} >> ${env.SUMMARY_FILE}
                    """

                    // Read file content
                    def summaryContent = readFile(env.SUMMARY_FILE)

                    // Send the email
                    emailext (
                        subject: "✅ Data Migrated Successfully to SQL Server",
                        body: """\
Hello,

The data has been successfully migrated to the SQL Server.

Here is the summary:

${summaryContent}

Regards,
Jenkins Pipeline
""",
                        to: "${env.EMAIL_RECIPIENT}",
                        from: 'srikarvanaparthy@gmail.com'
                    )
                }
            }
        }
    }

    post {
        failure {
            emailext(
                to: "${env.EMAIL_RECIPIENT}",
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
