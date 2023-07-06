from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, PasswordField, EmailField
from wtforms.validators import DataRequired, Length, EqualTo, Email
from flask_wtf.file import FileField

class QuestionForm(FlaskForm):
    subject = StringField('제목', validators=[DataRequired('제목은 필수입력 항목입니다.')])
    content = TextAreaField('내용', validators=[DataRequired('내용은 필수입력 항목입니다.')])
    name = TextAreaField('이름', validators=[DataRequired('이름은 필수입력 항목입니다.')])
    relation = TextAreaField('관계', validators=[DataRequired('관계는 필수입력 항목입니다.')])
    file_data = FileField('사진')


class AnswerForm(FlaskForm):
    content = TextAreaField('내용', validators=[DataRequired('내용은 필수입력 항목입니다.')])


class UserCreateForm(FlaskForm):
    username = StringField('사용자이름', validators=[DataRequired('이름은 필수입력 항목입니다.'), Length(min=2, max=25)])
    password1 = PasswordField('비밀번호', validators=[
        DataRequired('비밀번호는 필수입력 항목입니다.'), EqualTo('password2', '비밀번호가 일치하지 않습니다')])
    password2 = PasswordField('비밀번호확인', validators=[DataRequired('비밀번호 확인은 필수입력 항목입니다.')])
    email = EmailField('이메일', validators=[DataRequired('이메일은 필수 입력 항목입니다.'), Email()])


class UserLoginForm(FlaskForm):
    email = EmailField('이메일', validators=[DataRequired('이메일은 필수 입력 항목입니다.'), Email()])
    password = PasswordField('비밀번호', validators=[DataRequired('비밀번호는 필수입력 항목입니다.')])


class ChumoForm(FlaskForm):
    name = TextAreaField('이름', validators=[DataRequired('이름은 필수입력 항목입니다.')])
    birth = TextAreaField('생년월일', validators=[DataRequired('생년월일은 필수입력 항목입니다.')])
    death = TextAreaField('기일', validators=[DataRequired('기일은 필수입력 항목입니다.')])
    profile_data = FileField('사진')
    content = TextAreaField('메인 메세지')
