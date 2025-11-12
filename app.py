from flask import Flask, render_template, request, redirect, url_for, send_from_directory, session, flash, jsonify
import datetime
import json
import os
import secrets

# --- Matplotlib Imports (Unit-IV) ---
import matplotlib
import matplotlib.pyplot as plt
import io  
import base64 
matplotlib.use('Agg')

app = Flask(__name__)

# --- Secret key for session management ---

SECRET_KEY = os.environ.get('SECRET_KEY')
if not SECRET_KEY:
    print("WARNING: SECRET_KEY not set. Using generated key for development only.")
    SECRET_KEY = secrets.token_hex(32)
app.config['SECRET_KEY'] = SECRET_KEY

ADMIN_PASSWORD = os.environ.get('ADMIN_PASSWORD', 'admin123')
if ADMIN_PASSWORD == 'admin123':
    print("WARNING: ADMIN_PASSWORD not set. Using default 'admin123' - change this in production!")

# --- Configuration ---
DB_FILE = 'db.json'
UPLOAD_FOLDER = 'my_subject_files'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# --- YOUR HARDCODED COURSE DATA (from final.pdf) ---
COURSE_LIST = [
    "Discrete Mathematics and Laplace Transforms",
    "Engineering Chemistry",
    "Fundamentals of Digital Electronics",
    "Problem solving using Python",
    "Fundamentals of Embedded Systems",
    "Innovation & Design Thinking",
    "Environmental Studies",
    "Technical English",
    "Engineering Chemistry Lab",
    "Web Technology Lab"
]

# --- YOUR HARDCODED TIMETABLE (from final.pdf) ---
TIMETABLE = {
    "Monday": [
        {"time": "9:00 - 10:40", "subject": "DE LAB B1 / PY LAB B2"},
        {"time": "10:55 - 11:45", "subject": "Engineering Chemistry"},
        {"time": "11:45 - 12:35", "subject": "Innovation & Design Thinking"},
        {"time": "1:30 - 3:15", "subject": "Problem solving using Python (Lab)"},
        {"time": "3:20 - 4:10", "subject": "Engineering Chemistry"},
    ],
    "Tuesday": [
        {"time": "9:00 - 9:50", "subject": "Fundamentals of Digital Electronics"},
        {"time": "9:50 - 10:40", "subject": "Engineering Chemistry"},
        {"time": "10:55 - 11:45", "subject": "Discrete Mathematics and Laplace Transforms"},
        {"time": "1:30 - 3:15", "subject": "CHY LAB B1 / PY LAB B2"},
        {"time": "3:20 - 4:10", "subject": "Problem solving using Python"},
    ],
    "Wednesday": [
        {"time": "9:00 - 9:50", "subject": "Technical English"},
        {"time": "9:50 - 10:40", "subject": "Problem solving using Python"},
        {"time": "10:55 - 11:45", "subject": "Discrete Mathematics and Laplace Transforms"},
        {"time": "11:45 - 12:35", "subject": "Engineering Chemistry"},
        {"time": "1:30 - 2:20", "subject": "Innovation & Design Thinking"},
        {"time": "2:25 - 3:15", "subject": "Fundamentals of Digital Electronics"},
        {"time": "3:20 - 4:10", "subject": "Fundamentals of Embedded Systems"},
    ],
    "Thursday": [
        {"time": "9:00 - 9:50", "subject": "Fundamentals of Digital Electronics"},
        {"time": "9:50 - 10:40", "subject": "Problem solving using Python"},
        {"time": "10:55 - 11:45", "subject": "Fundamentals of Embedded Systems"},
        {"time": "11:45 - 12:35", "subject": "Engineering Chemistry"},
        {"time": "1:30 - 2:20", "subject": "Environmental Studies"},
        {"time": "2:25 - 3:15", "subject": "Engineering Chemistry"},
        {"time": "3:20 - 4:10", "subject": "Discrete Mathematics and Laplace Transforms"},
        {"time": "4:10 - 5:00", "subject": "Discrete Mathematics and Laplace Transforms"},
    ],
    "Friday": [
        {"time": "9:00 - 9:50", "subject": "Fundamentals of Digital Electronics"},
        {"time": "9:50 - 10:40", "subject": "Discrete Mathematics and Laplace Transforms"},
        {"time": "10:55 - 12:35", "subject": "DE LAB B2 / PY LAB B1"},
        {"time": "1:30 - 3:15", "subject": "CHY LAB B2 / PY LAB B1"},
        {"time": "3:20 - 4:10", "subject": "Problem solving using Python"},
    ],
    "Saturday": [
        {"time": "9:00 - 10:40", "subject": "Web Technology Lab"},
        {"time": "10:55 - 11:45", "subject": "Engineering Chemistry"},
        {"time": "11:45 - 12:35", "subject": "Discrete Mathematics and Laplace Transforms"},
    ],
    "Sunday": []
}

