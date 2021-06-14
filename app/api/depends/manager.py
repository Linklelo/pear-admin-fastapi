from fastapi_login import LoginManager
from fastapi_sqlalchemy import db
from app.models.admin import User
from app.core.config import SECRET_KEY
from app.api.errors.notauth_error import NotAuthenticatedException

manager = LoginManager(SECRET_KEY, token_url='/admin/login', use_cookie=True)
manager.not_authenticated_exception = NotAuthenticatedException


@manager.user_loader
def load_user(username: str):  # could also be an asynchronous function
    user = db.session.query(User).filter_by(username=username).first()
    return user