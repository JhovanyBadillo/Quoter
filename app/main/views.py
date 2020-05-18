from flask import render_template, redirect, url_for, session, flash, current_app
from flask_login import login_required, current_user
from . import main
from .forms import LoginForm, RegistroUsuarioForm
from .. import db
from ..models import Usuario, Cliente
from hashlib import md5

@main.route('/', methods=['GET', 'POST'])
def index():
    if current_user.is_authenticated:
        print(current_user)
        return redirect(url_for('main.menu'))
    else:
        return render_template('index.html')

@main.route('/menu')
@login_required
def menu():
    return render_template('menu.html')
