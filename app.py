from flask import Flask, render_template, request, redirect, flash, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import datetime

# Initialize the Flask application
app = Flask(__name__, folder_main = 'main')
app = Flask(__name__, folder_user = 'user')
app.config['SECRET_KEY'] = '5505project'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///puzzles.db'
db = SQLAlchemy(app)

#creat database

request = db.Table('request',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('request_id', db.Integer, db.ForeignKey('request.id'), primary_key=True)
)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)
    request = db.relationship('Request', secondary=request, lazy='subquery',backref=db.backref('accepted_by_users', lazy=True))
    user_responses = db.relationship('Response', backref='response_user', lazy=True) 

class Request(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    request_title = db.Column(db.String(120), nullable=False)
    request_description = db.Column(db.String(300), nullable=False)
    request_status = db.Column(db.String(10), default='open')
    request_responses = db.relationship('Response', backref='response_request', lazy=True)

class Response(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    request_id = db.Column(db.Integer, db.ForeignKey('request.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    response_text = db.Column(db.Text, nullable=False)

class Puzzle(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    puzzle_title = db.Column(db.String(100), nullable=False)
    puzzle_content = db.Column(db.Text, nullable=False)
    puzzle_creator = db.Column(db.String(50), nullable=False)
    puzzle_create_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    puzzle_solve_time = db.Column(db.DateTime)
    puzzle_solved_by = db.Column(db.String(50))


    def __repr__(self):
        return f'<Puzzle {self.id}>'

# Define routes and view functions

# Home page route
@app.route("/")
def home():
    puzzles = Puzzle.query.order_by(Puzzle.create_date.desc()).all()
    return render_template("home.html", puzzles=puzzles)

# Register route
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        # Handle registration form submission
        flash("Registration successful!", "success")
        return redirect(url_for("login"))
    return render_template("register.html")

# Login route
@app.route("/login", methods=["GET", "POST"])
def login():
    error_message = None
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username = username)
        # Handle login form submission
        if user and user.password == password
            flash("Login successful!", "success")
            return redirect(url_for('index'))
        elif user:
            flash('password is wrong, please check')
        else:
            flash('no user, please regist')
            retrun render_template('register.html')

    return redirect(url_for("home"))
    return render_template("index.html")

# Create puzzle route
@app.route("/create_puzzle", methods=["GET", "POST"])
def create_puzzle():
    """
    Render the puzzle creation page and handle puzzle creation form submission.

    Returns:
        str: Rendered HTML content of the puzzle creation page.
    """
    if request.method == "POST":
        title = request.form["title"]
        content = request.form["content"]
        creator = request.form["creator"]
        puzzle = Puzzle(title=title, content=content, creator=creator)
        db.session.add(puzzle)
        db.session.commit()
        flash("Puzzle created successfully!", "success")
        return redirect(url_for("home"))
    return render_template("create_puzzle.html")

# Solve puzzle route
@app.route("/solve_puzzle/<int:puzzle_id>", methods=["GET", "POST"])
def solve_puzzle(puzzle_id):
    """
    Render the puzzle solving page and handle puzzle solving form submission.

    Args:
        puzzle_id (int): The ID of the puzzle to solve.

    Returns:
        str: Rendered HTML content of the puzzle solving page.
    """
    puzzle = Puzzle.query.get_or_404(puzzle_id)
    if request.method == "POST":
        if not puzzle.solved_by:
            puzzle.solve_time = datetime.utcnow()
            puzzle.solved_by = request.form["solver"]
            db.session.commit()
            flash("Puzzle solved successfully!", "success")
        else:
            flash("Puzzle has already been solved!", "danger")
        return redirect(url_for("home"))
    return render_template("solve_puzzle.html", puzzle=puzzle)

# Leaderboard route
@app.route("/leaderboard")
def leaderboard():
    """
    Render the leaderboard page.

    Returns:
        str: Rendered HTML content of the leaderboard page.
    """
    fastest_puzzles = Puzzle.query.filter(Puzzle.solved_by.isnot(None)).order_by(Puzzle.solve_time).limit(10).all()
    return render_template("leaderboard.html", fastest_puzzles=fastest_puzzles)

# Run the application
if __name__ == "__main__":
    app.run(debug=True)
