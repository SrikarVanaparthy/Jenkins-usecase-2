pipeline {
    agent any

    environment {
        PYTHON_SCRIPT_LOAD = 'scripts\\load_csv_to_gcp.py'
        PYTHON_SCRIPT_SUMMARY = 'scripts\\generate_summary.py'
        SUMMARY_FILE = 'upload_summary.txt'

        // Replace with your Jenkins email settings or credentials
        EMAIL_RECIPIENT = 'srikarvanaparthy21@gmail.com'
    }


    stages {
        stage('Checkout Repository') {
            steps {
                // Update with your actual GitHub repo URL
                git url: 'https://github.com/SrikarVanaparthy/Jenkins-usecase-2.git', branch: 'main'
            }
        }

        stage('Setup Python and Dependencies') {
            steps {
                bat '''
                    python -m venv venv
                    call venv\\Scripts\\activate
                    python -m pip install --upgrade pip
                    python -m pip install pandas mysql-connector-python

                '''
            }
        }

        stage('Load CSV to GCP') {
            steps {
                bat '''
                    call venv\\Scripts\\activate
                    python %PYTHON_SCRIPT_LOAD%
                '''
            }
        }

        stage('Generate Summary Report') {
            steps {
                bat '''
                    call venv\\Scripts\\activate
                    python %PYTHON_SCRIPT_SUMMARY%
                '''
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
                    to: "${env.EMAIL_RECIPIENT}"
            )
        }
    }
}

    }

    post {
        failure {
            mail to: "${env.EMAIL_RECIPIENT}",
                 subject: "❌ GCP Upload Pipeline FAILED",
                 body: "Check Jenkins job: ${env.JOB_NAME} #${env.BUILD_NUMBER}\nURL: ${env.BUILD_URL}"
        }
    }
}