# --- SPECIAL DATES (from your uploaded calendar images) ---
SPECIAL_DATES = {
    "2025-11-01": "Kannada Rajyotsava (H)",
    "2025-11-04": "Second Internal Assessment Test (SOE)",
    "2025-11-05": "Second Internal Assessment Test (SOE)",
    "2025-11-06": "Second Internal Assessment Test (SOE)",
    "2025-11-07": "Second Internal Assessment Test (SOE)",
    "2025-11-08": "Kanakadasa Jayanthi (H)",
    "2025-11-10": "Continuous Internal assessment-2 (SOL)",
    "2025-11-13": "Internal Practical Examination (SOE)",
    "2025-11-14": "Childrens Day / Internal Practical Exam (SOE)",
    "2025-11-15": "Internal Practical Examination (SOE)",
    "2025-11-20": "Retest for eligible students (SOL)",
    "2025-11-24": "Last date for submitting assignment (SOL)",
    "2025-11-25": "Presentation of the assignment (SOL)",
    "2025-11-26": "Constitution Day",
    "2025-11-28": "Last Working Day (SOE)",
    "2025-11-29": "Last day of classes (SOL)",
    "2025-12-05": "Final Practical Exam (SOE)",
    "2025-12-06": "Final Practical Exam (SOE)",
    "2025-12-08": "Commencement of Final End Sem Exam",
    "2025-12-15": "Commencement of evaluation",
    "2025-12-25": "Christmas (H)",
    "2025-12-27": "Christmas Vacation",
    "2025-12-28": "Christmas Vacation",
    "2025-12-29": "Christmas Vacation",
    "2025-12-30": "Christmas Vacation",
    "2025-12-31": "Christmas Vacation",
    "2026-01-01": "New Year (H)",
    "2026-01-05": "Re-opening of Second Semester",
    "2026-01-12": "Foundation Day / Alumni Gathering / Last date for assignment topic (SOL)",
    "2026-01-14": "Makara Sankranthi (H)",
    "2026-01-15": "Declaration of Results (SOL)",
    "2026-01-19": "Cultural Day",
    "2026-01-26": "Republic Day (H)",
    "2026-01-31": "Joy of Giving Day (SOE)",
    "2026-02-02": "Last date for synopsis presentation (SOL)",
    "2026-02-15": "Maha Shivaratri (H)",
    "2026-02-18": "Ash Wednesday",
    "2026-02-21": "Sports Day",
    "2026-02-23": "Continuous Internal Assessment-1 (SOL)",
    "2026-02-25": "First Internal Assessment Test (SOE)",
    "2026-02-26": "First Internal Assessment Test (SOE)",
    "2026-02-27": "First Internal Assessment Test (SOE)",
    "2026-02-28": "National Science Day",
    "2026-03-03": "Retest for eligible students (SOL)",
    "2026-03-08": "Womens Day",
    "2026-03-13": "Annual Day",
    "2026-03-14": "Parents Meet (SOE)",
    "2026-03-20": "Ugadi (H)",
    "2026-03-21": "Idul-Fitr (H)",
    "2026-03-31": "Mahavir Jayanthi (H)",
    "2026-04-03": "Good Friday (H)",
    "2026-04-04": "Continuous Internal Assessment-2 (SOL)",
    "2026-04-05": "Easter Sunday (H)",
    "2026-04-06": "Continues Internal Assessment-2 (SOL)",
    "2026-04-09": "Second Internal Assessment Test (SOE)",
    "2026-04-10": "Second Internal Assessment Test (SOE)",
    "2026-04-11": "Second Internal Assessment Test (SOE)",
    "2026-04-14": "Ambedkar Jayanthi (H)",
    "2026-04-15": "Retest for eligible students (SOL)",
    "2026-04-25": "Internal Practical Exam (SOE)",
    "2026-04-26": "Internal Practical Exam (SOE)",
    "2026-04-27": "Last date for assignments (SOL) / Internal Practical Exam (SOE)",
    "2026-04-28": "Presentation of the assignments (SOL)",
    "2026-04-30": "Last Working Day (SOE)",
    "2026-05-01": "May Day (H)",
    "2026-05-08": "Final Practical Exam (SOE)",
    "2026-05-09": "Final Practical Exam (SOE)",
    "2026-05-11": "Commencement of end Semester examination (SOL)",
    "2026-05-15": "Commencement of end Semester Exam",
    "2CSS-05-18": "Commencement of evaluation",
    "2026-05-27": "Bakrid (H)",
    "2026-05-30": "End of second Semester Examination (SOE)",
    "2026-06-21": "Feast of St Aloysius Gonzaga / International Day of Yoga"
}


