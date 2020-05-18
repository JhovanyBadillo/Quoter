from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.fields.html5 import EmailField
from wtforms.fields import SelectField
from wtforms.validators import DataRequired, Email, EqualTo

class LoginForm(FlaskForm):
    email = EmailField('', validators=[DataRequired(), Email()], render_kw={'placeholder': 'Email'})
    password = PasswordField('', validators=[DataRequired()], render_kw={'placeholder': 'Contraseña'})
    submit = SubmitField('Iniciar Sesión')


class RegistroUsuarioForm(FlaskForm):
    email = EmailField('', validators=[DataRequired(), Email()], render_kw={'placeholder': 'Email'})
    password = PasswordField('', validators=[DataRequired()], render_kw={'placeholder': 'Contraseña'})
    confirmarPassword = PasswordField('', validators=[DataRequired(), EqualTo('password')], render_kw={'placeholder': 'Confirmar contraseña'})
    submit = SubmitField('Registrarse')
