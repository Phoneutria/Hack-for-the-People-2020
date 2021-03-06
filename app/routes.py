from app import app, db
from app.forms import LoginForm, RegistrationForm, CreateForm, SearchForm
from app.scraping import Scraping
from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, Post
from werkzeug.urls import url_parse

@app.route('/')
@app.route('/home')
def home():
    return render_template("home.html", title="Home")


@app.route('/about')
def about():
    return render_template("about.html", title="About")

@app.route('/faq')
def faq():
    return render_template("faq.html", title = "FAQ")

@app.route('/search', methods = ['GET', 'POST'])
@login_required
def search():
    form = SearchForm()
    if form.validate_on_submit():
        location = form.location.data
        user = form.name.data
        offering = form.offering.data
        looking = form.looking.data

        #get all posts from the server
        postList = Post.query.all()

        # update list of posts based on each criteria
        postList = [post for post in postList if (not location or post.location == location)]

        postList = [post for post in postList if (not user or post.author.username == user)]

        postList = [post for post in postList if (not offering or post.offering == offering)]

        postList = [post for post in postList if (not looking or post.looking == looking)]

        return render_template("catalog.html", title = "Search Results", listings = postList, searched = True)

    return render_template("search.html", title="Search", form = form)

@app.route('/catalog')
@login_required
def catalog():
    # gets the list of posts from the server and gives them to catalog.html to render
    postList = Post.query.all()
    return render_template("catalog.html", title="Catalog", listings = postList)

@app.route('/create', methods = ['GET', 'POST'])
@login_required
def create():
    form = CreateForm()
    if form.validate_on_submit():
        listing = Post(offering = form.offering.data, looking = form.lookingFor.data,
        add_info = form.other.data, author = current_user)
        db.session.add(listing)
        db.session.commit()
        return redirect(url_for('catalog'))

    return render_template("create.html", title = "Create", form = form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('home')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data,
         name=form.name.data, location=form.location.data, zipcode = form.zipcode.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash("Congratulations, you are now a registered user!")
        return redirect(url_for('login'))
    return render_template('register.html', title="Register", form=form)

@app.route('/recommend')
@login_required
def recommend():
    return render_template('recommend.html', plants = Scraping.find_range(Scraping.scrape_tables(zipcode = current_user.zipcode)))