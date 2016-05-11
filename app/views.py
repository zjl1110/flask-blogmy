from app import app,db,lm,models
from flask import render_template,flash,redirect,url_for,session,request,g
from forms import LoginForm,EditForm,PlForm
from .models import User,Post,Pinl
from flask.ext.login import login_user,logout_user,current_user,login_required
from config import PASSWORD_KEY
import hashlib
from datetime import datetime


@lm.user_loader
def load_user(id):
    return User.query.get(int(id))

@app.before_request
def before_request():
    g.user = current_user


@app.route('/')
@app.route('/index')
def index ():
    tiltes=models.Post.query.all()
    return render_template('index.html',tiltes=tiltes)


@app.route('/login',methods=['POST','GET'])
def login():
    form=LoginForm()
    if form.validate_on_submit():
        md5=hashlib.md5()
        md5.update(form.userpassword.data+PASSWORD_KEY)
        form_password=md5.hexdigest()
        if models.User.query.filter_by(username=form.username.data,userpassword=form_password).first():
            user = User.query.filter_by(username=form.username.data,userpassword=form_password).first_or_404()
            login_user(user)
            #flash('username: '+form.username.data+" "+'password: '+form.userpassword.data+str(g.user))
            return redirect('edit')
        else:
            error='[NO]'
            return render_template('login.html',form=form,error=error)
    return render_template('login.html',form=form)


@app.route('/logout',methods=['POST','GET'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/edit',methods=['POST','GET'])
@login_required
def edit():
    form=EditForm()
    if form.validate_on_submit():
        title=form.blogtilte.data
        body=form.blogbody.data
        if body or title:
            post=models.Post(tilte=title,body=body,timestamp=datetime.utcnow(),author=g.user)
        try:
            db.session.add(post)
            db.session.commit()
        except Exception,e:
            db.session.rollback()
        flash('OK',request.args)
        return redirect('edit')
        #error='OK'
        #return render_template('edit.html',form=form,error=error)
    
    else:
        flash('None')
        return render_template('edit.html',form=form)


@app.route('/xxx/<int:id>',methods=['POST','GET'])
@login_required
def xxx(id):
    form=EditForm()
    post=models.Post.query.filter_by(id=id).first_or_404()
    if form.validate_on_submit():
        post.tilte=form.blogtilte.data
        post.body=form.blogbody.data
        try:
            db.session.add(post)
            db.session.commit()
        except Exception,e:
            db.session.rollback()
        flash('OK',request.args)
        return redirect(url_for('xxx',id=id))
        #error='OK'
        #return render_template('edit.html',form=form,error=error)
    
    else:
        form.blogtilte.data=post.tilte
        form.blogbody.data=post.body
        id=post.id
        return render_template('xxx.html',form=form)

    

@app.route('/blogxlist')
@login_required
def blogxlist():
    tiltes=models.Post.query.all()
    return render_template('blogxlist.html',tiltes=tiltes)

@app.route('/dels/<int:id>',methods=['POST','GET'])
@login_required
def dels(id):
    if id :
        try:
            post=models.Post.query.filter_by(id=id).first()
            pingls=models.Pinl.query.filter_by(body_id=id).all()
            for pingl in pingls:
                db.session.delete(pingl)
            db.session.delete(post)
            db.session.commit()
        except Exception,e:
           db.session.rollback() 
    return redirect('blogxlist')



@app.route('/pinglxlist')
@login_required
def pinglxlist():
    tiltes=models.Pinl.query.all()
    return render_template('pinglxlist.html',tiltes=tiltes)

@app.route('/pingldels/<int:id>',methods=['POST','GET'])
@login_required
def pingldels(id):
    if id :
        try:
            pingl=models.Pinl.query.filter_by(id=id).first()
            db.session.delete(pingl)
            db.session.commit()
        except Exception,e:
           db.session.rollback() 
    return redirect('pinglxlist')



@app.route('/blogxq/<int:id>',methods=['POST','GET'])
def blogxq(id):
    post=models.Post.query.filter_by(id=id).first_or_404()
    title=post.tilte
    body=post.body
    time=post.timestamp
    time=str(time).split(' ')[0]
    pinglbodys=models.Pinl.query.filter_by(body_id=id).all()
    form=PlForm()
    if form.validate_on_submit():
        plbody=form.plbody.data
        pinglun=models.Pinl(plbody=plbody,timestamp=datetime.utcnow(),postt=post)
        db.session.add(pinglun)
        db.session.commit()
    return render_template('blogxq.html',title=title,body=body,time=time,id=id,form=form,pinglbodys=pinglbodys)

