# HR.AI Project

## Overview

HR.AI is a simple web application designed to streamline the hiring process for junior software engineering roles by using AI to evaluate candidate resumes and coding assessments.

## Features

- **Job Listing**: Candidates can view available job listings.
- **Resume Upload**: Candidates can apply by uploading their resumes.
- **Resume Screening**: The system checks resumes against basic requirements (e.g., GPA > 3.0, Python knowledge).
- **Coding Assessment**: Approved candidates proceed to answer coding questions.
- **AI Evaluation**: Submissions are evaluated using OpenAI models (GPT-4o and o1-mini).
- **Results Storage**: Passing candidates' information is stored in a database.
- **Developer and Employer Access**: Authorized users can access the candidate database.

## Installation

### Prerequisites

- Python 3.7 or higher
- An OpenAI API key with access to GPT-4o and o1-mini models

### Steps

1. **Clone the repository**:

   ```bash
   git clone https://github.com/yourusername/HRAI.git
   cd HRAI
2. Create and activate a virtual environment:


Copy code:
python -m venv venv
# On Windows
venv\Scripts\activate
# On Unix or MacOS
source venv/bin/activate

3. Install dependencies:

pip install -r requirements.txt

4. Set up environment variables:

Create a .env file in the root directory.

Add your OpenAI API key and a secret key:

OPENAI_API_KEY=your_openai_api_key_here
SECRET_KEY=your_secret_key_here

5. Initialize the database:

flask db init
flask db migrate -m "Initial migration."
flask db upgrade
6. Run the application:

flask run
Access the application at http://localhost:5000.

# Usage
Candidates:

Visit the homepage to view the job listing.
Click "Apply Now" to upload your resume.
If your resume meets the requirements, proceed to the coding assessment.
Submit your code solution for evaluation.
View the thank-you page upon completion.
Developers and Employers:

Access the candidate database at /admin (authentication not implemented in this version).
File Structure
app/: Contains the Flask application modules.
templates/: HTML templates for rendering views.
static/: Static files like CSS.
uploads/: Directory where uploaded resumes are stored.
main.py: Entry point of the application.
requirements.txt: Lists project dependencies.
config.py: Configuration settings.
.env: Environment variables (should not be committed to version control).
Technologies Used
Flask: Web framework.
Flask SQLAlchemy: Database ORM.
Flask Migrate: Database migrations.
OpenAI API: AI-powered code evaluation.
SQLite: Lightweight database for development purposes.
License
This project is for educational purposes.

yaml
Copy code

---

## **2. requirements.txt**

Flask>=2.0.3
Flask_SQLAlchemy>=2.5.1
Flask_Migrate>=3.1.0
python-dotenv>=0.21.0
openai>=1.0.0
PyPDF2>=1.26.0