from flask import Flask

app = Flask(__name__)

app.config['SECRET_KEY'] = '1234'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SESSION_TYPE'] = 'filesystem'
app.config['CACHE_TYPE'] = 'SimpleCache'
app.config['CACHE_DEFAULT_TIMEOUT'] = 1000
