from app.controller.indexcontroller.blueprint import upload
from flask import render_template,request,g,jsonify
from model.database.db import Article,db
import html
@upload.route('/upload.html', methods=['GET'])
def upload_file():
    return render_template('upload.html')
@upload.route('/blogupload', methods=['POST'])
def upload_blog():
    user=g.get('userObject')
    userid=user.id
    data=request.get_json()
    
    try:
        content=data['content']
        title=data['title']
    except KeyError:
        return jsonify(code=400,message='参数错误')

    db.session.add(Article(title=title,content=content,userid=userid))
    db.session.commit()
    user.money=user.money+1
    db.session.commit()
    return jsonify(code=200,message='上传成功,获得1积分!')