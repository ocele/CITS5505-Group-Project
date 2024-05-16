from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError

app = Flask(__name__)
app.secret_key = "your_secret_key"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///requests.db'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(50), nullable=False)

class Request(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('requests', lazy=True))
    answers = db.relationship('Answer', backref='request', lazy=True)

class Answer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('answers', lazy=True))
    request_id = db.Column(db.Integer, db.ForeignKey('request.id'), nullable=False)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        # Your registration logic here...
        # Check if username is already taken
        user = User.query.filter_by(username=username).first()
        if user:
            error_message = 'Username already taken. Please choose another one.'
            session['error_message'] = error_message
            return redirect(url_for('register'))
        # Registration successful
        session['success_message'] = 'Registration successful. You can now login.'
        return redirect(url_for('login'))
    error_message = session.pop('error_message', None)
    success_message = session.pop('success_message', None)
    return render_template('register.html', error_message=error_message, success_message=success_message)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user:
            if user.password == password:
                # Successful login
                session['user_id'] = user.id
                session['username'] = user.username
                return redirect(url_for('user_dashboard'))
            else:
                error_message = 'Wrong password.'
        else:
            error_message = 'No such user. Please register.'
        session['error_message'] = error_message
        return redirect(url_for('login'))
    error_message = session.pop('error_message', None)
    return render_template('login.html', error_message=error_message)

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('username', None)
    return redirect(url_for('index'))

@app.route('/user/dashboard')
def user_dashboard():
    if 'user_id' in session:
        user_id = session['user_id']
        user = User.query.get(user_id)
        requests = Request.query.filter_by(user_id=user_id).all()
        return render_template('user_dashboard.html', user=user, requests=requests)
    return redirect(url_for('login'))

@app.route('/request/create', methods=['GET', 'POST'])
def create_request():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        user_id = session['user_id']
        new_request = Request(title=title, description=description, user_id=user_id)
        db.session.add(new_request)
        db.session.commit()
        flash('Request created successfully.')
        return redirect(url_for('user_dashboard'))
    return render_template('create_request.html')

@app.route('/request/search')
def search_request():
    keyword = request.args.get('keyword')
    if keyword:
        requests = Request.query.filter(Request.title.contains(keyword) | Request.description.contains(keyword)).all()
    else:
        requests = Request.query.all()
    return render_template('search_request.html', requests=requests)

@app.route('/request/<int:request_id>/answer', methods=['POST'])
def answer_request(request_id):
    if 'user_id' in session:
        user_id = session['user_id']
        text = request.form['text']
        answer = Answer(text=text, user_id=user_id, request_id=request_id)
        db.session.add(answer)
        db.session.commit()
        flash('Your answer has been posted.')
        return redirect(url_for('view_request', request_id=request_id))
    return redirect(url_for('login'))

@app.route('/request/<int:request_id>')
def view_request(request_id):
    request_obj = Request.query.get(request_id)
    return render_template('view_request.html', request=request_obj)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
