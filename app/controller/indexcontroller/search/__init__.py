from app.controller.indexcontroller.blueprint import  serch
from flask import request,render_template
from model.database.db import Article,db
@serch.route('/search',methods=['POST'])
def search():
    searchtext=request.form.get('keyword')
    if searchtext is None:
        return "请输入关键词"
    articles = Article.query.filter(db.or_(Article.title.like(f'%{searchtext}%'), Article.content.like(f'%{searchtext}%'))).all()
    data=[]
    for i in articles:
       data.append({"id":i.id,"title":i.title,"content":i.content,'time':i.create_time.strftime("%Y-%m-%d %H:%M")})
    data = [dict(t) for t in {tuple(d.items()) for d in data}]
    return render_template('index.html',tasks=data,word=searchtext)
