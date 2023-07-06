import requests
# from config1 import CLIENT_ID, CLIENT_SECRET, REDIRECT_URI


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
            url=self.auth_server % "/oauth/token", 
            headers=self.default_header,
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
            #"property_keys":'["kakao_account.profile_image_url"]'
            data={}
        ).json()