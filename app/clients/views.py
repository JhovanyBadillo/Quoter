from flask import render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from . import clients
from ..models import Cliente, Cotizacion
from .. import db

@clients.route('/', methods=['GET', 'POST'])
@login_required
def listado_clientes():
    clientes = Cliente.query.filter_by(usuario=current_user).all()
    return render_template('clients/listado_clientes.html', clientes=clientes)

@clients.route('/<string:cliente>')
@login_required
def historial(cliente):
    cliente_actual = Cliente.query.filter_by(nombre_corto=cliente).first()
    cotizaciones = Cotizacion.query.filter_by(cliente=cliente_actual).all()
    return render_template('clients/historial_cotizaciones.html', cliente=cliente_actual, cotizaciones=cotizaciones)

@clients.route('/agregar-cliente', methods=['GET', 'POST'])
@login_required
def agregar_cliente():
    if request.method == 'POST':
        print(request.form)
        nuevo_cliente = Cliente(usuario=current_user, razon_social=request.form['razon_social'], rfc=request.form['rfc'], nombre_corto=request.form['nombre_corto'], telefono=request.form['telefono'], calle_numero=request.form['calle_numero'], colonia=request.form['colonia'], municipio=request.form['municipio'], estado=request.form['estado'], cp=request.form['cp'])
        print(nuevo_cliente)
        db.session.add(nuevo_cliente)
        db.session.commit()
        flash('El cliente ha sido agregado satisfactoriamente')
        return redirect(url_for('clients.listado_clientes'))
    return render_template('clients/agregar_cliente.html')

@clients.route('/editar-cliente/<string:cliente>', methods=['GET', 'POST'])
@login_required
def editar_cliente(cliente):
    """
    Esta función NO compara los datos almacenados del cliente a modificar con los
    que se reciben en request.form. Se reescriben los campos en el registro correspondiente
    del cliente solamente si el dato modificado no es un string de longitud 0. 
    """
    cliente_a_editar = Cliente.query.filter_by(nombre_corto=cliente).first()
    if request.method == 'POST':
        for dato in request.form.keys():
            if len(request.form[dato]) > 0:
                setattr(cliente_a_editar, dato, request.form[dato])
        db.session.add(cliente_a_editar)
        db.session.commit()
        flash('Se han guardado los cambios')
        return redirect(url_for('clients.listado_clientes'))
    return render_template('clients/editar_cliente.html', cliente=cliente_a_editar)

# @clients.route('/', methods=['GET', 'POST'])
# @login_required
# def seleccionar_cliente():
#     clientes = [cliente.razon_social for cliente in Cliente.query.filter_by(usuario=current_user).all()]
#     if request.method == 'POST':
#         selected_client = Cliente.query.filter_by(razon_social=request.form['cliente']).first()
#         print(request.form['cliente'])
#         return redirect('/clientes/{}'.format(selected_client.nombre_corto))
#     return render_template('clients/seleccionar_cliente.html', clientes=clientes)
