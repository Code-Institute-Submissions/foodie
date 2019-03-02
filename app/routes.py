import json
from app import app, db
from flask import render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, login_required, current_user
from app.models.forms import SignForm
from app.models.users import User


# ================================================ #


# make filters dict available to all templates
@app.context_processor
def inject_filters():
    with open('app/data/schemas/filters.json') as filters_file:
        filters = json.load(filters_file)
        return dict(filters=filters)


# ================================================ #


# index
@app.route('/')
def index():
    return render_template('index.html')


# ================================================ #


# profile
@app.route('/profile')
@login_required
def profile():
    return render_template('profile.html')


# ================================================ #


# sign in / out
@app.route('/sign/<url>', methods=['GET', 'POST'])
def sign(url):

    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = SignForm()
    if form.validate_on_submit():

        # check if user exists
        user = db.users.find_one({"username": form.username.data})

        # if the user is signing in
        if url == 'in':
            if user and User.check_password(user['password'], form.password.data):
                login_user(User(user['username']), remember=form.remember.data)
                return redirect(request.args.get("next") or url_for("profile"))
            else:
                flash("Incorrect username or password.", category='sign-error')
                return redirect(url_for('sign', url=url))
        
        # if the user is signing up
        else:
            if user:
                flash("That username is already in use.", category='sign-error')
                return redirect(url_for('sign', url=url))
            else:
                User.add_user(form.username.data, form.password.data)
                login_user(User(form.username.data), remember=form.remember.data)
                return redirect(request.args.get("next") or url_for("profile"))

    return render_template('sign.html', form=form, url=url)


# ================================================ #


# sign out
@app.route('/signout')
def signout():
    logout_user()    
    return redirect(url_for('sign', url='in'))


# ================================================ #
