from flask import Blueprint, url_for, render_template, flash, request, session, g, Flask, redirect, current_app
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import redirect
from flask_mail import Mail, Message

from pybo import db
from pybo.forms import UserCreateForm, UserLoginForm
from pybo.models import User

import functools
import config

bp = Blueprint('auth', __name__, url_prefix='/auth')





app = Flask(__name__)
mail = Mail(app)
    
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'a4569677@gmail.com'
app.config['MAIL_PASSWORD'] = '991027Baby~'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True

    
@app.route('/signup/')
def index():
    msg = Message('Hello', sender='a4569677@gmail.com', recipients=['ihg1130@naver.com'])
    msg.body = 'Hello Flask'
    mail.send(msg)
    

@bp.route('/signup/', methods=('GET', 'POST'))
def signup():
    form = UserCreateForm()
    if request.method == 'POST' and form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if not user:
            user = User(username=form.username.data,
                        password=generate_password_hash(form.password1.data),
                        email=form.email.data)
            db.session.add(user)
            db.session.commit()
            msg = Message('Hello', sender='a4569677@gmail.com', recipients=['ihg1130@naver.com'])
            msg.body = 'Hello Flask'
            mail.send(msg)
            
    return render_template('auth/signup.html', form=form)


@bp.route('/login/', methods=('GET', 'POST'))
def login():
    form = UserLoginForm()
    if request.method == 'POST' and form.validate_on_submit():
        error = None
        user = User.query.filter_by(email=form.email.data).first()
        if not user:
            error = "존재하지 않는 사용자입니다."
        elif not check_password_hash(user.password, form.password.data):
            error = "비밀번호가 올바르지 않습니다."
        if error is None:
            session.clear()
            session['user_id'] = user.id
            _next = request.args.get('next', '')
            if _next:
                return redirect(_next)
            else:
                return redirect(url_for('main.index'))
        flash(error)
    return render_template('auth/login.html', form=form)

# 로그인,로그아웃 세션 메소드(모든 라우팅 함수보다 먼저 실행됨)
@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')
    # g.user 는 request 변수처럼 요청 -> 응답 과정을 거침, db 사용자 정보가 저장됨
    if user_id is None:
        g.user = None
    else:
        g.user = User.query.get(user_id)

@bp.route('/logout/')
def logout():
    session.clear()
    return redirect(url_for('main.index'))

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(*args, **kwargs):
        if g.user is None:
            _next = request.url if request.method == 'GET' else ''
            return redirect(url_for('auth.login', next=_next))
        return view(*args, **kwargs)
    return wrapped_view

