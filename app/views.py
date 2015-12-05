from flask import render_template, flash, redirect, url_for, session, request
from app import app
from .forms import LoginForm, RegistrationForm
from .models import User


#HOME
@app.route('/')
@app.route('/index')
def index():
    user = {'name': 'Miguel'}  # fake user
    #list of dictionaries
    meals = [
        {
            'house': 'Kirkland',
            'author': {'name': 'John'}
        },
        {
            'house': 'Eliot',
            'author': {'name': 'Susan'}
        }
    ]
    return render_template('index.html',
                           title='Home',
                           user=user,
                           posts=meals)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm(request.form)
    if request.method == 'POST' and form.validate_on_submit():
        user = User(name=form.name.data, email=form.email.data,
            password=form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Thanks for registering')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'POST' and form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            session['user'] = user
            return redirect(request.args.get('next') or url_for('index'))
        flash('Invalid username or password.')
    return render_template('login.html', form=form)

