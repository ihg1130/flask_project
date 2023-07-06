from datetime import datetime
from flask import Flask, Blueprint, current_app, render_template, request, url_for, g, flash, send_file
from pybo.forms import QuestionForm, AnswerForm, ChumoForm
from werkzeug.utils import redirect, secure_filename
from pybo.models import Question, Chumo, User
from datetime import datetime
from .. import db
from pybo.views.auth_views import login_required
from io import BytesIO

import os
import base64

bp = Blueprint('question', __name__, url_prefix='/question')

app=Flask(__name__)

@bp.route('/list/')
def _list():
    chumos = Chumo.query.all()
    page = request.args.get('page', type=int, default=1)  # 페이지
    question_list = Question.query.order_by(Question.create_date.desc())
    question_list = question_list.paginate(page=page, per_page=10)
    return render_template('memorial1.html', question_list=question_list, chumos=chumos)


@bp.route('/detail/<int:question_id>/')
def detail(question_id):
    form = AnswerForm()
    question = Question.query.get_or_404(question_id)
    return render_template('question/question_detail.html', question=question, form=form, image_file='images/question.file_name.png')

@bp.route('/create/', methods=('GET', 'POST'))
@login_required
def create():
    form = QuestionForm()
    # user = User.query.all()
    if request.method == 'GET':
        chumos = Chumo.query.all()
        for chumo in chumos:
         if chumo.profile_data is not None:
           chumo.profile_data = base64.b64encode(chumo.profile_data).decode('utf-8')
    if request.method == 'POST' and form.validate_on_submit():
        file = request.files['file_data']
        file_data = file.read()
        question = Question(file_data=file_data, subject=form.subject.data, content=form.content.data,
                             name=form.name.data, relation=form.relation.data,
                             create_date=datetime.now(), user=g.user)
        db.session.add(question)
        db.session.commit()
        return redirect(url_for('question._list'))
    return render_template('memorial.html', form=form, chumos=chumos)


@bp.route('/modify/<int:question_id>', methods=('GET', 'POST'))
@login_required
def modify(question_id):
    question = Question.query.get_or_404(question_id)
    if g.user != question.user:
        flash('수정권한이 없습니다')
        return redirect(url_for('question.detail', question_id=question_id))
    if request.method == 'POST':  # POST 요청
        form = QuestionForm()
        if form.validate_on_submit():
            # form 변수에 들어있는 입력 데이터를 question 객체에 업데이트
            form.populate_obj(question)
            question.modify_date = datetime.now()  # 수정일시 저장
            db.session.commit()
            return redirect(url_for('question.detail', question_id=question_id))
    else:  # GET 요청, 조회한 데이터를 obj 매개변수에 전달하여 폼 생성
        form = QuestionForm(obj=question)
    return render_template('question/question_form.html', form=form)

@bp.route('/delete/<int:question_id>')
@login_required
def delete(question_id):
    question = Question.query.get_or_404(question_id)
    if g.user != question.user:
        flash('삭제권한이 없습니다')
        return redirect(url_for('question.detail', question_id=question_id))
    db.session.delete(question)
    db.session.commit()
    return redirect(url_for('question._list'))

@bp.route('/vote/<int:question_id>/')
@login_required
def vote(question_id):
    _question = Question.query.get_or_404(question_id)
    # if g.user == _question.user:
    #     flash('본인이 작성한 글은 추천할수 없습니다')
    # else:
    _question.voter.append(g.user)
    db.session.commit()
    return redirect(url_for('question.detail', question_id=question_id))

@bp.route('/new', methods=('GET', 'POST'))
@login_required
def new():
    form = ChumoForm()
    if request.method == 'POST' and form.validate_on_submit():
        file = request.files['profile_data']
        profile_data = file.read()
        chumo = Chumo(profile_data=profile_data, name=form.name.data, birth=form.birth.data,
                             death=form.death.data,
                            content=form.content.data,
                             create_date=datetime.now(), user=g.user)
        db.session.add(chumo)
        db.session.commit()
        
        return redirect(url_for('question.create'))
    return render_template('new.html', form=form)

@bp.route('/send')
@login_required
def send():
      return render_template("send.html")

@bp.route('/massage')
@login_required
def massage():
      return render_template("main_massage.html")

@bp.route('/setting')
@login_required
def setting():
      return render_template("setting.html")

@bp.route('/rooms')
@login_required
def rooms():
      return render_template("rooms.html")

@bp.route('/history')
@login_required
def history():
      return render_template("history.html")

@bp.route('/gallery')
@login_required
def gallery():
    chumos = Chumo.query.all()
    questions = Question.query.all()
    for question in questions:
        if question.file_data is not None:
           question.file_data = base64.b64encode(question.file_data).decode('utf-8')
    return render_template('gallery.html', questions=questions, chumos=chumos)
      

@bp.route('/timeline')
@login_required
def timeline():
      chumos = Chumo.query.all()
      return render_template("timeline.html", chumos=chumos)



