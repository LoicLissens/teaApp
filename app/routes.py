from flask import render_template, redirect, flash, url_for, request
from werkzeug.urls import url_parse
from app import app
from app import db
from app.forms import LoginForm, RegisterForm, AddTeaForm, AddFunFactForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, Tea
from app.myjson import FunFactJson

# INDEX ROUTZ
@app.route('/')
@app.route('/index')
def index():

    return render_template('index.html',  title="My Tea reference")


# LOGIN ROUTE
@app.route('/login', methods=['GET', 'POST'])
def login():
    fun_fact = FunFactJson.get_random_fact("en")
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(
            username=form.username.data.lower()).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password', 'is-danger')

            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        # the url parse with netloc is use to check if the url in the next is on the same domain name  => secu
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template("login.html", form=form, title="Login", fun_fact=fun_fact)

# LOGOUT ROUTE
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

# REGISTER ROUTE
@app.route('/register', methods=['GET', 'POST'])
def register():
    fun_fact = FunFactJson.get_random_fact("en")
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(username=form.username.data.lower(),
                    email=form.email.data.lower())
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash(
            f"You got succeful registered, your username is: {form.username.data} and your mail is:  {form.email.data}", 'is-success')
        return redirect(url_for("login"))

    return render_template("register.html", form=form, title="Register", fun_fact=fun_fact)

# ROUTE FOR ACCOUNT PAGE
@app.route('/account')
@login_required  # Intercept the request and check if the user is logeed if not he is redirect to the login pagea
def account():
    return render_template("account.html", title="Personal space")


# ROUTE FOR COLLECTION OF TEA
@app.route('/collection')
def collection():
    return render_template("collection.html")

# ROUTE FOR ADMIN PANEL
@app.route('/panel')
def panel():
    fun_fact = FunFactJson.get_random_fact("en")
    if not current_user.is_authenticated:
        return render_template('404.html', fun_fact=fun_fact), 404
    if not current_user.admin:
        return render_template('404.html', fun_fact=fun_fact), 404
    form_tea = AddTeaForm()
    form_fun_fact = AddFunFactForm()

    return render_template("panel.html", title="Admin panel", form_fun_fact=form_fun_fact, form_tea=form_tea)


# ROUTE FOR ADDING FUN FACT
@app.route('/addfunfact', methods=['POST', 'GET'])
def add_fun_fact():
    fun_fact = FunFactJson.get_random_fact("en")
    if not current_user.is_authenticated:
        return render_template('404.html', fun_fact=fun_fact), 404
    if not current_user.admin:
        return render_template('404.html', fun_fact=fun_fact), 404
    form = AddFunFactForm()
    if form.validate_on_submit():
        fr = form.fun_fact_fr.data
        en = form.fun_fact_en.data
        data = {"fr": fr, "en": en}
        FunFactJson.set_fact(data)
        flash(
            f"Your fun fact has been added. 'En:{en}' 'Fr:{fr}'", "is-success")
        return redirect(url_for('panel'))
    else:
        return "This url accept only post request"


# ROUTE FOR ADDING TEA
@app.route('/addtea', methods=['POST', 'GET'])
def add_tea():
    fun_fact = FunFactJson.get_random_fact("en")
    if not current_user.is_authenticated:
        return render_template('404.html', fun_fact=fun_fact), 404
    if not current_user.admin:
        return render_template('404.html', fun_fact=fun_fact), 404
    form = AddTeaForm()
    if form.validate_on_submit():
        tea = Tea(name=form.teaname.data.lower(),
                  description=form.description.data, region_id=form.region.data, type_id=form.type.data, water_temp=form.water_temp.data, water_time=form.water_time.data)
        db.session.add(tea)
        db.session.commit()
        flash(
            f"Your Tea has been added. 'Nom: {form.teaname.data}' 'Description: {form.description.data}' 'Id region: {form.region.data}' 'Id type: {form.type.data}' 'Temperature of water: {form.water_temp.data}' 'Time of infusion: {form.water_time.data}'", "is-success")
        return redirect(url_for('panel'))
    else:
        return f"This url accept only post request or there is an error: {form.errors}"
# 404
@app.errorhandler(404)
def page_not_found(e):
    fun_fact = FunFactJson.get_random_fact("en")
    return render_template('404.html', fun_fact=fun_fact), 404
