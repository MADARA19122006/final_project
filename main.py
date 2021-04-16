from flask import Flask, render_template, redirect
from flask_restful import Api
from flask_login import LoginManager, login_required, logout_user, login_user

from data import db_session
from data.availability import Availability
from data.booking import Booking
from data.guests import Guests
from data.rooms import Rooms
from forms.choice_room import RoomForm
from forms.date_choice import DateForm
from forms.login_form import LoginForm
from forms.register_form import RegisterForm
import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
api = Api(app)
login_manager = LoginManager()
login_manager.init_app(app)


def main():
    db_session.global_init("db/final_project.db")
    app.run()


@app.route("/")
def main_page():
    return render_template("base.html", title='awgwagrg')


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(Guests).get(user_id)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(Guests).filter(Guests.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form, message="Такой пользователь уже есть")
        guests = Guests(
            name=form.name.data,
            surname=form.surname.data,
            email=form.email.data,
            phone=form.phone.data)
        guests.set_password(form.password.data)
        db_sess.add(guests)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(Guests).filter(Guests.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/booking', methods=['GET', 'POST'])
def booking():
    form = DateForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        rooms = db_sess.query(Availability).filter(Availability.date >= form.check_in.data,
                                                   Availability.date < form.check_out.data).all()

        room_list = {}
        for i in rooms:
            if i.room in room_list:
                if i.quantity_rooms < room_list[i.room]:
                    room_list[i.room] = i.quantity_rooms
            else:
                room_list[i.room] = i.quantity_rooms
        room_nlist = []
        for room_id, qty in room_list.items():
            if qty > 0:
                room_type = db_sess.query(Rooms).get(room_id)
                room_nlist.append(
                    {'name': room_type.name_room, 'description': room_type.description, 'qty': qty})

        frm = RoomForm(data={'rooms': [0] * len(room_nlist)})
        print(frm.rooms)
        for el in zip(room_nlist, frm.rooms):
            el[1].choices = list(range(el[0]['qty'] + 1))
        return render_template('room_choice.html', title='Выбор номеров', room_nlist=room_nlist, form=frm, n=len(room_nlist))
    return render_template('date_choice.html', title='Поиск номеров', form=form)


@app.route('/testform', methods=['GET', 'POST'])
def testform():
    form = RoomForm(data={'rooms': [0] * 3})
    print(form.rooms)
    available = [3, 4, 5, 1, 7]
    for n, el in enumerate(form.rooms):
        el.choices = list(range(available[n] + 1))
    if form.validate_on_submit():
        pass
    return render_template('testform.html', title='Dynamic form 1', form=form)


@app.route('/admin/allbookings')
def allbookings():
    db_sess = db_session.create_session()
    booking = db_sess.query(Booking).filter(Booking.check_in >= datetime.date.today())
    return render_template("table_booking.html", booking=booking)


if __name__ == '__main__':
    main()
