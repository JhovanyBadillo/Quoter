from flask import render_template, redirect, url_for, session, flash, current_app, request
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
    datos_completos = current_user.datos_completos
    return render_template('menu.html', datos_completos=datos_completos)

@main.route('/mis-datos', methods=['GET', 'POST'])
@login_required
def mis_datos():
    if request.method == 'POST':
        print(request.form)
        if 'fisica' in request.form.keys():
            return redirect(url_for('main.mis_datos_fisica'))
        elif 'moral' in request.form.keys():
            return redirect(url_for('main.mis_datos_moral'))
        else:
            return redirect(url_for('main.menu'))
    else:
        return render_template('mis_datos.html')

@main.route('/mis-datos/fisica', methods=['GET', 'POST'])
@login_required
def mis_datos_fisica():
    me = current_user
    if request.method == 'POST':
        print(request.form)
        for dato in request.form.keys():
            setattr(me, dato, request.form[dato])
        me.datos_completos = 'Y'
        db.session.add(me)
        db.session.commit()
        flash('Información almacenada. Ahora ya puedes generar cotizaciones')
        return redirect(url_for('main.menu'))
    else:
        return render_template('mis_datos_fisica.html', me=me)

@main.route('/mis-datos/moral', methods=['GET', 'POST'])
@login_required
def mis_datos_moral():
    me = current_user
    if request.method == 'POST':
        print(request.form)
        for dato in request.form.keys():
            setattr(me, dato, request.form[dato])
        me.datos_completos = 'Y'
        db.session.add(me)
        db.session.commit()
        flash('Información almacenada. Ahora ya puedes generar cotizaciones')
        return redirect(url_for('main.menu'))
    else:
        return render_template('mis_datos_moral.html', me=me)

@main.route('/mis-productos')
@login_required
def mis_productos():
    mis_productos = []
    for cliente in current_user.clientes.all():
        for producto in cliente.productos.all():
            mis_productos.append(producto)
    return render_template('mis_productos.html', mis_productos=mis_productos)
