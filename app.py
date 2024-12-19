from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Configure the database URI (use SQLite for development)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///projects.db'  # File-based SQLite database
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Disable modification tracking

# Initialize the SQLAlchemy object
db = SQLAlchemy(app)


# Model for projects
class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # Auto-incremented ID
    name = db.Column(db.String(100), nullable=False)  # Project name
    date_added = db.Column(db.String(100), nullable=False)  # Date the project was added
    description = db.Column(db.String(500), nullable=False)  # Project description
    tasks = db.relationship('Task', backref='project', lazy=True)  # Relationship with tasks


# Model for Tasks
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # Auto-incremented ID
    name = db.Column(db.String(100), nullable=False)  # Task name
    date_added = db.Column(db.String(100), nullable=False)  # Date task was added
    description = db.Column(db.String(500), nullable=False)  # Task description
    importance = db.Column(db.Integer, nullable=False)  # Task importance (1-10)
    status = db.Column(db.String(50), default='requested')  # Task status (requested, in-progress, done)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'), nullable=False)  # Foreign key to Project


with app.app_context():
    db.create_all()


# Route for creating a new project
@app.route('/create_project', methods=['POST'])
def create_project():
    # Get form data
    project_name = request.form['project_name']
    date_added = request.form['date_added']
    description = request.form['description']

    # Create a new project object
    new_project = Project(name=project_name, date_added=date_added, description=description)

    # Add the project to the session
    db.session.add(new_project)
    db.session.commit()

    # Redirect to the newly created project page
    return redirect(url_for('project_page', project_id=new_project.id))


# Route for displaying a project's details and tasks
@app.route('/project/<int:project_id>', methods=['GET', 'POST'])
def project_page(project_id):
    # Get the project and its tasks from the database
    project = Project.query.get_or_404(project_id)

    # Handle task creation from the project page
    if request.method == 'POST':
        task_name = request.form['task_name']
        date_added = request.form['date_added']
        description = request.form['description']
        importance = request.form['importance']

        # Create a new task object
        new_task = Task(name=task_name, date_added=date_added, description=description, importance=importance,
                        project_id=project_id)

        # Add the task to the session
        db.session.add(new_task)
        db.session.commit()

        # Redirect back to the project page
        return redirect(url_for('project_page', project_id=project_id))

    return render_template('project_page.html', project=project)


# Route for the homepage
@app.route('/')
def home():
    return render_template('home.html')




@app.route('/saved_projects')
def saved_projects():
    # Fetch all the projects from the database
    projects = Project.query.all()

    # Render the saved_projects page and pass the projects to the template
    return render_template('saved_projects.html', projects=projects)

@app.route('/analytics')
def analytics():
    # Fetch all projects from the database
    projects = Project.query.all()
    project_data = []

    for project in projects:
        # Get all tasks for this project
        total_tasks = len(project.tasks)
        completed_tasks = sum(1 for task in project.tasks if task.status == 'done')

        # Calculate the percentage of completed tasks (if there are tasks)
        if total_tasks > 0:
            completion_percentage = (completed_tasks / total_tasks) * 100
        else:
            completion_percentage = 0

        # Add the project name and its completion percentage to the list
        project_data.append({
            'name': project.name,
            'completion_percentage': round(completion_percentage, 2)
        })

    # Render the analytics page and pass the project data to the template
    return render_template('analytics.html', project_data=project_data)
# Route to the about us page
@app.route('/about_us')
def about_us():
    return render_template('about_us.html')


# Route to handle task creation form submission from the homepage (if needed)
@app.route('/create_task', methods=['POST'])
def create_task():
    # Get form data from the modal
    task_name = request.form.get('task_name')
    date_added = request.form.get('date_added')
    description = request.form.get('description')
    importance = request.form.get('importance')

    # Here you could save the task to a database if necessary
    print(f"Task Name: {task_name}, Date Added: {date_added}, Description: {description}, Importance: {importance}")

    # Redirect back to the homepage after the task is created
    return redirect(url_for('home'))



if __name__ == '__main__':
    app.run(debug=True)
