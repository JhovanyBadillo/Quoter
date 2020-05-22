from flask import render_template, redirect, url_for, session, flash, current_app
from flask_login import login_required, current_user
from . import main
from .forms import LoginForm, RegistroUsuarioForm
from .. import db
from ..models import Usuario, Cliente, Producto

@main.route('/', methods=['GET', 'POST'])
def index():
    if current_user.is_authenticated:
        return redirect(url_for('main.menu'))
    else:
        return render_template('index.html')

@main.route('/menu')
@login_required
def menu():
    return render_template('menu.html')

@main.route('/mis-productos')
@login_required
def mis_productos():
    mis_productos = []
    for cliente in current_user.clientes.all():
        for producto in cliente.productos.all():
            mis_productos.append(producto)
    return render_template('mis_productos.html', mis_productos=mis_productos)
