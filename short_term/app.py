from flask import Flask, session, render_template, redirect, request, Blueprint
from config import Config
from db import db
import re


from views.page import page
from views.user import user
app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

# 注册蓝图
app.register_blueprint(page.pb)
app.register_blueprint(user.ub)

pb = Blueprint('page', __name__, url_prefix='/page', template_folder='templates')
print(f"蓝图模板文件夹: {pb.template_folder}")

@app.route('/')
def index():
    return redirect('/user/login')

@app.before_request
def before_request():
    pat = re.compile(r'^/static')
    if re.search(pat, request.path):
        return
    if request.path == '/user/login':
        return
    if request.path == '/user/register':
        return
    uname = session.get('username')
    if uname:
        return None

    return redirect('/user/login')

@app.route('/<path:path>')
def catch_all(path):
    return render_template('404.html')

if __name__ == '__main__':
    app.run()
