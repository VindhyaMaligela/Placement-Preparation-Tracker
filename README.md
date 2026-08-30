# Placement PrepTracker

Placement PrepTracker is a web-based tracking application designed to help students organize, monitor, and streamline their job application processes and preparation tasks in a single unified dashboard.

---

## Project Overview

Placement PrepTracker provides a centralized platform for students targeting internship and full-time job opportunities. It allows users to track their target companies, manage application statuses, and maintain preparation tasks (such as DSA practice, mock interviews, and resume reviews) linked directly to specific company applications.

---

## Problem Statement

During placement seasons, students apply to dozens of companies across multiple platforms. Tracking application status (Applied, Interviewing, Offered, etc.), key dates, and specific preparation actions required for each company is highly disorganized when managed across multiple spreadsheets, notes, and task managers. This lack of coordination leads to missed deadlines, inadequate preparation for specific interview rounds, and difficulty tracking overall progress.

---

## Objectives

*   **Centralize Job Application Tracking**: Maintain a persistent list of targeted companies, applied roles, status categories, and application dates.
*   **Manage Preparation Tasks**: Track study milestones, mock interviews, and tasks.
*   **Contextual Prep Linkage**: Link preparation tasks directly to specific company profiles to align preparation with application requirements.
*   **Analyze Progress Dynamically**: Provide a clean dashboard showing overall metrics, status distributions, and upcoming deadlines.
*   **Flexible Search & Filtering**: Allow quick search and filter operations by role name, company, category, and status.

---

## Key Features

*   **Dashboard Summary**: Clean 3-card metrics overview showcasing total companies tracked, tasks completion status (completed/total), and dynamic completion rate with a Bootstrap progress bar.
*   **Application Status Distribution**: Interactive distribution breakdown showing counts for each application phase (Interested, Applied, Interviewing, Offered, Rejected).
*   **Upcoming Tasks**: High-priority listing of upcoming incomplete tasks ordered by due dates.
*   **Recent Companies**: List of the 5 most recently added company applications.
*   **Quick Actions**: Shortcuts to add companies, add tasks, view companies list, or view tasks list.
*   **Company CRUD**: Create, read, update, and delete company applications.
*   **Company Profile View**: Specific details page for each company showing role details, notes, and a linked list of preparation tasks.
*   **Tasks CRUD**: Create, read, update, and delete tasks with attributes for title, description, category, due date, and status.
*   **Interactive Search & Filters**:
    *   **Companies Page**: Filter by case-insensitive name/role search terms, status category dropdowns, or both combined instantly.
    *   **Tasks Page**: Filter by title search, category dropdown, or status dropdown.

---

## Technology Stack

*   **Backend Framework**: Python, Flask (with WTForms for input validation and SQLAlchemy ORM for database queries)
*   **Database**: SQLite (SQLAlchemy ORM)
*   **Frontend**: HTML5, CSS3, Bootstrap 5 (Icons & UI templates), JavaScript (native client-side form submissions)
*   **Testing**: pytest

---

## Project Structure

```text
Placement-Preparation-Tracker/
│
├── app/                        # Application package
│   ├── __init__.py             # Flask app factory, extension setup, and blueprint routing
│   ├── forms.py                # WTForms validation schemas (CompanyForm, TaskForm)
│   ├── models.py               # Database schemas (Company, Task)
│   │
│   ├── routes/                 # Request routing blueprints
│   │   ├── companies.py        # Company listing, search/filter, detail, and CRUD routes
│   │   ├── dashboard.py        # Primary dashboard metrics page route
│   │   └── tasks.py            # Task listing, search/filter, completion toggle, and CRUD routes
│   │
│   ├── services/               # Core backend services
│   │   └── statistics.py       # Helper logic calculating counts, progress percentages, and list ordering
│   │
│   ├── static/                 # Static styling assets
│   │   └── css/style.css       # Custom stylesheet overrides
│   │
│   └── templates/              # HTML layout view templates
│       ├── base.html           # Main navbar, footer, and styling framework structure
│       ├── companies/          # Company index list view, detail layout, and forms
│       ├── dashboard/          # Redesigned main workspace dashboard view
│       └── tasks/              # Task list view, creation/editing templates
│
├── tests/                      # Automated test suite
│   ├── conftest.py             # Configuration for Flask test client fixtures
│   ├── test_companies.py       # Unit tests verifying Company CRUD operations
│   ├── test_company_detail.py  # Unit tests verifying details page and linked tasks
│   ├── test_dashboard.py       # Unit tests verifying dashboard metrics calculations and sorting
│   ├── test_search_filter.py   # Unit tests verifying search, status, and combined filters
│   ├── test_tasks.py           # Unit tests verifying Task CRUD and completion toggles
│   └── verify_crud.py          # Script executing end-to-end CRUD integration checks
│
├── config.py                   # Configuration setups for development and testing environments
├── requirements.txt            # Python environment packages listing
└── run.py                      # Startup script initiating Flask server (with debug mode enabled)
```

