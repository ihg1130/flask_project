from flask import Flask, Blueprint, url_for, render_template, flash, request, session, g, Flask, redirect, current_app
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
import config

# from config1 import CLIENT_ID, REDIRECT_URI
# from controller import Oauth
# from model import UserModel, UserData

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
      return render_template("index.html")

@bp.route('/memorial')
def memorial():
      return render_template("memorial.html")

@bp.route('/1')
def index1():
      return redirect(url_for('question._list'))

# @bp.route('/')
# def home():
#     return render_template("APIExamNaverLogin.html")
 
@bp.route('/naverlogin')
def login():
    return render_template("callback.html")

# @bp.route('/3')
# def home():
#     return render_template("kakao.html")



# @bp.route("/oauth")
# def oauth_api():
#     create_app()
# #     """
# #     # OAuth API [GET]
# #     사용자로부터 authorization code를 인자로 받은 후,
# #     아래의 과정 수행함
# #     1. 전달받은 authorization code를 통해서
# #         access_token, refresh_token을 발급.
# #     2. access_token을 이용해서, Kakao에서 사용자 식별 정보 획득
# #     3. 해당 식별 정보를 서비스 DB에 저장 (회원가입)
# #     3-1. 만약 이미 있을 경우, (3) 과정 스킵
# #     4. 사용자 식별 id를 바탕으로 서비스 전용 access_token 생성
# #     """
#     code = str(request.args.get('code'))
    
#     oauth = Oauth()
#     auth_info = oauth.auth(code)
#     user = oauth.userinfo("Bearer " + auth_info['access_token'])
    
#     user = UserData(user)
#     UserModel().upsert_user(user)


#     resp = make_response(render_template('index.html'))
#     access_token = create_access_token(identity=user.id)
#     refresh_token = create_refresh_token(identity=user.id)
#     resp.set_cookie("logined", "true")
#     set_access_cookies(resp, access_token)
#     set_refresh_cookies(resp, refresh_token)

#     return resp


# @bp.route('/token/refresh')
# @jwt_required
# def token_refresh_api():
#     """
#     Refresh Token을 이용한 Access Token 재발급
#     """
#     user_id = get_jwt_identity()
#     resp = jsonify({'result': True})
#     access_token = create_access_token(identity=user_id)
#     set_access_cookies(resp, access_token)
#     return resp


# @bp.route('/token/remove')
# def token_remove_api():
#     """
#     Cookie에 등록된 Token 제거
#     """
#     resp = jsonify({'result': True})
#     unset_jwt_cookies(resp)
#     resp.delete_cookie('logined')
#     return resp


# # @bp.route("/userinfo")
# # @jwt_required
# # def userinfo():
# #      """
# #      Access Token을 이용한 DB에 저장된 사용자 정보 가져오기
# #      """
# #      user_id = get_jwt_identity()
# #      userinfo = UserModel().get_user(user_id).serialize()
# #      return jsonify(userinfo)


# @bp.route('/oauth/url')
# def oauth_url_api():
#     """
#     Kakao OAuth URL 가져오기
#     """
#     return jsonify(
#         kakao_oauth_url="https://kauth.kakao.com/oauth/authorize?client_id=%s&redirect_uri=%s&response_type=code" \
#         % ("6925e2e950e402e6d1d144af81ee1292","http://localhost:5000/oauth")
#     )


# @bp.route("/oauth/refresh", methods=['POST'])
# def oauth_refesh_api():
#     """
#     # OAuth Refresh API
#     refresh token을 인자로 받은 후,
#     kakao에서 access_token 및 refresh_token을 재발급.
#     (% refresh token의 경우, 
#     유효기간이 1달 이상일 경우 결과에서 제외됨)
#     """
#     refresh_token = request.get_json()['refresh_token']
#     result = Oauth().refresh(refresh_token)
#     return jsonify(result)


# @bp.route("/oauth/userinfo", methods=['POST'])
# def oauth_userinfo_api():
#     """
#     # OAuth Userinfo API
#     kakao access token을 인자로 받은 후,
#     kakao에서 해당 유저의 실제 Userinfo를 가져옴
#     """
#     access_token = request.get_json()['access_token']
#     result = Oauth().userinfo("Bearer " + access_token)
#     return jsonify(result)

