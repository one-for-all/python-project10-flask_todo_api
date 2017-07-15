from flask_httpauth import HTTPBasicAuth
from flask import g
import models

basic_auth = HTTPBasicAuth()
auth = basic_auth


@basic_auth.verify_password
def verify_password(username, password):
    try:
        user = models.User.select().where(models.User.username ==
                                          username).get()
        if not user.verify_password(password):
            return False
    except models.DoesNotExist:
        return False
    else:
        g.user = user
        return True