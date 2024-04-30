from flask import Flask, render_template, flash, request
import os

from werkzeug.utils import redirect

from DB import DB, UserModel, BookModel
from Server.templates.list import ListForm
from Server.templates.login import LoginForm

app = Flask(__name__)

db = DB()
books = BookModel(db.get_connection())
users = UserModel(db.get_connection())


@app.route('/')
@app.route('/index')
def index():
    return "Привет, Яндекс!"


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested for user {}, remember_me={}'.format(
            form.username.data, form.remember_me.data))
        dbData = users.select("name", form.username.data)
        if len(dbData) and dbData[0][2] == format(form.password.data):
            # return render_template('list.html', title='Books list', form=form)
            return redirect('/list?name={0}&isAdmin={1}'.format(dbData[0][1], dbData[0][3]))
    return render_template('login.html', title='Sign In', form=form)


@app.route('/list', methods=['GET', 'POST'])
def list():
    nameStr = request.args.get('name')
    isAdminStr = request.args.get('isAdmin')
    isAdmin = False
    if isAdminStr == '1' or isAdminStr=='True':
        isAdmin = True
    form = ListForm()
    return render_template('list.html', title='Books list', books=books.select(),headers=books.columnNames, name=nameStr, isAdmin=isAdmin,
                           form=form)


@app.route('/delete', methods=['GET', 'POST'])
def delete():
    idStr = request.args.get('id')
    books.delete("id", idStr)
    nameStr = request.args.get('name')
    isAdminStr = request.args.get('isAdmin')
    isAdmin = False
    if isAdminStr == '1':
        isAdmin = True
    form = ListForm()
    return redirect('/list?name={0}&isAdmin={1}'.format(nameStr, isAdminStr))

    return render_template('list.html', title='Books list', books=books.select(),headers=books.columnNames, name=nameStr, isAdmin=isAdmin,
                           form=form)


if __name__ == '__main__':
    users.insert(["admin", "12345678", "1"])
    users.insert(["student", "12345678", "0"])
    books.insert(["Книга Властелин колец 1", "lol", "https://knijky.ru/books/vlastelin-kolec-bratstvo-kolca"])
    books.insert(["Книга Властелин колец 2", "lol", "https://knijky.ru/books/vlastelin-kolec-dve-kreposti"])
    books.insert(["Книга Властелин колец 3", "lol", "https://knijky.ru/books/vlastelin-kolec-vozvrashchenie-korolya"])
    SECRET_KEY = os.urandom(32)
    app.config['SECRET_KEY'] = SECRET_KEY
    app.run(debug=True, port=8080, host='127.0.0.1')
