from flask import Flask, Blueprint, current_app, url_for, render_template, flash, request, session, g, Flask, redirect, current_app
from pybo.models import Question
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import redirect
from flask_mail import Mail, Message
from flask import render_template, request, jsonify, make_response
from flask_jwt_extended import (
    JWTManager, create_access_token, 
    get_jwt_identity, jwt_required,
    set_access_cookies, set_refresh_cookies, 
    unset_jwt_cookies, create_refresh_token,
    jwt_required,
)
from pybo.__init__ import create_app
import requests
from tinydb import TinyDB, Query
from pybo import db
from pybo.forms import UserCreateForm, UserLoginForm, QuestionForm
from pybo.models import User, Question

import functools


bp = Blueprint('main', __name__, url_prefix='/')

class UserModel:

    def __init__(self, path='db.json'):
        self.db = TinyDB(path)

    def upsert_user(self, user):
        if not self.db.search(Query().id == user.id):
            self.db.insert(user.serialize())

    def get_user(self, user_id):
        user = self.db.search(Query().id == user_id)
        return UserData.deserialize(user[0])

    def remove_user(self, user_id):
        self.db.remove(Query().id == user_id)


class UserData:
    
    def __init__(self, user=None):
        if user:
            user_info = user['kakao_account']['profile']
            self.id = user['id']
            self.nickname = user_info['nickname']
            self.profile = user_info['profile_image_url'] 
            self.thumbnail = user_info['thumbnail_image_url']
        else:
            self.id = None
            self.nickname = None
            self.profile = None
            self.thumbnail = None

    def __str__(self):
        return "<UserData>(id:%s, nickname:%s)" \
                % (self.id, self.nickname)

    def serialize(self):
        return {
            "id": self.id,
            "nickname": self.nickname,
            "profile": self.profile,
            "thumbnail": self.thumbnail
        }

    @staticmethod
    def deserialize(user_data):
        user = UserData()
        user.id = user_data['id']
        user.nickname = user_data['nickname']
        user.profile = user_data['profile']
        user.thumbnail = user_data['thumbnail']
        return user
    

class Oauth:
    
    def __init__(self):
        self.auth_server = "https://kauth.kakao.com%s"
        self.api_server = "https://kapi.kakao.com%s"
        self.default_header = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Cache-Control": "no-cache",
        }

    def auth(self, code):
        return requests.post(
            url="https://kauth.kakao.com/oauth/token", 
            headers={
            "Content-Type": "application/x-www-form-urlencoded",
            "Cache-Control": "no-cache",
        },
            data={
                "grant_type": "authorization_code",
                "client_id": "6925e2e950e402e6d1d144af81ee1292",
                "client_secret": "MGFMXFDJnsuFW4c8azm0dXXkX1N93H3w",
                "redirect_uri": "http://localhost:5000/oauth",
                "code": code,
            }, 
        ).json()


    def refresh(self, refresh_token):
        return requests.post(
            url=self.auth_server % "/oauth/token", 
            headers=self.default_header,
            data={
                "grant_type": "refresh_token",
                "client_id": "6925e2e950e402e6d1d144af81ee1292",
                "client_secret": "MGFMXFDJnsuFW4c8azm0dXXkX1N93H3w",
                "refresh_token": refresh_token,
            }, 
        ).json()


    def userinfo(self, bearer_token):
        return requests.post(
            url=self.api_server % "/v2/user/me", 
            headers={
                **self.default_header,
                **{"Authorization": bearer_token}
            },
            # "property_keys":'["kakao_account.profile_image_url"]'
            data={}
        ).json()

@bp.route('/')
def index():
      current_app.logger.info("INFO 레벨로 출력")
      return render_template("index.html")

@bp.route('/memorial')
def memorial():
      return render_template("memorial.html")

@bp.route('/1')
def index1():
      return redirect(url_for('question._list'))

@bp.route('/naverlogin')
def login():
    return render_template("callback.html")

