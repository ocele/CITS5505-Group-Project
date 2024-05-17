from flask import Blueprint, request, session, jsonify
from model.database.db import db, User
import time

lg = Blueprint('lg', __name__)


@lg.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    try:
        username = data['username']
        password = data['password']
        print(username, password)
    except KeyError:
        return jsonify(code=400, message='Request Error')
    finduser = User.query.filter_by(username=username).first()
    if finduser is None:
        return jsonify(code=400, message='User Name Does Not Exit')
    if finduser.password != password:
        return jsonify(code=400, message='Wrong Password')

    session['userid'] = finduser.id
    session['username'] = finduser.username
    session['timestamp'] = time.time()
    return jsonify(code=200, message='Login Successful!')
