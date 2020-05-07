import os
from flask import Flask, request
from flask import render_template
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from flask_restful import abort
from flask_wtf import FlaskForm
from werkzeug.utils import redirect
from wtforms import PasswordField, SubmitField, StringField, BooleanField, TextAreaField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired
from data import db_session
from data.users import User
from data.movies import Movie


app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'

login_manager = LoginManager()
login_manager.init_app(app)


class RegisterForm(FlaskForm):
    email = EmailField('Почта', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    password_again = PasswordField('Повторите пароль', validators=[DataRequired()])
    name = StringField('Имя пользователя', validators=[DataRequired()])
    submit = SubmitField('Войти')


class LoginForm(FlaskForm):
    email = EmailField('Почта', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')


class FilmForm(FlaskForm):
    name = StringField('Название', validators=[DataRequired()])
    genre = StringField('Жанр')
    year = StringField('Год выхода')
    duration = StringField('Длительность')
    watched = BooleanField("Просмотрен")
    timecode = StringField('Время на котором вы остановились')
    review = TextAreaField('Содержание')
    submit = SubmitField('Применить')


def main():
    db_session.global_init("db/blogs.sqlite")
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)


@login_manager.user_loader
def load_user(user_id):
    session = db_session.create_session()
    return session.query(User).get(user_id)


@app.route("/")
def index():
    session = db_session.create_session()
    movies = session.query(Movie).filter(Movie.id <= 5)
    return render_template("hello.html", movies=movies, title='PlanVid')


@app.route("/home")
def home():
    session = db_session.create_session()
    movies = session.query(Movie).filter(Movie.user == current_user)
    return render_template("home.html", movies=movies, title='Домашняя страница')


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        session = db_session.create_session()
        if session.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User()
        user.name = form.name.data
        user.email = form.email.data
        user.set_password(form.password.data)
        session.add(user)
        session.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        session = db_session.create_session()
        user = session.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/home")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route('/film',  methods=['GET', 'POST'])
@login_required
def add_news():
    form = FilmForm()
    if form.validate_on_submit():
        session = db_session.create_session()
        film = Movie()
        film.name = form.name.data
        film.genre = form.genre.data
        film.year = form.year.data
        film.duration = form.duration.data
        film.watched = form.watched.data
        film.timecode = form.timecode.data
        film.review = form.review.data
        current_user.movie.append(film)
        session.merge(current_user)
        session.commit()
        return redirect('/home')
    return render_template('movie.html', title='Добавление фильма',
                           form=form)


@app.route('/film/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_film(id):
    form = FilmForm()
    if request.method == "GET":
        session = db_session.create_session()
        film = session.query(Movie).filter(Movie.id == id,
                                           Movie.user == current_user).first()
        if film:
            form.name.data = film.name
            form.genre.data = film.genre
            form.year.data = film.year
            form.duration.data = film.duration
            form.watched.data = film.watched
            form.timecode.data = film.timecode
        else:
            abort(404)
    if form.validate_on_submit():
        session = db_session.create_session()
        film = session.query(Movie).filter(Movie.id == id,
                                           Movie.user == current_user).first()
        if film:
            film.name = form.name.data
            film.genre = form.genre.data
            film.year = form.year.data
            film.duration = form.duration.data
            film.watched = form.watched.data
            film.timecode = form.timecode.data
            session.commit()
            return redirect('/home')
        else:
            abort(404)
    return render_template('movie.html', title='Редактирование новости', form=form)


@app.route('/film_delete/<int:id>', methods=['GET', 'POST'])
@login_required
def film_delete(id):
    session = db_session.create_session()
    film = session.query(Movie).filter(Movie.id == id,
                                       Movie.user == current_user).first()
    if film:
        session.delete(film)
        session.commit()
    else:
        abort(404)
    return redirect('/home')


if __name__ == '__main__':
    main()
