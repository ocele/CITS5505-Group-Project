from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  

# 登录接口
@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    return jsonify({ 'code':200,"username": username})
  
  
if __name__ == '__main__':
    app.run(debug=True)