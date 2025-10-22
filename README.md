Hostel Management System
A full-stack web application built with Python (Flask) and MySQL to efficiently manage all aspects of a student hostel, from room allocation and fees to complaints and mess management.

✨ Features
This system provides a complete solution for both administrators and students:

Admin Dashboard: A central hub showing key statistics:

Total Students

Room Occupancy Percentage

Pending Complaints

Total Fees Collected

Student counts by block

Student Management: Secure registration, login, and profile management for students.

Room Management: View room details, status (occupied/vacant), and manage room allocation.

Fee Management: Track and manage student fee payments.

Complaint System: Students can submit complaints (e.g., Electrical, Plumbing), which admins can track and resolve.

Mess Management: Module for managing mess-related information and activities.

💻 Technology Stack
Backend: Python, Flask

Database: MySQL

Frontend: HTML, CSS, JavaScript (and likely Bootstrap)

Environment: python-dotenv for configuration management

Server: WSGI (Gunicorn recommended for production)

🚀 Setup and Installation
Follow these steps to get the project running on your local machine.

1. Prerequisites
Python 3.x

MySQL Server

Git (optional, for cloning)

2. Clone the Repository
Bash

git clone <your-repository-url>
cd HOSTEL_MANAGEMENT
3. Create and Activate a Virtual Environment
It's highly recommended to use a virtual environment.

On Windows:

Bash

python -m venv venv
.\venv\Scripts\activate
On macOS/Linux:

Bash

python3 -m venv venv
source venv/bin/activate
4. Install Dependencies
You should create a requirements.txt file with all your project's dependencies.

requirements.txt:

Flask
mysql-connector-python
python-dotenv
Then, install them:

Bash

pip install -r requirements.txt
5. Database Setup
Open your MySQL client (e.g., MySQL Workbench, terminal).

Create a new database for the project.

SQL

CREATE DATABASE hostel_db;
Import your database schema (your .sql file with CREATE TABLE ... statements) into this database.

6. Environment Variables
Create a file named .env in the root directory (HOSTEL_MANAGEMENT/.env). This file will hold your secret keys and database credentials.

.env:

# Flask Secret Key (change this to a random string)
SECRET_KEY=a-very-hard-to-guess-string

# Database Configuration
DB_HOST=localhost
DB_USER=your_mysql_username
DB_PASSWORD=your_mysql_password
DB_NAME=hostel_db
7. Run the Application
Once your environment is set up, you can run the app:

Bash

python run.py
The application will be running at http://127.0.0.1:5000.

📁 Project Structure
HOSTEL_MANAGEMENT/
├── .env                # Stores environment variables (MUST create)
├── run.py              # Main entry point to run the app
├── requirements.txt    # Project dependencies
├── app/
│   ├── __init__.py     # App factory (create_app)
│   ├── config.py       # Configuration class (Config)
│   │
│   ├── routes/         # All application blueprints
│   │   ├── __init__.py
│   │   ├── admin.py
│   │   ├── complaint.py
│   │   ├── fees.py
│   │   ├── login.py
│   │   ├── logout.py
│   │   ├── mees.py
│   │   ├── profile.py
│   │   ├── registration.py
│   │   ├── room.py
│   │   └── student.py
│   │
│   └── templates/      # All HTML files
│       ├── admin_panel.html
│       ├── login.html
│       ├── register.html
│       └── ... (etc.)
│
└── venv/                 # Virtual environment