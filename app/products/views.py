from flask import render_template, redirect, request, flash, url_for
from flask_login import login_required, current_user
from . import products
from ..models import Cliente, Producto
from .. import db


@products.route('/<string:cliente>')
@login_required
def listado_productos(cliente):
    current_cliente = Cliente.query.filter_by(nombre_corto=cliente).first()
    return render_template('products/listado_productos.html', cliente=current_cliente)

# @products.route('/agregar-producto')
# Recurso para agregar un producto seleccionando el cliente al vuelo

@products.route('/agregar-producto/<string:cliente>', methods=['GET', 'POST'])
@login_required
def agregar_producto(cliente):
    """
    El único filtro por ahora de esta función es verificar en base de datos si ya existe el sku
    del producto a agregar.
    """
    current_cliente = Cliente.query.filter_by(nombre_corto=cliente).first()
    if request.method == 'POST':
        if Producto.query.filter_by(sku=request.form['sku']).first():
            flash('SKU previamente registrado')
            return redirect(request.url)
        else:
            nuevo_producto = Producto(cliente=current_cliente, sku=request.form['sku'], medicion=request.form['medicion'], descripcion=request.form['descripcion'], precio_unitario=request.form['precio_unitario'])
            db.session.add(nuevo_producto)
            db.session.commit()
            flash('Producto agregado satisfactoriamente')
            return redirect(url_for('products.listado_productos', cliente=current_cliente.nombre_corto))
    return render_template('products/agregar_producto.html', cliente=current_cliente)

@products.route('/editar-producto/<string:sku>', methods=['GET', 'POST'])
@login_required
def editar_producto(sku):
    """
    Función para modificar los datos de un producto. La recolección de los datos a modificar son buscados
    en base de datos usando el sku del producto. 
    """
    producto_a_editar = Producto.query.filter_by(sku=sku).first()
    current_cliente = Cliente.query.filter_by(id=producto_a_editar.cliente_id).first()
    if request.method == 'POST':
        for campo in request.form.keys():
            if len(request.form[campo]) > 0:
                setattr(producto_a_editar, campo, request.form[campo])
        db.session.add(producto_a_editar)
        db.session.commit()
        flash('Se han guardado los cambios')
        return redirect(url_for('products.listado_productos', cliente=current_cliente.nombre_corto))
    return render_template('products/editar_producto.html', producto=producto_a_editar, cliente=current_cliente)