from flask import render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
from . import quotations
from ..models import Cliente, Cotizacion
from .. import db

@quotations.route('/elegir-cliente', methods=['GET', 'POST'])
@login_required
def elegir_cliente():
    """
    Este recurso sirve de prompt para especificar el cliente para el que se genera 
    una nueva cotización. La elección se hace por nombre corto de cada cliente. Se
    redirecciona al recurso categorias indicando en la URL el nombre corto 
    del cliente.
    """
    if request.method == 'POST':
        cliente_nombre_corto = request.form['cliente']
        return redirect(url_for('quotations.categorias', cliente=cliente_nombre_corto))
    else:
        clientes = [cliente.nombre_corto for cliente in current_user.clientes]
        print(clientes)
        return render_template('quotations/elegir_cliente.html', clientes=clientes)

@quotations.route('/categorias/<string:cliente>', methods=['GET', 'POST'])
@login_required
def categorias(cliente):
    """
    Este recurso sirve de prompt para solicitar el número de categorias [distintas]
    de productos por cliente que van a cotizarse. Se redirecciona al recurso nueva_cotizacion
    exportando el número de categorias.
    """
    current_cliente = Cliente.query.filter_by(nombre_corto=cliente).first()
    total_categorias_productos = len([producto for producto in current_cliente.productos])
    if request.method == 'POST':
        categorias_a_cotizar = int(request.form['categorias'])
        return redirect(url_for('quotations.nueva_cotizacion', cliente=cliente, categorias_a_cotizar=categorias_a_cotizar))
    else:
        return render_template('quotations/categorias.html', cliente=cliente, total_categorias_productos=total_categorias_productos)

@quotations.route('/nueva-cotizacion/<string:cliente>/<int:categorias_a_cotizar>', methods=['GET', 'POST'])
@login_required
def nueva_cotizacion(cliente, categorias_a_cotizar):
    """
    Recurso que importa la información de los productos y número de categorías a cotizar.
    """
    current_cliente = Cliente.query.filter_by(nombre_corto=cliente).first()
    if request.method == 'POST':
        print(request.form)
        return '<h1>Nueva cotización para {}</h1>'.format(cliente)
    else:
        return render_template('quotations/nueva_cotizacion.html', cliente=current_cliente, categorias_a_cotizar=categorias_a_cotizar)