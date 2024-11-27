## 📄 README.md

# HR.AI

## 📖 Table of Contents

- [About](#about)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Admin Dashboard](#admin-dashboard)
- [Technologies Used](#technologies-used)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)
- [Changelog](#changelog)

## 🧐 About

HR.AI is an intelligent recruitment platform designed to streamline the hiring process by automating resume screening and coding assessments. Leveraging the power of OpenAI's GPT-4o/GPT-o1, HR.AI efficiently evaluates candidates based on predefined criteria, provides comprehensive feedback, and maintains structured records for both successful and unsuccessful applicants.

## 🚀 Features

- **Automated Resume Screening:** Utilizes AI to assess resumes against required criteria such as GPA and technical skills.
- **Coding Assessments:** Presents candidates with coding challenges and evaluates their submissions for correctness, efficiency, and code quality.
- **Admin Dashboard:** Provides a comprehensive interface for administrators to review, manage, and provide feedback on candidate applications.
  - **Separate Tables for Passed and Failed Candidates:** Organizes candidates into distinct categories for better clarity.
  - **Developer Feedback:** Allows administrators to add and edit feedback for all candidates.
- **Concise Evaluations:** Generates brief and constructive overall evaluations to enhance readability and usability.
- **Responsive Design:** Ensures the platform is accessible and user-friendly across various devices and screen sizes.
- **Secure File Handling:** Safely uploads and stores candidate resumes in PDF format.

## 🛠 Installation

### Prerequisites

- Python 3.7 or higher
- [pip](https://pip.pypa.io/en/stable/)
- [Git](https://git-scm.com/)
- [Virtualenv](https://virtualenv.pypa.io/en/latest/) (optional but recommended)

### Steps

1. **Clone the Repository**

   ```bash
   git clone https://github.com/AbdullahAbdelKhalek/HR.AI
   cd HR.AI
   ```

2. **Create a Virtual Environment**

   ```bash
   python -m venv venv
   ```

3. **Activate the Virtual Environment**

   - **Windows:**

     ```bash
     venv\Scripts\activate
     ```

   - **macOS/Linux:**

     ```bash
     source venv/bin/activate
     ```

4. **Install Dependencies**

   ```bash
   pip install -r requirements.txt
   ```

5. **Set Up Environment Variables**

   Create a `.env` file in the root directory and add the following:

   ```env
   FLASK_APP=run.py
   FLASK_ENV=development
   SECRET_KEY=your_secret_key
   OPENAI_API_KEY=your_openai_api_key
   UPLOAD_FOLDER=uploads
   ```

   - Replace `your_secret_key` with a secure secret key.
   - Replace `your_openai_api_key` with your OpenAI API key.

6. **Initialize the Database**

   ```bash
   flask db init
   flask db migrate -m "Initial migration."
   flask db upgrade
   ```

7. **Run the Application**

   ```bash
   flask run
   ```

   The application will be accessible at `http://127.0.0.1:5000/`.

## 🖥 Usage

### For Candidates

1. **Apply for a Position**

   - Navigate to the [Apply](http://127.0.0.1:5000/apply) page.
   - Upload your resume in PDF format.
   - If your resume meets the criteria, you'll be redirected to the coding assessment.

2. **Complete the Coding Assessment**

   - Answer the provided Python coding question.
   - Submit your code for evaluation.

3. **Receive Feedback**

   - Based on your performance, you'll receive feedback and an overall evaluation.

### For Administrators

1. **Access the Admin Dashboard**

   - Navigate to the [Admin Dashboard](http://127.0.0.1:5000/admin/candidates) page.
   - **Note:** Currently, the admin routes are accessible without authentication. It's recommended to implement authentication for security.

2. **Review Candidates**

   - **Passed Candidates:** View candidates who have met the requirements and completed the assessment.
   - **Failed Candidates:** View candidates who did not meet the initial screening criteria.

3. **Provide Developer Feedback**

   - Click on the "Edit Feedback" button next to a candidate to add or modify feedback.

## 🛡 Admin Dashboard

The Admin Dashboard provides two separate tables:

1. **Passed Candidates**

   | ID | Resume | Passed | Score | Date | Developer Feedback | Overall Evaluation | Questions Asked | Candidate Answers | Actions |
   |----|--------|--------|-------|------|--------------------|--------------------|-----------------|--------------------|---------|
   | 1  | [Download](#) | Yes    | 85    | 2024-11-18 | No comment         | [View](#)          | [View](#)        | [View](#)          | Edit Feedback |

2. **Failed Candidates**

   | ID | Resume | Passed | Score | Date | Developer Feedback | Overall Evaluation | Actions |
   |----|--------|--------|-------|------|--------------------|--------------------|---------|
   | 3  | [Download](#) | No     | 0     | 2024-11-18 | No comment         | "Candidate does not meet the GPA requirement." | Edit Feedback |

- **Truncated Text:** Long evaluations are truncated for readability. Hover over the text to view the full evaluation in a tooltip.

## 🧰 Technologies Used

- **Backend:**
  - [Flask](https://flask.palletsprojects.com/) - Web framework
  - [SQLAlchemy](https://www.sqlalchemy.org/) - ORM for database interactions
  - [OpenAI GPT-4](https://openai.com/) - AI for resume screening and code evaluation

- **Frontend:**
  - [Bootstrap 5](https://getbootstrap.com/) - CSS framework for responsive design
  - [Jinja2](https://jinja.palletsprojects.com/) - Templating engine

- **Others:**
  - [PyPDF2](https://pypi.org/project/PyPDF2/) - PDF parsing
  - [Flask-Migrate](https://flask-migrate.readthedocs.io/) - Database migrations
  - [dotenv](https://pypi.org/project/python-dotenv/) - Environment variable management

## 📜 License

**Important Note:**  
This project is currently in the process of being licensed. Until the licensing process is complete, all rights to this project, including its use, modification, and distribution, are reserved by the authors. For questions or permissions, please contact the repository owner.

## 📫 Contact

- **Abdullah Abdel-Khalek**
- **Email:** AbdullahHussamAK@gmail.com
- **GitHub:** [Abdullah Abdel-Khalek](https://github.com/AbdullahAbdelKhalek)

## 🗂 Changelog


# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.1.0] - 2024-11-18

### Added

- **Separate Tables for Passed and Failed Candidates:** Introduced distinct tables in the admin dashboard to organize candidates based on their screening results.
- **Developer Feedback for Failed Candidates:** Enabled administrators to add and edit feedback for candidates who did not meet the initial requirements.
- **Issues Field in Code Evaluation:** Modified the AI prompt to include an `"issues"` field, allowing for precise deductions based on identified code problems.

### Improved

- **Score Consistency:** Resolved discrepancies between the scores displayed in the terminal and those stored in the database by accurately applying deductions only when issues are present.
- **Overall Evaluation Length:** Limited the AI-generated overall evaluations to approximately 56 words or 375 characters for enhanced readability and usability.
- **Admin Dashboard Layout:** Enhanced the admin dashboard with improved table layouts and responsive design for better user experience.

### Fixed

- **Deduction Misapplication:** Fixed the `apply_grading_rubric` function to prevent incorrect deductions when feedback contains negations like "no syntax errors."
- **Truncated Evaluations:** Ensured that lengthy evaluations are properly truncated and that full evaluations are accessible via tooltips without stretching the table layout.

## [1.0.0] - 2024-11-17

### Added

- **Automated Resume Screening:** Implemented AI-driven resume evaluation based on GPA and Python knowledge.
- **Coding Assessment Feature:** Developed a coding challenge interface where candidates can submit Python functions for evaluation.
- **Admin Dashboard:** Created an admin interface to review candidates, download resumes, and provide feedback.
- **Overall Evaluation Generation:** Enabled AI-generated comprehensive evaluations combining resume and coding assessment results.

### Fixed

- **Initial Setup Issues:** Resolved various bugs related to file uploads and database interactions to ensure smooth operation.
