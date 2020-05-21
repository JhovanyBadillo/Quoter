from . import db, login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

class Usuario(UserMixin, db.Model):
    __tablename__ = 'usuarios'

    id               = db.Column(db.Integer, primary_key=True)
    nombre           = db.Column(db.String(100))
    apellido_paterno = db.Column(db.String(100))
    apellido_materno = db.Column(db.String(100))
    calle_numero     = db.Column(db.String(100))
    colonia          = db.Column(db.String(100))
    municipio        = db.Column(db.String(100))
    cp               = db.Column(db.String(5))
    estado           = db.Column(db.String(100))
    telefono         = db.Column(db.String(100))
    correo           = db.Column(db.String(100), unique=True, index=True)
    rfc              = db.Column(db.String(100), unique=True)
    password_hash    = db.Column(db.String(128))

    clientes = db.relationship('Cliente', backref='usuario', lazy='dynamic')

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

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
    cp              = db.Column(db.String(5))
    estado          = db.Column(db.String(100))

    cotizaciones = db.relationship('Cotizacion', backref='cliente', lazy='dynamic')

    def __repr__(self):
        return '<Cliente %r>' % self.nombre_corto


class Cotizacion(db.Model):
    __tablename__ = 'cotizaciones'

    id          = db.Column(db.Integer, primary_key=True, nullable=False)
    cliente_id  = db.Column(db.Integer, db.ForeignKey('clientes.id'), nullable=False)
    folio       = db.Column(db.String(10), nullable=False, index=True, unique=True)
    nombre      = db.Column(db.String(100), nullable=False)
    fecha       = db.Column(db.String(10), nullable=False)
    resumen     = db.Column(db.Text(), nullable=False)
    importe     = db.Column(db.String(20), nullable=True)

    def __repr__(self):
        return '<Cotizacion %r>' % self.folio
        

@login_manager.user_loader
def load_user(user_id):
    return Usuario.query.get(int(user_id))