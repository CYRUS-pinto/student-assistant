# Student Dashboard

## Overview
A comprehensive Flask-based student dashboard application for managing academic life. The dashboard features:
- Interactive timetable display (today's/tomorrow's classes)
- Academic calendar with special events
- Subject-wise file management with PDF viewing
- Deadline tracking system
- Python compiler interface
- Admin portal for content management
- Data visualization with charts (matplotlib)

## Project Architecture

### Technology Stack
- **Backend**: Flask 3.0.0 (Python web framework)
- **Frontend**: HTML with Tailwind CSS (via CDN)
- **Charts**: Matplotlib 3.8.2
- **Database**: JSON file-based storage (db.json)
- **Production Server**: Gunicorn 21.2.0

### File Structure
```
.
├── app.py                      # Main Flask application
├── db.json                     # Database for deadlines
├── requirements.txt            # Python dependencies
├── templates/                  # HTML templates
│   ├── index.html             # Homepage/dashboard
│   ├── admin_dashboard.html   # Admin interface
│   ├── admin_login.html       # Admin login page
│   ├── calendar.html          # Academic calendar
│   ├── compiler.html          # Python compiler
│   └── subject_page.html      # Subject file viewer
└── my_subject_files/          # Course materials organized by subject
    ├── Discrete Mathematics and Laplace Transforms/
    ├── Engineering Chemistry/
    ├── Environmental Studies/
    └── ... (other subjects)
```

### Key Features

#### 1. Dynamic Timetable
- Shows today's classes (before 5 PM) or tomorrow's classes (after 5 PM)
- Hardcoded schedule for Monday-Saturday
- Time slots with subject names

#### 2. File Management
- Subject-based organization
- PDF viewer integration
- Download functionality
- Admin file upload

#### 3. Deadline Tracker
- Add/delete deadlines via admin panel
- Live updates without page refresh
- Visual charts showing upcoming deadlines (30-day window)

#### 4. Data Visualization
- Pie chart: File distribution by subject
- Bar chart: Deadlines in next 30 days
- Dark mode optimized charts

#### 5. Admin Portal
- Password-protected access
- File upload to specific subjects
- Deadline management
- Session-based authentication

## Configuration

### Environment Variables
- `SECRET_KEY`: Flask session secret key (default: 'your_super_secret_key_12345')
- `ADMIN_PASSWORD`: Admin portal password (default: 'password1234')

### Development
The app runs on `0.0.0.0:5000` for Replit environment compatibility.

### Production Deployment
Configured with Gunicorn for autoscale deployment:
```
gunicorn --bind=0.0.0.0:5000 --reuse-port app:app
```

## API Endpoints

### Public Routes
- `/` - Homepage with dashboard
- `/subject/<subject_name>` - Subject page with files
- `/calendar` - Academic calendar
- `/compiler` - Python compiler interface
- `/view/<subject>/<filename>` - View file in browser
- `/download/<subject>/<filename>` - Download file
- `/api/get_deadlines` - Get deadlines as JSON

### Admin Routes
- `/admin_portal` - Admin login
- `/admin_dashboard` - Admin management panel
- `/admin/logout` - Logout
- `/admin/upload` - File upload (POST)
- `/admin/add_deadline` - Add deadline (POST)
- `/admin/delete_deadline/<id>` - Delete deadline

## Data Storage
Uses `db.json` for persistent storage of:
- Deadlines (id, title, date, details, completed status)
- Auto-incrementing deadline ID counter

## Recent Changes
- **2025-11-12**: Migrated to Replit environment
  - Added gunicorn for production deployment
  - Configured to run on 0.0.0.0:5000
  - Added environment variable support for SECRET_KEY and ADMIN_PASSWORD
  - Created .gitignore for Python project
  - Set up workflow for automatic restart

## User Preferences
None specified yet.

## Hardcoded Data
The application includes hardcoded:
- Course list (10 subjects)
- Weekly timetable (Monday-Saturday)
- Special dates/events for academic year 2025-2026

These can be modified directly in `app.py` if needed.