# --- Database Variables ---
deadlines = []
deadline_id_counter = 1

# --- Database Functions ---
def load_data():
    """Loads deadlines from db.json."""
    global deadlines, deadline_id_counter
    try:
        with open(DB_FILE, 'r') as f:
            data = json.load(f)
            deadlines = data.get('deadlines', [])
            deadline_id_counter = data.get('deadline_id_counter', 1)
            # --- NEW: Ensure all deadlines have a 'details' key ---
            for d in deadlines:
                if 'details' not in d:
                    d['details'] = '' # Add empty string if 'details' is missing
    except (FileNotFoundError, json.JSONDecodeError):
        print("db.json not found. Starting with a fresh database.")
        deadlines = []
        deadline_id_counter = 1

def save_data():
    """Saves deadlines to db.json."""
    with open(DB_FILE, 'w') as f:
        data_to_save = {
            'deadlines': deadlines,
            'deadline_id_counter': deadline_id_counter
        }
        json.dump(data_to_save, f, indent=4)

# --- Helper Function: Get files for stats ---
def get_files_by_folder():
    """ Scans the UPLOAD_FOLDER and returns a dict of {subject: file_count} """
    file_map = {}
    root_dir = app.config['UPLOAD_FOLDER']
    
    # Ensure root_dir exists
    if not os.path.exists(root_dir):
        return file_map

    for subject in COURSE_LIST:
        subject_path = os.path.join(root_dir, subject)
        if not os.path.exists(subject_path) or not os.path.isdir(subject_path):
            file_map[subject] = 0
            continue
        
        try:
            files = [f for f in os.listdir(subject_path) if os.path.isfile(os.path.join(subject_path, f)) and not f.startswith('.')]
            file_map[subject] = len(files)
        except OSError:
            file_map[subject] = 0
            
    return file_map

# --- Chart Generation (Unit-IV) ---
def create_pie_chart(file_data):
    """Generates a pie chart of files per subject."""
    # This is the background color of the chart's card
    fc_color_face = '#1f2937' # This is the dark gray (gray-800)
    
    # Filter out subjects with 0 files to make the chart cleaner
    labels = [subject for subject, count in file_data.items() if count > 0]
    sizes = [count for count in file_data.values() if count > 0]

    if not labels:
        return None # Don't create a chart if there's no data

    fig, ax = plt.subplots(figsize=(6, 6))
    
    # --- Custom colors for dark mode ---
    colors = plt.cm.Paired(range(len(labels)))
    textprops = {"color": "w", "weight": "bold"} # White text

    ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90, colors=colors, textprops=textprops, pctdistance=0.85)
    
    # Draw a circle to make it a donut chart
    centre_circle = plt.Circle((0,0),0.70,fc=fc_color_face) # --- This line is fixed ---
    fig.gca().add_artist(centre_circle)
    
    ax.axis('equal')  # Equal aspect ratio
    
    # --- Make background transparent ---
    fig.patch.set_alpha(0)
    ax.patch.set_alpha(0)
    
    # Save to a in-memory buffer
    buf = io.BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight')
    plt.close(fig)
    return base64.b64encode(buf.getvalue()).decode('utf-8')

