from flask import Flask, render_template, redirect, request, make_response, session, jsonify, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, InputRequired, Length
from flask_login import login_required, logout_user, current_user, LoginManager, login_user
from flask_mail import Mail, Message

from data import db_session
from data.models import User, Detection

import datetime


app = Flask(__name__)
app.config['SECRET_KEY'] = 'you-will-never-guess'
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 100
app.config['PERMANENT_SESSION_LIFETIME'] = datetime.timedelta(days=10)
app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'virus.self.isolation@gmail.com'
app.config['MAIL_DEFAULT_SENDER'] = 'virus.self.isolation@gmail.com'
app.config['MAIL_PASSWORD'] = 'V!13wirM_TR'

login_manager = LoginManager()
login_manager.init_app(app)


class LoginForm(FlaskForm):
    mail = StringField('Почта',
                       validators=[InputRequired("Необходимо ввести email")])
    name = StringField('Имя',
                           validators=[InputRequired("Необходимо ввести имя")])
    surname = StringField('Фамилия',
                           validators=[InputRequired("Необходимо ввести фамилию")])
    password = PasswordField('Пароль',
                             validators=[InputRequired("Необходимо ввести пароль"),
                                         Length(min=9, message='Пароль должен содержать больше 8 символов')])
    remember_me = BooleanField('Запомнить меня')
    submit_res = SubmitField('Зарегистрироваться')
    submit_sign = SubmitField('Войдите')


@login_manager.user_loader
def load_user(user_id):
    session = db_session.create_session()
    return session.query(User).get(user_id)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        print(form.submit_res.data)
        print(form.submit_sign.data)
        if form.submit_res.data:
            session = db_session.create_session()
            if session.query(User).filter(User.email == form.mail.data).first():
                return render_template("login.html", form=form,
                                       message="Пользователь с таким email уже есть")
            user = User()
            user.name = form.name.data
            user.surname = form.surname.data
            user.email = form.mail.data
            user.set_password(form.password.data)

            session.add(user)
            session.commit()

            #login_user(user)

            return redirect(url_for('.check', user=user))

        elif form.submit_sign.data:
            pass
    return render_template('login.html', form=form)


@app.route('/check', methods=['GET', 'POST'])
def check(user):
    session = db_session.create_session()
    print(current_user.get_id())
    return str(current_user)


@app.route('/sign_in', methods=['GET', 'POST'])
def sign_in():
    pass


@login_manager.user_loader
def load_user(user_id):
    session = db_session.create_session()
    return session.query(User).get(user_id)


def main():
    db_session.global_init("test.sqlite")
    app.run(host='127.0.0.1', port=8080)


if __name__ == '__main__':
    main()