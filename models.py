import datetime

from argon2 import PasswordHasher
from itsdangerous import (TimedJSONWebSignatureSerializer as Serializer,
                          BadSignature, SignatureExpired)
from peewee import *

import config


HASHER = PasswordHasher()

DATABASE = SqliteDatabase('todos.sqlite')


class User(Model):
    username = CharField(unique=True)
    email = CharField(unique=True)
    password = CharField()

    class Meta:
        database = DATABASE

    @classmethod
    def create_user(cls, username, email, password):
        user = cls.create(
            username=username,
            email=email,
            password=cls.set_password(password)
        )
        return user

    @staticmethod
    def set_password(password):
        return HASHER.hash(password)

    def verify_password(self, password):
        return HASHER.verify(self.password, password)


class Todo(Model):
    name = CharField()
    created_at = DateTimeField(default=datetime.datetime.now)
    created_by = ForeignKeyField(User)

    class Meta:
        database = DATABASE


def initialize():
    DATABASE.connect()
    DATABASE.create_tables([User, Todo], safe=True)
    DATABASE.close()