def create_bar_chart(deadlines_data):
    """Generates a bar chart of deadlines in the next 30 days."""
    today = datetime.date.today()
    thirty_days_from_now = today + datetime.timedelta(days=30)
    
    # Filter for deadlines in the next 30 days
    upcoming_deadlines_30 = [
        d for d in deadlines_data 
        if d.get('date') and # check if date exists
           datetime.date.fromisoformat(d['date']) >= today and 
           datetime.date.fromisoformat(d['date']) <= thirty_days_from_now
    ]
    
    if not upcoming_deadlines_30:
        return None

    # Group by date
    deadlines_by_date = {}
    for d in upcoming_deadlines_30:
        day = d['date']
        deadlines_by_date[day] = deadlines_by_date.get(day, 0) + 1
        
    labels = sorted(deadlines_by_date.keys())
    counts = [deadlines_by_date[label] for label in labels]
    
    # Extract just the month and day for a cleaner label (e.g., "Nov 11")
    day_labels = [datetime.date.fromisoformat(label).strftime('%b %d') for label in labels]

    fig, ax = plt.subplots(figsize=(8, 4))
    
    # --- Custom colors for dark mode ---
    ax.bar(day_labels, counts, color='#3b82f6') # Blue bars
    
    # --- White/Light text and labels ---
    ax.set_title('Deadlines in the Next 30 Days', color='w', weight='bold') # <-- New Title
    ax.set_ylabel('Total Events', color='w')
    ax.set_xlabel('Date', color='w')
    ax.tick_params(colors='w', rotation=45, labelsize=8) # Rotate labels if they overlap
    
    # --- Transparent background ---
    fig.patch.set_alpha(0)
    ax.patch.set_alpha(0)
    
    # --- Make grid lines subtle ---
    ax.yaxis.grid(True, linestyle='--', alpha=0.3)
    
    plt.tight_layout() # Add this to prevent labels from being cut off
    
    # Save to buffer
    buf = io.BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight')
    plt.close(fig)
    return base64.b64encode(buf.getvalue()).decode('utf-8')


# --- (Shared Function) Get sidebar data ---
def get_sidebar_data():
    return {
        "all_subjects": COURSE_LIST
    }

# --- CONSUMER ROUTES ---

@app.route('/')
def homepage():
    now = datetime.datetime.now()
    
    # Logic for "Today's" or "Tomorrow's" classes
    if now.hour < 17: # If before 5:00 PM
        target_day = now
        day_name = now.strftime('%A')
        day_title = "Today's Classes"
    else: # 5:00 PM or later
        target_day = now + datetime.timedelta(days=1)
        day_name = target_day.strftime('%A')
        day_title = "Tomorrow's Classes"
        
    target_classes = TIMETABLE.get(day_name, [])
    
    load_data() # Ensure we have the latest data
    upcoming_deadlines = sorted(
        [d for d in deadlines if not d.get('completed', False)], 
        key=lambda x: x['date']
    )
    
    # --- Generate Charts ---
    file_stats = get_files_by_folder()
    pie_chart_img = create_pie_chart(file_stats)
    bar_chart_img = create_bar_chart(upcoming_deadlines)
    
    return render_template('index.html', 
                           day_title=day_title,
                           target_day_name=day_name,
                           target_classes=target_classes,
                           upcoming_deadlines=upcoming_deadlines,
                           pie_chart=pie_chart_img,
                           bar_chart=bar_chart_img,
                           file_stats=file_stats, 
                           **get_sidebar_data())

@app.route('/subject/<subject_name>')
def subject_page(subject_name):
    if subject_name not in COURSE_LIST:
        return "Subject not found", 404

    subject_path = os.path.join(app.config['UPLOAD_FOLDER'], subject_name)
    subject_files = []
    
    if os.path.exists(subject_path):
        try:
            # Get all files, ignore dotfiles (like .DS_Store)
            subject_files = [f for f in os.listdir(subject_path) if os.path.isfile(os.path.join(subject_path, f)) and not f.startswith('.')]
        except OSError:
            pass # Folder might be inaccessible

    return render_template('subject_page.html', 
                           subject_name=subject_name,
                           subject_files=subject_files,
                           **get_sidebar_data())

@app.route('/calendar')
def calendar_page():
    # Convert dict to list for easier JS parsing
    events_list = [{"date": date, "title": title} for date, title in SPECIAL_DATES.items()]
    
    return render_template('calendar.html',
                           special_events_json=json.dumps(events_list),
                           **get_sidebar_data())

# --- NEW: COMPILER ROUTE ---
@app.route('/compiler')
def compiler_page():
    """
    Renders the new compiler page.
    """
    return render_template('compiler.html', **get_sidebar_data())


# --- NEW ROUTE FOR LIVE DEADLINES ---
@app.route('/api/get_deadlines')
def api_get_deadlines():
    """
    This is a new API route. It doesn't return a full HTML page,
    just the raw deadline data as JSON. This allows our homepage
    to fetch updates without a full refresh.
    """
    load_data() # Get the freshest data from db.json
    upcoming = sorted(
        [d for d in deadlines if not d.get('completed', False)], 
        key=lambda x: x['date']
    )
    # --- NEW: Return the 'details' field as well ---
    return jsonify(deadlines=[{"id": d["id"], "title": d["title"], "date": d["date"], "details": d.get("details", "")} for d in upcoming])


