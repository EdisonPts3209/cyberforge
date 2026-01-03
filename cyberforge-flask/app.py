from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from models import db, User
from werkzeug.security import generate_password_hash, check_password_hash
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'super_secret_key_change_it_now'  # ОБЯЗАТЕЛЬНО ИЗМЕНИ!
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///instance/cyberforge.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Войдите, чтобы получить доступ к этой странице.'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Создаём БД и владельца при первом запуске
with app.app_context():
    db.create_all()
    if not User.query.filter_by(username='red1dark').first():
        owner = User(
            username='red1dark',
            email='red1dark@cyberforge.ru',
            password_hash=generate_password_hash('твой_супер_надёжный_пароль'),  # ИЗМЕНИ!
            role='owner'
        )
        db.session.add(owner)
        db.session.commit()
        print("Владелец @red1dark создан!")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password_hash, password):
            login_user(user)
            flash('Успешный вход!', 'success')
            return redirect(url_for('dashboard'))
        flash('Неверный логин или пароль', 'danger')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        if User.query.filter_by(username=username).first():
            flash('Такой username уже занят', 'danger')
            return redirect(url_for('register'))
        if User.query.filter_by(email=email).first():
            flash('Такой email уже зарегистрирован', 'danger')
            return redirect(url_for('register'))
        new_user = User(
            username=username,
            email=email,
            password_hash=generate_password_hash(password),
            role='user'
        )
        db.session.add(new_user)
        db.session.commit()
        flash('Регистрация успешна! Теперь войдите.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Вы вышли из аккаунта', 'info')
    return redirect(url_for('index'))

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')

@app.route('/admin')
@login_required
def admin_panel():
    if not current_user.is_owner():
        flash('Доступ запрещён', 'danger')
        return redirect(url_for('index'))
    users = User.query.all()
    return render_template('admin-panel.html', users=users)

# Остальные страницы (просто рендер)
@app.route('/rules')
def rules():
    return render_template('rules.html')

@app.route('/privacy')
def privacy():
    return render_template('privacy.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/support')
def support():
    return render_template('support.html')

@app.route('/terms')
def terms():
    return render_template('terms.html')

@app.route('/for-authors')
def for_authors():
    return render_template('for-authors.html')

@app.route('/articles')
def articles():
    return render_template('articles.html')

@app.route('/classes')
def classes():
    return render_template('classes.html')

@app.route('/faq')
def faq():
    return render_template('faq.html')

@app.route('/new-article')
@login_required
def new_article():
    return render_template('new-article.html')

@app.route('/new-class')
@login_required
def new_class():
    return render_template('new-class.html')

@app.route('/certificate-create')
@login_required
def certificate_create():
    return render_template('certificate-create.html')

@app.route('/profile/<username>')
def profile(username):
    user = User.query.filter_by(username=username).first_or_404()
    return render_template('profile.html', profile_user=user)

if __name__ == '__main__':
    app.run(debug=True, port=5000)