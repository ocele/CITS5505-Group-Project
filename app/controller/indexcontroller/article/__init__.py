from app.controller.indexcontroller.blueprint import article
from model.database.db import Article,Comment,db,Articlelike,User
from flask import render_template,request,jsonify,g,session
from sqlalchemy.exc import IntegrityError
import html
@article.route('/article')
def get_article():
    id=request.args.get('id',type=int)
    if id is None:
         return jsonify(code=400,message='页面不存在'),404
    art=Article.query.filter_by(id=id).first()
    if art is None:
        return jsonify(code=400,message='页面不存在'),404
    username=session.get('username')
    if username is None:
       return render_template('article.html',userdata=art.user,art=art)
    user=User.query.filter_by(username=username).first()
    if user is None:
        session.clear()
        return render_template('article.html',userdata=art.user,art=art)
    
    if Articlelike.query.filter_by(userid=user.id,articleid=id).first() is None:
         return render_template('article.html',userdata=art.user,art=art)
    active='active'
    return render_template('article.html',userdata=art.user,art=art,active=active)
@article.route('/comment/add',methods=['POST'])
def addarticle():
    data=request.get_json()
    try:
        article_id=data['article_id']
        content=data['content']
    except KeyError:
        return jsonify(code=400,message='参数错误')
    userobject=g.get('userObject')
    boolvalue=False
    findcomm=Comment.query.filter_by(articleid=article_id,userid=userobject.id).first()
    if findcomm is None:
        boolvalue=True
    try:
        db.session.add(Comment(articleid=article_id,userid=userobject.id,content=html.escape(content)))
        db.session.commit()
    except IntegrityError:
        return jsonify(code=400,message='评论失败')
    if boolvalue:
        userobject.money=userobject.money+1
    
        db.session.commit()
        return jsonify(code=200,message='评论成功,+1积分')
    return jsonify(code=200,message='评论成功')
@article.route('/getcomment')
def getcomment():
    articleid=request.args.get('article_id',type=int)
    if articleid is None:
        return jsonify(code=400,message='页面不存在')
    data=[]
    artdata=Comment.query.filter(Comment.articleid==articleid).all()

    for i in artdata:
        data.append({'id':i.id,'content':i.content,'user':i.user.username,'avatar':'/static/photo/'+i.user.photopath})
    return jsonify(code=200,message='获取成功',data=data)

@article.route('/like',methods=['POST'])
def clicklick():
    articleid=request.get_json().get('articleid')
    if articleid is None:
        return jsonify(code=400,message='参数错误')
    userObject=g.get('userObject')
    like=Articlelike.query.filter_by(userid=userObject.id,articleid=articleid)
    if  like.first() is None:
        db.session.add(Articlelike(userid=userObject.id,articleid=articleid))
        db.session.commit()
        return jsonify(code=200,message='点赞成功')
    like.delete()
    db.session.commit()
    return jsonify(code=200,message='取消点赞成功')
    