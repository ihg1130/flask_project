from flask import Flask, Blueprint, render_template, request, url_for
from pybo.forms import QuestionForm, AnswerForm
from werkzeug.utils import redirect
from pybo.models import Question
from datetime import datetime
from .. import db
from werkzeug.utils import secure_filename

bp = Blueprint('question', __name__, url_prefix='/question')
app = Flask(__name__)

app.config['']


@bp.route('/list/')
def _list():
    page = request.args.get('page', type=int, default=1)  # 페이지
    question_list = Question.query.order_by(Question.create_date.desc())
    question_list = question_list.paginate(page=page, per_page=10)
    return render_template('question/question_list.html', question_list=question_list)


@bp.route('/detail/<int:question_id>/')
def detail(question_id):
    form = AnswerForm()
    question = Question.query.get_or_404(question_id)
    return render_template('question/question_detail.html', question=question, form=form)

@bp.route('/create/', methods=('GET', 'POST'))
def create():
    form = QuestionForm()
    if request.method == 'POST' and form.validate_on_submit():
        question = Question(subject=form.subject.data, content=form.content.data, create_date=datetime.now())
        db.session.add(question)
        db.session.commit()
        return redirect(url_for('main.index'))
    return render_template('question/question_form.html', form=form)


@app.route('/uploader', methods=['GET', 'POST'])
def uploader_file(): 
    if request.method =='POST':
        f = request.files['file']
        f.save(secure_filename(f.filename))
        return render_template('question/list.html')
    else:
        return render_template('question_form.html')
    