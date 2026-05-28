from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import date

app = Flask(__name__)
app.secret_key = "synq_secret_key"

# MySQL Database Configuration

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://admin:windowss@synq-mysql.cpwsciem63aw.ap-south-1.rds.amazonaws.com:3306/synqdb'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize Database

db = SQLAlchemy(app)

# User Model

class User(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    username = db.Column(db.String(100), nullable=False)

    email = db.Column(db.String(120), unique=True, nullable=False)

    password = db.Column(db.String(200), nullable=False)
    role = db.Column(
    db.String(20),
    default="user"
)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    title = db.Column(db.String(200), nullable=False)

    description = db.Column(db.Text, nullable=False)

    status = db.Column(db.String(50), default="To Do")

    priority = db.Column(db.String(50), default="Medium")

    due_date = db.Column(db.String(50))

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

# Routes

@app.route("/")
def home():

    return render_template("index.html")

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form["email"]

        password = request.form["password"]

        # Find user by email

        user = User.query.filter_by(email=email).first()

        # Check user exists and password matches

        if user and check_password_hash(user.password, password):

            session["user_id"] = user.id
            session["username"] = user.username
            session["role"] = user.role

            # ADMIN LOGIN
            if user.role == "admin":
                return redirect(url_for("admin"))

            # NORMAL USER LOGIN
            return redirect(url_for("dashboard"))

        else:

            return "Invalid email or password"

    return render_template("login.html")
@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        username = request.form["username"]

        email = request.form["email"]

        password = request.form["password"]

        confirm_password = request.form["confirm_password"]

        # Check password match

        if password != confirm_password:
            return "Passwords do not match"

        # Hash password

        hashed_password = generate_password_hash(password)

        # Create user

        new_user = User(
            username=username,
            email=email,
            password=hashed_password
        )

        # Save to database

        db.session.add(new_user)

        db.session.commit()

        # Redirect to login

        return redirect(url_for("login"))

    return render_template("register.html")

@app.route("/dashboard")
def dashboard():
    
    search_query = request.args.get("search", "")

    if "user_id" not in session:
        return redirect(url_for("login"))

    username = session["username"]

    if search_query:

     user_tasks = Task.query.filter(
        Task.user_id == session["user_id"],
        Task.title.ilike(f"%{search_query}%")
     ).all()

    else:

     user_tasks = Task.query.filter_by(
        user_id=session["user_id"]
     ).all()

    # REAL TASK LISTS

    todo_tasks = [
        task for task in user_tasks
        if task.status == "To Do"
    ]

    inprogress_tasks = [
        task for task in user_tasks
        if task.status == "In Progress"
    ]

    completed_task_list = [
        task for task in user_tasks
        if task.status == "Completed"
    ]

    # COUNTS

    total_tasks = len(user_tasks)

    completed_tasks = len(completed_task_list)

    progress_tasks = len(inprogress_tasks)

    pending_tasks = len(todo_tasks)

    # PERCENTAGE

    if total_tasks > 0:
        completion_percentage = int(
            (completed_tasks / total_tasks) * 100
        )
    else:
        completion_percentage = 0

    return render_template(
        "dashboard.html",
        search_query=search_query,

        username=username,

        total_tasks=total_tasks,

        completed_tasks=completed_tasks,

        progress_tasks=progress_tasks,

        pending_tasks=pending_tasks,

        completion_percentage=completion_percentage,

        todo_tasks=todo_tasks,

        inprogress_tasks=inprogress_tasks,

        completed_task_list=completed_task_list
    )
@app.route("/tasks")
def tasks():

    if "user_id" not in session:
        return redirect(url_for("login"))

    # ADMIN ACCESS

    if session.get("role") == "admin":

        users = User.query.all()

        user_tasks = {}

        for user in users:

            tasks = Task.query.filter_by(
                user_id=user.id
            ).all()

            user_tasks[user.id] = tasks

        return render_template(
            "admin_tasks.html",
            users=users,
            user_tasks=user_tasks
        )

    # NORMAL USER

    tasks = Task.query.filter_by(
        user_id=session["user_id"]
    ).all()

    return render_template(
        "tasks.html",
        tasks=tasks
    )
@app.route("/schedule")
def schedule():

    if "user_id" not in session:
        return redirect(url_for("login"))

    today = date.today()

    user_tasks = Task.query.filter_by(
        user_id=session["user_id"]
    ).all()

    today_tasks = []

    upcoming_tasks = []

    overdue_tasks = []

    for task in user_tasks:

        if task.due_date:

            task_date = date.fromisoformat(
                str(task.due_date)
            )

            if task_date == today:

                today_tasks.append(task)

            elif task_date > today:

                upcoming_tasks.append(task)

            else:

                if task.status != "Completed":

                    overdue_tasks.append(task)

    return render_template(
        "schedule.html",

        today_tasks=today_tasks,

        upcoming_tasks=upcoming_tasks,

        overdue_tasks=overdue_tasks
    )

@app.route("/analytics")
def analytics():

    if "user_id" not in session:
        return redirect(url_for("login"))

    user_tasks = Task.query.filter_by(
        user_id=session["user_id"]
    ).all()

    total_tasks = len(user_tasks)

    completed_tasks = len([
        task for task in user_tasks
        if task.status == "Completed"
    ])

    progress_tasks = len([
        task for task in user_tasks
        if task.status == "In Progress"
    ])

    pending_tasks = len([
        task for task in user_tasks
        if task.status == "To Do"
    ])

    high_priority = len([
        task for task in user_tasks
        if task.priority == "High"
    ])

    medium_priority = len([
        task for task in user_tasks
        if task.priority == "Medium"
    ])

    low_priority = len([
        task for task in user_tasks
        if task.priority == "Low"
    ])

    if total_tasks > 0:

        completion_percentage = int(
            (completed_tasks / total_tasks) * 100
        )

    else:

        completion_percentage = 0

    return render_template(
        "analytics.html",

        total_tasks=total_tasks,

        completed_tasks=completed_tasks,

        progress_tasks=progress_tasks,

        pending_tasks=pending_tasks,

        high_priority=high_priority,

        medium_priority=medium_priority,

        low_priority=low_priority,

        completion_percentage=completion_percentage
    )

@app.route("/admin")
def admin():

    if "user_id" not in session:
        return redirect(url_for("login"))

    if session.get("role") != "admin":
        return redirect(url_for("dashboard"))

    users = User.query.all()

    total_users = User.query.count()

    total_tasks = Task.query.count()

    completed_tasks = Task.query.filter_by(
        status="Completed"
    ).count()

    pending_tasks = Task.query.filter_by(
        status="To Do"
    ).count()

    recent_users = User.query.order_by(
        User.id.desc()
    ).limit(3).all()

    return render_template(

        "admin.html",

        users=users,

        total_users=total_users,

        total_tasks=total_tasks,

        completed_tasks=completed_tasks,

        pending_tasks=pending_tasks,

        recent_users=recent_users
    )

@app.route("/delete_user/<int:user_id>")
def delete_user(user_id):

    # Check login

    if "user_id" not in session:
        return redirect(url_for("login"))

    # Only admin allowed

    if session.get("role") != "admin":
        return redirect(url_for("dashboard"))

    # Get user

    user = User.query.get(user_id)

    # Prevent deleting admin

    if user.role == "admin":
        return redirect(url_for("admin"))

    # Delete all tasks of that user first

    Task.query.filter_by(user_id=user.id).delete()

    # Delete user

    db.session.delete(user)

    db.session.commit()

    return redirect(url_for("admin"))
@app.route("/profile")
def profile():

    user = User.query.get(session["user_id"])

    return render_template(
        "profile.html",
        username=user.username,
        email=user.email
    )
@app.route("/add_task", methods=["POST"])
def add_task():

    if "user_id" not in session:
        return redirect(url_for("login"))

    title = request.form["title"]
    description = request.form["description"]
    status = request.form["status"]
    priority = request.form["priority"]
    due_date = request.form["due_date"]

    new_task = Task(
        title=title,
        description=description,
        status=status,
        priority=priority,
        due_date=due_date,
        user_id=session["user_id"]
    )

    db.session.add(new_task)
    db.session.commit()

    flash("Task added successfully!", "success")

    return redirect(url_for("tasks"))
@app.route("/move_task/<int:task_id>/<status>")
def move_task(task_id, status):

    task = Task.query.get(task_id)

    if status == "todo":
        task.status = "To Do"

    elif status == "progress":
        task.status = "In Progress"

    elif status == "completed":
        task.status = "Completed"

    db.session.commit()

    return redirect(url_for("tasks"))

@app.route("/delete_task/<int:task_id>")
def delete_task(task_id):

    task = Task.query.get(task_id)

    db.session.delete(task)

    db.session.commit()

    return redirect(url_for("tasks"))

@app.route("/edit_task/<int:task_id>",
methods=["GET", "POST"])

def edit_task(task_id):

    if "user_id" not in session:
        return redirect(url_for("login"))

    task = Task.query.get(task_id)

    if request.method == "POST":

        task.title = request.form["title"]

        task.description = request.form["description"]

        task.status = request.form["status"]

        task.priority = request.form["priority"]

        task.due_date = request.form["due_date"]

        db.session.commit()

        return redirect(url_for("tasks"))

    return render_template(
        "edit_task.html",
        task=task
    )

@app.route("/projects")
def projects():

    if "user_id" not in session:
        return redirect(url_for("login"))

    return render_template("projects.html")
@app.route("/logout")
def logout():

    session.clear()

    return redirect(url_for("login"))


# Run App

if __name__ == "__main__":

    with app.app_context():
        db.create_all()

    app.run(host='0.0.0.0', port=5000, debug=False)
# CI/CD TEST