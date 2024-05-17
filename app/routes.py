from flask import Blueprint, render_template, request, redirect, url_for, jsonify, session
from flask_login import logout_user, login_required
from .forms import RegistrationForm, LoginForm
from model.database.db import db, User, Article
from sqlalchemy.exc import IntegrityError
from flask import flash
import time
from functools import wraps

main = Blueprint('main', __name__)
auth = Blueprint('auth', __name__)

def my_login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if 'userid' not in session or 'username' not in session:
            return jsonify(code=401, message='Login Required')
        return func(*args, **kwargs)

    return wrapper

@main.route('/')
def index():
    users = User.query.order_by(User.money.desc()).all()  # Replace with actual data retrieval logic
    return render_template('leaderboard.html', users=users)

@main.route('/index')
def index_page():
    tasks = []
    articledata = Article.query.join(User).filter(Article.userid == User.id).order_by(Article.create_time.desc()).all()
    for i in articledata:
        tasks.append(
            {'id': i.id, 'title': i.title, 'content': i.content, 'time': i.create_time.strftime("%Y-%m-%d %H:%M")}
        )
    return render_template('index.html', tasks=tasks)

@main.route('/login')
def main_login():
    type = request.args.get('type', default=1, type=int)
    return render_template('login.html', type=type)

@main.route('/profile')
def profile():
    if 'username' in session:
        username = session['username']
        return render_template('profile.html', username=username)
    else:
        return redirect(url_for('main_login'))

@main.route('/forgot_password')
def forgot_password():
    return render_template('password.html')

@auth.route('/register', methods=['GET', 'POST'])
def app_register():
    if request.method == 'POST':
        data = request.get_json()
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')

        if not username or not email or not password:
            return jsonify({'code': 400, 'message': 'Please provide all required fields.'}), 200

        if User.query.filter_by(username=username).first():
            return jsonify({'code': 400, 'message': 'User Name Has Been Taken.'}), 200

        if User.query.filter_by(email=email).first():
            return jsonify({'code': 400, 'message': 'Email already exists.'}), 200

        new_user = User(username=username, email=email, password=password)

        db.session.add(new_user)
        db.session.commit()
        session['username'] = new_user.username
        session['userid'] = new_user.id
        session['timestamp'] = time.time()

        return jsonify({'code': 200, 'message': 'User registered successfully.'}), 200
    else:
        return render_template('register.html')

@main.route('/logout')
def logout():
    session.pop('username', None)
    session.pop('userid', None)
    session.pop('timestamp', None)
    logout_user()
    return redirect(url_for('main.index'))

@main.route('/search', methods=['POST'])
def search():
    keyword = request.form.get('keyword')
    sort_order = request.form.get('sortOrder')

    query = Article.query.filter(Article.title.contains(keyword) | Article.content.contains(keyword))

    if sort_order == 'date-newest':
        query = query.order_by(Article.create_time.desc())
    elif sort_order == 'date-oldest':
        query = query.order_by(Article.create_time.asc())

    tasks = query.all()

    results = [
        {'id': task.id, 'title': task.title, 'content': task.content,
         'time': task.create_time.strftime("%Y-%m-%d %H:%M")}
        for task in tasks
    ]

    return render_template('index.html', tasks=results, word=keyword)

