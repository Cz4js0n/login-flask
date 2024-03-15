from flask import Flask, redirect, request, url_for, render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///testowa.db'
app.config['SECRET_KEY'] = 'ZAQ!2wsx'
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False, unique=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now())

    def __repr__(self):
        return '<User %r>' % self.id


@app.route('/')
def index():
    return redirect('/register')


@app.route('/register', methods=['POST', 'GET'])
def register_user():
    if request.method == 'GET':
        return render_template('register-form.html')
    username = request.form['username']
    email = request.form['email']
    password = request.form['password']
    repassword = request.form['r_password']
    if request.method == 'POST':
        if username == "" or email == "" or password == "" or repassword == "":
            return 'Rejestracja nieudana (nie wypełniono wszystkich pól)'
        elif password != repassword:
            return 'Rejestracja nieudana (hasła się nie zgadzają)'
        else:
            password_hashed = hash(password)
            new_user = User(username=username, email=email, password=password_hashed)
            db.session.add(new_user)
            db.session.commit()
            return redirect('/login')


@app.route('/login', methods=['POST', 'GET'])
def login_user():
    if request.method == 'GET':
        return render_template('login-form.html')
    username = request.form['username']
    password = request.form['password']
    password_check = hash(password)
    if request.method == 'POST':
        user = User.query.filter_by(username=username, password=password_check).first()
        if user is None:
            return redirect('/login-failed')
        else:
            return redirect('/login-success')


@app.route('/login-success')
def success():
    print('Zalogowano pomyślnie')
    return redirect('/login')


@app.route('/login-failed')
def fail():
    return 'Nie zalogowano (błędne hasło bądź nie ma takiego użytkownika)'


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
