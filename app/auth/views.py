from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, login_required, logout_user, current_user
from . import auth
from .forms import LoginForm, SignupForm
from ..models import Usuario
from .. import db


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.menu'))
    else:
        if request.method == 'POST':
            user = Usuario.query.filter_by(correo=request.form['email']).first()
            if user is not None and user.verify_password(request.form['password']):
                login_user(user)
                next = request.args.get('next')
                if next is None or not next.startswith('/'):
                    next = url_for('main.menu')
                return redirect(next)
            flash('Dirección de correo electrónico o contraseña inválida')
        return render_template('auth/login.html')

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Has cerrado sesión')
    return redirect(url_for('main.index'))

@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('main.menu'))
    else:
        if request.method == 'POST':
            if Usuario.query.filter_by(correo=request.form['email']).first():
                flash("La dirección de correo electrónico ya se encuentra en uso")
                return redirect(request.url)
            else:
                user = Usuario(correo=request.form['email'], password=request.form['password'])
                db.session.add(user)
                db.session.commit()
                flash('Ahora puedes iniciar sesión')
                return redirect(url_for('auth.login'))
        return render_template('auth/signup.html')