# --- FILE SERVING ROUTES ("Google Drive" Viewer) ---
@app.route('/view/<subject_name>/<filename>')
def view_file(subject_name, filename):
    """ Serves a file for in-browser viewing (PDFs, images) """
    if subject_name not in COURSE_LIST:
        return "Subject not found", 404
    
    directory = os.path.join(app.config['UPLOAD_FOLDER'], subject_name)
    
    # Use send_from_directory, as_attachment=False opens it in the browser
    return send_from_directory(directory, filename, as_attachment=False)

@app.route('/download/<subject_name>/<filename>')
def download_file(subject_name, filename):
    """ Forces a file to download """
    if subject_name not in COURSE_LIST:
        return "Subject not found", 404
        
    directory = os.path.join(app.config['UPLOAD_FOLDER'], subject_name)
    
    # as_attachment=True forces the "Save As..." dialog
    return send_from_directory(directory, filename, as_attachment=True)


# --- ADMIN ROUTES ---

def is_admin():
    """Check if user is logged in as admin"""
    return session.get('is_admin', False)

@app.route('/admin_portal', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        password = request.form.get('password')
        if password == ADMIN_PASSWORD:
            session['is_admin'] = True
            return redirect(url_for('admin_dashboard'))
        else:
            flash("Incorrect password.", "error")
            
    return render_template('admin_login.html')

@app.route('/admin_dashboard')
def admin_dashboard():
    if not is_admin():
        return redirect(url_for('admin_login'))
    
    load_data() # Make sure we have the latest data
    return render_template('admin_dashboard.html', 
                           all_deadlines=deadlines,
                           **get_sidebar_data())

@app.route('/admin/logout')
def admin_logout():
    session.pop('is_admin', None)
    return redirect(url_for('homepage'))

@app.route('/admin/upload', methods=['POST'])
def admin_upload_file():
    if not is_admin():
        return "Unauthorized", 403
    
    file = request.files.get('file')
    subject = request.form.get('subject')

    if not file or not subject or subject not in COURSE_LIST:
        flash("Invalid file or subject.", "error")
        return redirect(url_for('admin_dashboard'))
        
    if file.filename == '':
        flash("No selected file.", "error")
        return redirect(url_for('admin_dashboard'))

    filename = file.filename
    subject_dir = os.path.join(app.config['UPLOAD_FOLDER'], subject)
    os.makedirs(subject_dir, exist_ok=True)
    file.save(os.path.join(subject_dir, filename))
    
    flash(f"File '{filename}' uploaded to '{subject}' successfully.", "success")
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/add_deadline', methods=['POST'])
def admin_add_deadline():
    if not is_admin():
        return jsonify(success=False, error="Unauthorized"), 403
    
    global deadline_id_counter
    title = request.form.get('deadline_title')
    date = request.form.get('deadline_date')
    details = request.form.get('deadline_details', '') # NEW: Get details
    
    if title and date:
        new_deadline = {
            "id": deadline_id_counter,
            "title": title,
            "date": date,
            "details": details, # NEW: Save details
            "completed": False
        }
        deadlines.append(new_deadline)
        deadline_id_counter += 1
        save_data()
        return jsonify(success=True, deadline=new_deadline)
    else:
        return jsonify(success=False, error="Missing title or date"), 400

@app.route('/admin/delete_deadline/<int:deadline_id>')
def admin_delete_deadline(deadline_id):
    if not is_admin():
        return jsonify(success=False, error="Unauthorized"), 403
    
    global deadlines
    original_count = len(deadlines)
    deadlines = [d for d in deadlines if d['id'] != deadline_id]
    
    if len(deadlines) < original_count:
        save_data()
        return jsonify(success=True, deleted_id=deadline_id)
    else:
        return jsonify(success=False, error="Deadline not found"), 404

# --- Main App Runner ---
if __name__ == '__main__':
    # Ensure all subject folders exist on startup
    for subject in COURSE_LIST:
        os.makedirs(os.path.join(app.config['UPLOAD_FOLDER'], subject), exist_ok=True)
    
    # Load the database from db.json
    load_data()
    
    is_production = os.environ.get('REPL_DEPLOYMENT') == '1'
    app.run(host='0.0.0.0', port=5000, debug=(not is_production))