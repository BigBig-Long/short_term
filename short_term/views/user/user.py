from flask import Flask,session,render_template,redirect,Blueprint,request
from short_term.model.User import User
from short_term.utils.errorResponse import *
from short_term.db import database

# 创建蓝图，实现路由的接收
ub = Blueprint('user',__name__,url_prefix='/user',template_folder='templates')

@ub.route('/login',methods=['GET','POST'])
def login():
    if request.method == 'POST':
        user = User.query.filter_by(user_name=request.form['username'],user_password=request.form['password']).first()
        if user:
            session['username'] = user.user_name
            return redirect('/page/home')
        else:
            return errorResponse('输入的密码或账号出现问题')
    else:
        return render_template('login.html')

@ub.route('/register',methods=['GET','POST'])
def register():
    if request.method == 'POST':
        user = User.query.filter_by(user_name=request.form['username']).first()
        if user:
            return errorResponse('该用户名已存在')
        newUser = User(user_name=request.form['username'],user_password=request.form['password'])
        database.session.add(newUser)
        database.session.commit()
        return redirect('/user/login')
    else:
        return render_template('register.html')

@ub.route('/logOut',methods=['GET','POST'])
def logOut():
    session.clear()
    return redirect('/user/login')
