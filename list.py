from flask import request
from flask_wtf import FlaskForm

from DB import DB, UserModel


class ListForm(FlaskForm):
    print("list")
