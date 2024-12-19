from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Route to the homepage
@app.route('/')
def home():
    return render_template('home.html')

# Route to the saved projects page
@app.route('/saved_projects')
def saved_projects():
    return render_template('saved_projects.html')

# Route to the analytics page
@app.route('/analytics')
def analytics():
    return render_template('analytics.html')

# Route to the about us page
@app.route('/about_us')
def about_us():
    return render_template('about_us.html')

# Route to handle task creation form submission
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
