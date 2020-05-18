from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField
from wtforms.validators import DataRequired
from flask_login import current_user
from ..models import Cliente

class SelectClientForm(FlaskForm):
    # clients = [client.nombre_corto for client in Cliente.query.filter_by(usuario=current_user).all()]
    selected_client = SelectField('Selecciona un cliente', choices=['C++', 'Java'])
    submit = SubmitField('Enviar')