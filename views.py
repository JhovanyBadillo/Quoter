from flask import Flask, render_template, request, g, redirect, url_for, flash, session
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.fields.html5 import EmailField
from wtforms.fields import SelectField
from wtforms.validators import DataRequired, Email, EqualTo
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from hashlib import md5

import sqlite3, os, datetime

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'quotations.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = b'\xe8\xf7\xd9s\xfe\xa6\x11\r\x08b \xf5o\xb5\xbbW'
# app.config['PERMANENT_SESSION_LIFETIME'] = datetime.timedelta(seconds=600)
bootstrap = Bootstrap(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)


class Usuario(db.Model):
    __tablename__ = 'usuarios'

    id               = db.Column(db.Integer, primary_key=True)
    nombre           = db.Column(db.String(100))
    apellido_paterno = db.Column(db.String(100))
    apellido_materno = db.Column(db.String(100))
    calle_numero     = db.Column(db.String(100))
    colonia          = db.Column(db.String(100))
    municipio        = db.Column(db.String(100))
    cp               = db.Column(db.Integer)
    estado           = db.Column(db.String(100))
    telefono         = db.Column(db.String(100))
    correo           = db.Column(db.String(100), unique=True, index=True)
    rfc              = db.Column(db.String(100), unique=True)
    password         = db.Column(db.String(100))

    clientes = db.relationship('Cliente', backref='usuario', lazy='dynamic')

    def __repr__(self):
        return '<Usuario %r>' % self.correo


class Cliente(db.Model):
    __tablename__ = 'clientes'

    id              = db.Column(db.Integer, primary_key=True, nullable=False)
    usuario_id      = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    razon_social    = db.Column(db.String(100))
    rfc             = db.Column(db.String(100), unique=True)
    nombre_corto    = db.Column(db.String(100), index=True)
    telefono        = db.Column(db.String(100))
    calle_numero    = db.Column(db.String(100))
    colonia         = db.Column(db.String(100))
    municipio       = db.Column(db.String(100))
    cp              = db.Column(db.Integer)
    estado          = db.Column(db.String(100))

    def __repr__(self):
        return '<Cliente %r>' % self.nombre_corto

@app.shell_context_processor
def make_shell_context():
    return dict(db=db, Usuario=Usuario, Cliente=Cliente)


def dentroDeSesion():
    return True if (session.get('email') is not None) else False

class LoginForm(FlaskForm):
    email = EmailField('', validators=[DataRequired(), Email()], render_kw={'placeholder': 'Email'})
    password = PasswordField('', validators=[DataRequired()], render_kw={'placeholder': 'Contraseña'})
    submit = SubmitField('Iniciar Sesión')

class RegistroUsuarioForm(FlaskForm):
    email = EmailField('', validators=[DataRequired(), Email()], render_kw={'placeholder': 'Email'})
    password = PasswordField('', validators=[DataRequired()], render_kw={'placeholder': 'Contraseña'})
    confirmarPassword = PasswordField('', validators=[DataRequired(), EqualTo('password')], render_kw={'placeholder': 'Confirmar contraseña'})
    submit = SubmitField('Registrarse')


# class OpcionesForm(FlaskForm):
#     option = SelectField('Opciones', choices=['C++', 'Java', 'Python', 'Rust'])
#     submit = SubmitField('Enviar')


# class ClientesForm(FlaskForm):
#     def __init__(self, formdata, **kwargs):
#         self.currentUsuario = formdata
#         super(ClientesForm, self).__init__(formdata=formdata, **kwargs)
#     # currentUsuario = Usuario.query.filter_by(correo=session.get('email')).first()
#     clientes = Cliente.query.filter_by(usuario=ClientesForm().currentUsuario).all()
#     # clientes = getattr(g, '_clientes', [])
#     nombreCortoDeClientes = [cliente.nombre_corto for cliente in clientes]
#     clienteElegido = SelectField('Clientes', choices=nombreCortoDeClientes)
#     submit = SubmitField('Enviar')


@app.route('/', methods=['GET', 'POST'])
def index():
    if dentroDeSesion():
        return redirect(url_for('menu'))
    else:
        return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if session.get('email', False):
        return redirect(url_for('menu'))
    else:
        if form.validate_on_submit():
            usuario = Usuario.query.filter_by(correo=form.email.data).first()
            if usuario:
                if usuario.password == md5((form.password.data).encode()).hexdigest():
                    form.password.data = ''
                    session['email'] = form.email.data
                    form.email.data = ''
                    return redirect(url_for('menu'))
            else:
                flash('Datos incorrectos')
                return redirect(url_for('login'))
        return render_template('login.html', form=form)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    # TODO Verificar que no exista ya el correo a registrar
    form = RegistroUsuarioForm()
    if form.validate_on_submit():
        email = form.email.data
        password = md5((form.password.data).encode()).hexdigest()
        form.email.data = ''
        form.password.data = ''
        try:
            usuario = Usuario(correo=email, password=password)
            db.session.add(usuario)
            db.session.commit()
            return redirect(url_for('login'))
        except Exception as e:
            flash('La dirección de correo electrónico ya se encuentra en uso')
            return redirect(url_for('signup'))
    return render_template('signup.html', form=form)

@app.route('/logout')
def logout():
    if session.get('email', False):
        del session['email']
        return redirect(url_for('index'))
    return redirect(url_for('login'))

@app.route('/menu')
def menu():
    if session.get('email'):
        return render_template('menu.html')
    else:
        return redirect(url_for('login'))    

# @app.route('/clientes', methods=['GET', 'POST'])
# def listar_clientes():
#     if session.get('email'):
#         currentUsuario = Usuario.query.filter_by(correo=session.get('email')).first()
#         clientes = Cliente.query.filter_by(usuario=currentUsuario).all()
#         nombreCortoDeClientes = [cliente.nombre_corto for cliente in clientes]
#         print(nombreCortoDeClientes)
#         # return str([cliente.nombre_corto for cliente in clientes])
#         return render_template('clientes.html', clientes=nombreCortoDeClientes)
#     else:
#         return redirect(url_for('login'))
    
@app.route('/clientes', methods=['GET', 'POST'])
def listar_clientes():
    if session.get('email'):
        currentUsuario = Usuario.query.filter_by(correo=session.get('email')).first()
        clientes = Cliente.query.filter_by(usuario=currentUsuario).all()
        nombreCortoDeClientes = [cliente.nombre_corto for cliente in clientes]
        print(nombreCortoDeClientes)
        # return str([cliente.nombre_corto for cliente in clientes])
        return render_template('clientes.html', clientes=nombreCortoDeClientes)
    else:
        return redirect(url_for('login'))
    
@app.route('/clientes/ver/<nombre_corto>', methods=['GET', 'POST'])
def ver_cliente(nombre_corto):
    if session.get('email'):
        cliente = Cliente.query.filter_by(nombre_corto=nombre_corto.upper()).first()
        print(cliente.razon_social)
        return str(cliente.razon_social + ' ' + cliente.rfc)
    else:
        return redirect(url_for('login'))

@app.route('/registro-contacto')
def add_contacto():
    return "Registrar contacto"

@app.route('/registro-producto')
def add_product():
    return "Registrar producto"

if __name__ == '__main__':
    app.run(port=3002, debug=True)