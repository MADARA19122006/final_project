import json

from flask import Flask, render_template, redirect, request, session, url_for
from flask_restful import Api, abort
from flask_login import LoginManager, login_required, logout_user, login_user, current_user
from sqlalchemy import func

from data import db_session, api_availability, api_booking, api_bot
from data.availability import Availability
from data.booking import Booking
from data.guests import Guests
from data.rooms import Rooms
from forms.admin_form import AdminForm
from forms.choice_room import RoomForm
from forms.date_choice import DateForm
from forms.edit import EditForm
from forms.login_form import LoginForm
from forms.register_form import RegisterForm
import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
app.config['PERMANENT_SESSION_LIFETIME'] = datetime.timedelta(minutes=15)
api = Api(app)
login_manager = LoginManager()
login_manager.init_app(app)


def availroom(room_id, checkin, checkout):
    db_sess = db_session.create_session()
    return db_sess.query(func.min(Availability.quantity_rooms)).filter(Availability.room == room_id,
                                                                       Availability.date >= checkin,
                                                                       Availability.date < checkout).scalar()


def main():
    db_session.global_init("db/final_project.db")
    api.add_resource(api_availability.AvailabilityAdd, '/api/availability')
    api.add_resource(api_booking.BookingGet, '/api/booking_get')
    api.add_resource(api_bot.Bot, '/api/bot')
    app.run()


