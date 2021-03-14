import os
import secrets
from PIL import Image
from flask import render_template, url_for, flash, redirect, request, abort
from artwork import app, db, bcrypt
from artwork.forms import RegistrationForm, LoginForm, UpdateAccountForm, ArtworkForm, BidForm
from artwork.models import User, Category, Artwork, Bid
from flask_login import login_user, current_user, logout_user, login_required
from datetime import datetime


@app.route("/")
@app.route("/home")
def home():

    if 'keyword' in request.args:
        page = request.args.get('page', 1, type=int)
        keyword = request.args['keyword']
        artworks = Artwork.query.filter(Artwork.name.like(f'%{keyword}%')).paginate(page=page, per_page=10)

    else:
        page = request.args.get('page', 1, type=int)
        artworks = Artwork.query.order_by(Artwork.date_posted.desc()).paginate(page=page, per_page=10)

    return render_template('home.html', artworks=artworks)


@app.route("/about")
def about():
    return render_template('about.html', title='About')


@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html',
                           title='Register',
                           form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html',
                           title='Login',
                           form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))


def save_compressed_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/images', picture_fn)

    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn


def save_raw_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/images', picture_fn)

    form_picture.save(picture_path)

    return picture_fn


@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            # picture_file = save_compressed_picture(form.picture.data)
            picture_file = save_raw_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='images/' + current_user.image_file)
    return render_template('account.html',
                           title='Account',
                           image_file=image_file,
                           form=form)


@app.route('/new_artwork', methods=['GET', 'POST'])
def new_artwork():
    form = ArtworkForm()
    categories = Category.query.all()
    form.category.choices.append((0, 'Select...'))
    for category in categories:
        form.category.choices.append((category.id, category.name))

    if form.validate_on_submit():

        image_file = save_raw_picture(form.image_file.data)

        artwork = Artwork(user_id=current_user.id,
                          date_posted=datetime.now().date(),
                          category_id=form.category.data,
                          name=form.name.data,
                          base=form.base.data,
                          size=form.size.data,
                          frame=form.frame.data,
                          color=form.color.data,
                          time=form.time.data,
                          image_file=image_file)
        db.session.add(artwork)
        db.session.commit()
        flash('Your artwork has been created!', 'success')
        return redirect(url_for('home'))
    return render_template('new_artwork.html',
                           legend='Insert Artwork',
                           form=form)
#är det rätt att skriva det så? form.--.data? är det problemet?


@app.route("/artwork/<int:artwork_id>", methods=['GET', 'POST'])
def artwork(artwork_id):

    form = BidForm()
    if form.validate_on_submit():
        bid = Bid(bid_price=form.bid.data,
                  user_id=current_user.id,
                  artwork_id=artwork_id)

        db.session.add(bid)
        db.session.commit()
        flash('Your bid has been placed!', 'success')
        return redirect(url_for('home'))

    bids = Bid.query.order_by(Bid.bid_price.desc())

    artwork = Artwork.query.get_or_404(artwork_id)
    return render_template('artwork.html', name=artwork.name, artwork=artwork, bids=bids, legend='Place bid', form=form)


@app.route("/artwork/<int:artwork_id>/update", methods=['GET', 'POST'])
@login_required
def update_artwork(artwork_id):
    artwork = Artwork.query.get_or_404(artwork_id)
    if artwork.user != current_user:
        abort(403)
    form = ArtworkForm()
    categories = Category.query.all()
    form.category.choices.append((0, 'Select...'))
    for category in categories:
        form.category.choices.append((category.id, category.name))

    if form.validate_on_submit():
        artwork.name = form.name.data
        artwork.category_id = form.category.data
        artwork.time = form.time.data
        artwork.base = form.base.data
        artwork.size = form.size.data
        artwork.frame = form.frame.data
        artwork.color = form.color.data
        artwork.image_file = save_raw_picture(form.image_file.data)
        db.session.commit()
        flash('Your artwork has been updated!', 'success')
        return redirect(url_for('artwork', artwork_id=artwork.id))
    elif request.method == 'GET':

        form.name.data = artwork.name
        form.category.data = artwork.category
        form.time.data = artwork.time
        form.base.data = artwork.base
        form.size.data = artwork.size
        form.frame.data = artwork.frame
        form.color.data = artwork.color
        form.image_file.data = artwork.image_file

    return render_template('new_artwork.html', title='Update Artwork',
                           form=form, legend='Update Artwork')

@app.route("/artwork/<int:artwork_id>/delete", methods=['POST'])
@login_required
def delete_artwork(artwork_id):
    artwork = Artwork.query.get_or_404(artwork_id)
    if artwork.user != current_user:
        abort(403)
    db.session.delete(artwork)
    db.session.commit()
    flash('Your artwork has been deleted!', 'success')
    return redirect(url_for('home'))


@app.route("/user/<string:username>")
def user_artworks(username):
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    artworks = Artwork.query.filter_by(user=user)\
        .order_by(Artwork.date_posted.desc())\
        .paginate(page=page, per_page=5)
    return render_template('user_artworks.html', artworks=artworks, user=user)

# TODO: create here your routes
