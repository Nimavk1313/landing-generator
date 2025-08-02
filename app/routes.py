from flask import render_template, url_for, flash, redirect, request, jsonify
from app import app, db
from app.forms import RegistrationForm, LoginForm
from app.models import User, Page
from flask_login import login_user, current_user, logout_user, login_required
import json

@app.route('/')
@app.route('/home')
def home():
    return render_template('index.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('signup.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('dashboard'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/dashboard')
@login_required
def dashboard():
    page = Page.query.filter_by(author=current_user).first()
    if not page:
        page = Page(author=current_user)
        db.session.add(page)
        db.session.commit()
    return render_template('dashboard.html', page=page, emails=[]) # placeholder for emails

@app.route('/<string:username>')
def profile(username):
    user = User.query.filter_by(username=username).first_or_404()
    page = Page.query.filter_by(author=user).first_or_404()
    page.impressions += 1
    db.session.commit()

    content = json.loads(page.content) if page.content else []
    return render_template('profile.html', user=user, content=content)

@app.route('/api/track_click', methods=['POST'])
def track_click():
    data = request.get_json()
    user_id = data.get('user_id')
    page = Page.query.filter_by(user_id=user_id).first()
    if page:
        page.clicks += 1
        db.session.commit()
        return jsonify({'success': True})
    return jsonify({'success': False, 'error': 'Page not found'})

@app.route('/export_emails')
@login_required
def export_emails():
    # This is a placeholder for the email export functionality
    return "Email export functionality is not yet implemented."

@app.route('/editor')
@login_required
def editor():
    return render_template('editor.html')

@app.route('/test_editor')
def test_editor():
    return render_template('test_editor.html')

@app.route('/api/save_page', methods=['POST'])
@login_required
def save_page():
    data = request.get_json()
    page = Page.query.filter_by(author=current_user).first()
    if page:
        page.content = json.dumps(data.get('content'))
        db.session.commit()
        return jsonify({'success': True})
    return jsonify({'success': False, 'error': 'Page not found'})