@app.route("/")
def main_page():
    return redirect("/booking")


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
@app.route('/register/<redir>', methods=['GET', 'POST'])
def reqister(redir=None):
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
        newguest = Guests(
            name=form.name.data,
            surname=form.surname.data,
            email=form.email.data,
            phone=form.phone.data)
        newguest.set_password(form.password.data)
        db_sess.add(newguest)
        db_sess.commit()
        login_user(newguest, remember=True)
        if redir:
            return redirect(url_for(redir))
        else:
            return redirect("/booking")
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/login', methods=['GET', 'POST'])
@app.route('/login/<redir>', methods=['GET', 'POST'])
def login(redir=None):
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(Guests).filter(Guests.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            if redir:
                return redirect(url_for(redir))
            else:
                return redirect("/booking")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/booking', methods=['GET', 'POST'])
@app.route('/booking/', methods=['GET', 'POST'])
def booking():
    form = DateForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()

        rooms = {}

        for i in db_sess.query(Availability).filter(Availability.date >= form.check_in.data,
                                                    Availability.date < form.check_out.data).all():
            if i.room in rooms:
                rooms[i.room]['price'] += i.price
                if i.quantity_rooms < rooms[i.room]['qty']:
                    rooms[i.room]['qty'] = i.quantity_rooms
            else:
                rooms[i.room] = {'name': i.rooms.name_room, 'description': i.rooms.description,
                                 'qty': i.quantity_rooms, 'price': i.price}

        params = json.dumps({'rooms': rooms, 'checkin': form.check_in.data.strftime('%Y%m%d'),
                             'checkout': form.check_out.data.strftime('%Y%m%d')})
        session['params'] = params
        session['csrf_tokens'] = json.dumps(
            {'csrf_tokens': []})  # для защиты от повторной отправки формы
        # return redirect(url_for('booking2', params=params))
        return redirect(url_for('booking2'))

    return render_template('date_choice.html', title='Поиск номеров', form=form)


@app.route('/booking/step2', methods=['GET', 'POST'])
def booking2():
    params = json.loads(session['params'])
    checkin = datetime.datetime.strptime(params['checkin'], '%Y%m%d').date()
    checkout = datetime.datetime.strptime(params['checkout'], '%Y%m%d').date()
    rooms = params['rooms']
    room_nlist = []
    for key, value in rooms.items():
        if value['qty'] > 0:
            value['id'] = key
            room_nlist.append(value)
    data = {'rooms': [0] * len(room_nlist), 'ids': [el['id'] for el in room_nlist],
            'price': [el['price'] for el in room_nlist]}
    form = RoomForm(data=data)
    if form.validate_on_submit():
        csrf_tokens = json.loads(session['csrf_tokens'])['csrf_tokens']
        if form.csrf_token.data not in csrf_tokens:  # защита от повторной отправки формы
            csrf_tokens.append(form.csrf_token.data)
            session['csrf_tokens'] = json.dumps({'csrf_tokens': csrf_tokens})
            print(form.data)
            print(session['csrf_tokens'])

            bookingdata = []  # format [[qty, room id, room name, price],...]
            db_sess = db_session.create_session()
            for i in range(len(form.rooms)):
                qty = int(form.rooms[i].data)
                if qty:
                    ids = int(form.ids[i].data)
                    if qty > availroom(ids, checkin, checkout):
                        return '<h1>Ой! Похоже, вы не успели, эти номера' \
                               ' уже забронированы! Попробуйте повторить бронирование.</h1>'
                    bookingdata.append(
                        [qty, ids, db_sess.query(Rooms).get(ids).name_room, int(form.price[i].data)])
            if not bookingdata:
                return '<h1>Не выбрано ни одного номера!</h1>'
            booknumber = db_sess.query(func.max(Booking.number_booking)).scalar() + 1
            total = 0
            for el in bookingdata:
                total += el[3]
                for entry in db_sess.query(Availability).filter(Availability.date >= checkin,
                                                                Availability.date < checkout,
                                                                Availability.room == el[1]):
                    entry.quantity_rooms -= el[0]

                newbooking = Booking(
                    room=el[1],
                    guest=current_user.id,
                    check_in=checkin,
                    check_out=checkout,
                    quantity=el[0],
                    status=True,
                    number_booking=booknumber,
                    price=el[3]
                )
                db_sess.add(newbooking)
                db_sess.commit()

            return render_template('success.html', title='Success!', bookingdata=bookingdata,
                                   checkin=checkin,
                                   checkout=checkout, total=total, booknumber=booknumber)
        else:
            return redirect('/booking')

    for el in zip(room_nlist, form.rooms):
        el[1].choices = list(range(min(el[0]['qty'] + 1, 6)))
    return render_template('room_choice.html', title='Выбор номеров', room_nlist=room_nlist,
                           form=form, n=len(room_nlist), checkin=checkin, checkout=checkout)


@login_required
@app.route('/admin/allbookings', methods=['GET', 'POST'])
def allbookings():
    if current_user.is_admin:
        form = AdminForm(data={'check_in_from': datetime.date.today()})
        if request.method == 'POST':
            if form.check_in_from.data:
                check_in_from = form.check_in_from.data
            else:
                check_in_from = datetime.date(1900, 1, 1)
            if form.check_in_to.data:
                check_in_to = form.check_in_to.data
            else:
                check_in_to = datetime.date(2100, 1, 1)
            if form.check_out_from.data:
                check_out_from = form.check_out_from.data
            else:
                check_out_from = datetime.date(1900, 1, 1)
            if form.check_out_to.data:
                check_out_to = form.check_out_to.data
            else:
                check_out_to = datetime.date(2100, 1, 1)
            if form.number_booking.data:
                db_sess = db_session.create_session()
                booking = db_sess.query(Booking).filter(
                    Booking.number_booking == form.number_booking.data)
                return render_template("admin.html", booking=booking, form=form)
            else:
                db_sess = db_session.create_session()
                booking = db_sess.query(Booking).filter(Booking.check_in >= check_in_from,
                                                        Booking.check_in <= check_in_to,
                                                        Booking.check_out >= check_out_from,
                                                        Booking.check_out <= check_out_to)
                return render_template("admin.html", booking=booking, form=form)
        db_sess = db_session.create_session()
        booking = db_sess.query(Booking).filter(Booking.check_in >= datetime.date.today())
        return render_template("admin.html", booking=booking, form=form)


@login_required
@app.route('/cancel/<n>', methods=['GET', 'POST'])
def canceled(n):
    db_sess = db_session.create_session()
    booking = db_sess.query(Booking).filter(Booking.number_booking == n).first()
    if booking:
        if current_user == booking.guests:
            booklist = db_sess.query(Booking).filter(Booking.number_booking == n)
            for el in booklist:
                el.status = False
            db_sess.commit()
            return render_template("delete.html", x=booklist)


@login_required
@app.route('/overview/', methods=['GET', 'POST'])
@app.route('/overview/<date>', methods=['GET', 'POST'])
def overview(date=None):
    if current_user.is_admin:
        if not date:
            date = datetime.date.today()
        else:
            date = datetime.datetime.strptime(date, '%Y%m%d').date()
        datebkw = date - datetime.timedelta(days=14)
        datefwd = date + datetime.timedelta(days=14)
        db_sess = db_session.create_session()
        availability = db_sess.query(Availability).filter(Availability.date >= date,
                                                          Availability.date < datefwd).order_by(
            Availability.date)
        s = {}
        for i in availability:
            if i.rooms.code not in s:
                s[i.rooms.code] = [[i.date, i.quantity_rooms, i.price]]
            else:
                s[i.rooms.code].append([i.date, i.quantity_rooms, i.price])
        m = []
        for i in range(14):
            m.append(date + datetime.timedelta(days=i))
        return render_template("overview.html", s=s, date=m, datebkw=datebkw.strftime('%Y%m%d'),
                               datefwd=datefwd.strftime('%Y%m%d'))


@login_required
@app.route('/edit/<date>/<code>', methods=['GET', 'POST'])
def editday(date, code):
    if current_user.is_admin:
        form = EditForm()
        if request.method == "GET":
            db_sess = db_session.create_session()
            room_id = db_sess.query(Rooms).filter(Rooms.code == code).first().id
            edit = db_sess.query(Availability).filter(Availability.room == room_id,
                                                      Availability.date == date).first()
            if edit:
                form.quantity.data = edit.quantity_rooms
                form.price.data = edit.price
            else:
                abort(404)
        if form.validate_on_submit():
            db_sess = db_session.create_session()
            room_id = db_sess.query(Rooms).filter(Rooms.code == code).first().id
            edit = db_sess.query(Availability).filter(Availability.room == room_id,
                                                      Availability.date == date).first()
            if edit:
                edit.quantity_rooms = form.quantity.data
                edit.price = form.price.data
                db_sess.commit()
                return redirect('/overview')
            else:
                abort(404)
        return render_template('edit.html', title='Редактирование', form=form, code=code, date=date)


if __name__ == '__main__':
    main()
