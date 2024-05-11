from flask import Flask, render_template, request, redirect, flash, url_for, session
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import datetime

app = Flask(__name__, template_folder='templates')
app.config['SECRET_KEY'] = '5505project'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///puzzles.db'
db = SQLAlchemy(app)
migrate = Migrate(app, db)

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(80), nullable=False)
    lastname = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(80), unique=True, nullable=False)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)
    requests = db.relationship('Request', backref='user', lazy=True)
    rewards = db.Column(db.Integer, default=0)

class Request(db.Model):
    __tablename__ = 'request'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    request_title = db.Column(db.String(120), nullable=False)
    request_description = db.Column(db.String(300), nullable=False)
    request_status = db.Column(db.String(10), default='open')
    responses = db.relationship('Response', backref='request', lazy=True)

class Response(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    request_id = db.Column(db.Integer, db.ForeignKey('request.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    response_text = db.Column(db.Text, nullable=False)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    deadline = db.Column(db.DateTime, nullable=False)
    rewards = db.Column(db.Integer, nullable=False)

# Home page route
@app.route("/")
def home():
    sort_option = request.args.get('sort', 'rewards-high')

    if sort_option == 'rewards-high':
        tasks = Task.query.order_by(Task.rewards.desc()).all()
    elif sort_option == 'rewards-low':
        tasks = Task.query.order_by(Task.rewards).all()
    elif sort_option == 'date-newest':
        tasks = Task.query.order_by(Task.deadline.desc()).all()
    elif sort_option == 'date-oldest':
        tasks = Task.query.order_by(Task.deadline).all()
    else:
        tasks = Task.query.all()
    return render_template("home.html", tasks=tasks)

# Login route
@app.route("/index.html", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user:
            if user.password == password:
                session['user_id'] = user.id  # Store user ID in session
                flash("Login successful!", "success")
                return redirect(url_for('home'))
            else:
                flash('Incorrect password. Please try again.', "danger")
        else:
            flash('User does not exist. Please register.', "danger")
    return render_template("index.html")

# Register route
@app.route("/register.html", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']

        existing_user = User.query.filter_by(username=username).first()
        existing_email = User.query.filter_by(email=email).first()
        if existing_user:
            flash('Username already exists. Please choose a different username.', "danger")
        elif existing_email:
            flash('The email address has already been used. Please use a different email address.', "danger")
        else:
            new_user = User(firstname=firstname, lastname=lastname, email=email, username=username, password=password)
            db.session.add(new_user)
            db.session.commit()
            flash("Registration successful!", "success")
            return redirect(url_for("home"))
    return render_template("register.html")

# Logout route
@app.route("/logout")
def logout():
    session.pop('user_id', None)  # Remove user ID from session
    flash("You have been logged out.", "info")
    return redirect(url_for('home'))

# Upload page route
@app.route("/upload.html", methods=["GET", "POST"])
def upload():
    if 'user_id' not in session:
        flash("Please log in first.", "danger")
        return redirect(url_for("login"))

    if request.method == "POST":
        title = request.form['title']
        content = request.form['content']
        deadline = datetime.strptime(request.form['deadline'], '%Y-%m-%d')
        rewards = int(request.form['rewards'])

        new_task = Task(title=title, content=content, deadline=deadline, rewards=rewards)
        db.session.add(new_task)
        db.session.commit()

        flash("Task uploaded successfully!", "success")
        return redirect(url_for("home"))
    
    return render_template("upload.html")

# Profile page route
@app.route("/profile.html")
def profile():
    if 'user_id' in session:
        user_id = session['user_id']
        user = User.query.get(user_id)
        if user:
            return render_template("profile.html", user=user)
    flash("You need to log in first.", "warning")
    return redirect(url_for("login"))

@app.route('/leaderboard.html')
def leaderboard():
    users = User.query.order_by(User.rewards.desc()).limit(50).all()
    return render_template('leaderboard.html', users=users)

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
