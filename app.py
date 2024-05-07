from flask import Flask, render_template, request, redirect, flash, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# Initialize the Flask application
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key_here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///puzzles.db'
db = SQLAlchemy(app)

# Define database models
class Puzzle(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    creator = db.Column(db.String(50), nullable=False)
    create_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    solve_time = db.Column(db.DateTime)
    solved_by = db.Column(db.String(50))

    def __repr__(self):
        return f'<Puzzle {self.id}>'

# Define routes and view functions

# Home page route
@app.route("/")
def home():
    """
    Render the home page.

    Returns:
        str: Rendered HTML content of the home page.
    """
    puzzles = Puzzle.query.order_by(Puzzle.create_date.desc()).all()
    return render_template("home.html", puzzles=puzzles)

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




