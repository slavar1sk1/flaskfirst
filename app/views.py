from flask import render_template, request, redirect, url_for, session, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from .config import app
from .forms import Form, Registration, Login
from flask_login import UserMixin, LoginManager, login_user, logout_user, current_user, login_required
from os.path import join
from flask import current_app
from sqlalchemy.exc import IntegrityError
from werkzeug.security import check_password_hash, generate_password_hash
from flask_session import Session
from flask_caching import Cache
from sqlalchemy.exc import IntegrityError

cache = Cache(app)

db = SQLAlchemy(app)
migrate = Migrate(app, db)


login = LoginManager(app)
login.login_view = 'log_in'

count_services = 0
price_counter = 0
services_id = []

Session(app)


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False, unique=True)

    def hash_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)


class Service(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False, unique=True)
    intro = db.Column(db.String(100), nullable=False)
    text = db.Column(db.Text, nullable=False)
    catalog = db.Column(db.String, nullable=False)
    price = db.Column(db.Integer, nullable=False)
    img = db.Column(db.String)


class Connect(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)
    connect = db.Column(db.Integer, db.ForeignKey('user.id'))


@login.user_loader
def login(id):
    return User.query.get(id)


@app.route('/autorization', methods=['GET', 'POST'])
def log_in():
    form = Login()
    print('aaa')
    if form.validate_on_submit():
        print('ok')
        password = form.password.data
        username = form.username.data

        cache.set('username', username)
        cache.get('username')

        user = User.query.filter_by(username=username).first()
        if not user or not user.check_password(password):
            return render_template('login.html', message='1', form=form)
        else:
            login_user(user, remember=form.remember_me.data)
            return redirect('/')
    return render_template('login.html', form=form)


@app.route('/')
@login_required
def home():
    global count_services, price_counter

    return render_template('home.html', session=session, current_user=current_user)


@app.route('/make_service', methods=['GET', 'POST'])
def make_service():
    form = Form()
    print(form.errors)
    if request.method == 'POST':
        title = request.form['title']
        intro = request.form['intro']
        text = request.form['text']
        img = request.files['img']
        catalog = request.form['catalog']
        price = request.form['price']

        service = Service(title=title, intro=intro, text=text, catalog=catalog, price=price, img=img.filename)
        img.save(join(current_app.root_path, 'static', img.filename))
        try:
            db.session.add(service)
            db.session.commit()

        except IntegrityError:
            db.session.rollback()

            return {'error': 'Обьявление с таким заголовком уже существует!',
                    'success': False}
        return {'confirm': 'Успешно добавлен товар',
                'success': True}
    else:
        return render_template('make_service.html', form=form)







@app.route('/games_service')
def games_service():
    global count_services, price_counter
    data = Service.query.all()
    db.session.commit()

    game_service_list = [service for service in data if service.catalog == 'option1']

    if not session.get('counter'):
        print('ok')
        session['counter'] = '0'

    if not session.get('price_counter'):
        print('neok')
        session['price_counter'] = '0'

    if not session.get('services_id'):
        print('oki')
        session['services_id'] = []

    return render_template('games.html', game_list=game_service_list,
                           session=session, current_user=current_user)


@app.route('/programming_service')
def programming_service():
    global count_services, price_counter
    data = Service.query.all()
    db.session.commit()
    programming_service_list = [service for service in data if service.catalog == 'option2']

    if not session.get('counter'):
        print('ok')
        session['counter'] = '0'

    if not session.get('price_counter'):
        print('neok')
        session['price_counter'] = '0'

    if not session.get('services_id'):
        session['services_id'] = []

    return render_template('programming.html', programming_list=programming_service_list,
                           session=session, current_user=current_user)


@app.route('/programming_service/<int:id>')
def programming_detail(id):
    service = Service.query.get(id)

    return render_template('programming_detail.html', service=service, current_user=current_user)


@app.route('/games_service/<int:id>')
def games_detail(id):
    service = Service.query.get(id)

    return render_template('games_detail.html', service=service, current_user=current_user)


@app.route('/registration', methods=['GET', 'POST'])
def registration():
    form = Registration()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        email = form.email.data

        reg = User(username=username, email=email)
        reg.hash_password(password)
        try:

            db.session.add(reg)
            db.session.commit()
            login_user(reg, remember=True)
        except IntegrityError:
            db.session.rollback()
            return render_template('registration.html', message='1', form=form)
        return redirect('/')

    return render_template('registration.html', form=form)


@app.route('/add_to_pcart/<int:service_id>', methods=['POST'])
def add_to_pcart(service_id):
    if request.method == 'POST':
        service_info = Service.query.get(service_id)
        service_price = service_info.price
        print(service_price)

        if not session.get('counter'):
            session['counter'] = 1
        else:
            if service_id not in session.get('services_id'):
                session['counter'] = int(session['counter'])
                session['counter'] += 1

        if not session.get('price_counter'):
            session['price_counter'] = service_price
        else:
            if service_id not in session.get('services_id'):
                session['price_counter'] = int(session['price_counter'])
                session['price_counter'] += service_price

        if not session.get('services_id'):
            session['services_id'] = [service_id]
            print('imba')
        else:
            if service_id not in session.get('services_id'):
                session.get('services_id').append(service_id)



        return jsonify({
            'success': True,
            'counter': session.get('counter'),
            'price_counter': session.get('price_counter')

        })
    else:
        return jsonify({'error': 'Метод не разрешен'}), 405


@app.route('/add_to_gcart/<int:service_id>')
def add_to_gcart(service_id):

    if request.method == 'POST':

        if not session.get('services_id'):
            session['services_id'] = []
            print('imba')
        else:
            print('neimba')
            session.get('services_id').append(service_id)

        service_info = Service.query.get(service_id)
        service_price = service_info.price
        print(service_price)

        if not session.get('counter'):
            session['counter'] = 0
        else:
            session['counter'] = int(session['counter'])
            session['counter'] += 1

        if not session.get('price_counter'):
            session['price_counter'] = 0
        else:
            session['price_counter'] = int(session['price_counter'])
            session['price_counter'] += service_price

        return jsonify({
            'success': True,
            'counter': session.get('counter'),
            'price_counter': session.get('price_counter')

        })
    else:
        return jsonify({'error': 'Метод не разрешен'}), 405


@app.route('/cart')
def cart():
    global services_id, price_counter, count_services

    services = Service.query.all()

    cart_services = [service for service in services if service.id in session['services_id']]

    return render_template('cart.html', cart_services=cart_services,
                           session=session, current_user=current_user)


@app.route('/cancel_service/<int:service_id>', methods=['POST'])
def cancel_service(service_id):
    if request.method == 'POST':
        # Ensure that the service_id is removed from the session
        session_services_id = session.get('services_id')
        if service_id in session_services_id:
            session_services_id.remove(service_id)

            # Update session variables
            session['counter'] = session.get('counter', 0) - 1
            service_info = Service.query.get(service_id)
            session['price_counter'] = session.get('price_counter', 0) - service_info.price

            return jsonify({
                'success': True,
                'counter': session.get('counter'),
                'price_counter': session.get('price_counter')
            })

    return jsonify({'error': 'Failed to cancel service.'}), 400


@app.route('/logout_commit')
def log_out_commit():
    return render_template('logout_commit.html', current_user=current_user)


@app.route('/logout')
def log_out():
    logout_user()
    return redirect('/autorization')