---

## Database

Persistence is handled by a local SQLite database (stored as `instance/placement_tracker.db` during runtime). The schema consists of two related tables:

1.  **`companies` (Company model)**:
    *   `id` (Integer, Primary Key)
    *   `name` (String, required): Name of targeted company.
    *   `role` (String, required): Target job profile (e.g. SDE Intern, Product Manager).
    *   `status` (String, default 'Interested'): Application phase (Interested, Applied, Interviewing, Offered, Rejected).
    *   `application_date` (Date): Date of application.
    *   `notes` (Text): Custom interview summaries, contacts, or context.
    *   `tasks` (Relationship): One-to-many relationship linking tasks to the company.

2.  **`tasks` (Task model)**:
    *   `id` (Integer, Primary Key)
    *   `title` (String, required): Preparation milestone summary.
    *   `description` (Text): Specific preparation details.
    *   `category` (String, default 'Other'): Study areas (DSA, Aptitude, Resume, Interview, Other).
    *   `due_date` (Date): Target completion deadline.
    *   `status` (String, default 'Pending'): Task status (Pending, In Progress, Completed).
    *   `completed` (Boolean, default False): Quick complete binary flag.
    *   `company_id` (Integer, Foreign Key): Links task to a parent company (optional).

---

## Testing

The project contains a comprehensive test suite covering routes, form submissions, and database-level filter operations.

Run the test suite:
```powershell
python -m pytest
```

---

## Installation and Setup

### 1. Prerequisites
Ensure you have Python 3.8+ installed on your system.

### 2. Set Up Virtual Environment
Clone the repository, navigate to the project directory, and create a virtual environment:

```powershell
# Create virtual environment
python -m venv venv

# Activate virtual environment (Windows)
.\venv\Scripts\activate
```

### 3. Install Dependencies
Install all required libraries listed in `requirements.txt`:
```powershell
pip install -r requirements.txt
```

### 4. Run the Application
Start the Flask application server:
```powershell
python run.py
```
The server will start locally on: [http://127.0.0.1:5000/](http://127.0.0.1:5000/)

---

## Usage

1.  **Access the Dashboard**: Open [http://127.0.0.1:5000/](http://127.0.0.1:5000/) to view your preparation statistics, upcoming deadlines, status distribution, and quick action options.
2.  **Add a Company**: Click "Add Company", fill in the company name, target role, application date, status, and any initial notes.
3.  **Create Preparation Tasks**: Click "Add Task", set the title, choose a category (e.g., DSA), link it to a specific company if appropriate, set a deadline, and save.
4.  **Explore Details**: Click on any company name from the dashboard or companies table to open the company details view, displaying its target milestones and associated preparation actions.
5.  **Search & Filter**: Filter your applications by name/role or status on the Companies page. Tweak tasks based on category or status on the Tasks page to stay focused.

---

## Future Enhancements

*   **Calendar Sync Integration**: Sync task due dates to external calendar accounts (such as Google Calendar or Outlook).
*   **Automatic Interview Prep Recommendations**: Auto-populate recommended mock tasks or preparation material checklists depending on the target company (e.g. recommend system design for specific SDE profiles).
*   **Email Reminders**: Set automated email notifications warning students of approaching task deadlines or application follow-up dates.

---

## Academic Project

This application has been developed as an academic project focused on engineering clean web architectures, modular routing structures, database integrations, and automated unit testing models.
