from werkzeug.security import safe_str_cmp
from models.user import UserModel


def authenticate(username, password):
    user = UserModel.find_by_username(username)
    if user and safe_str_cmp(user.password, password):
        return user

def identity(payload):  #once a jwt is obtained, then in next sent it in next request to identity
    user_id = payload['identity']
    return UserModel.find_by_id(user_id)