from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length, Email, EqualTo
from wtforms import ValidationError
from ..models import Usuario

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Length(1, 64), Email()], render_kw={"placeholder": "Correo electrónico"})
    password = PasswordField('Contraseña', validators=[DataRequired()], render_kw={"placeholder": "Contraseña"})
    remember_me = BooleanField('Mantener sesión abierta')
    submit = SubmitField('Iniciar Sesión')


class SignupForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Length(1, 64), Email()])
    password = PasswordField('Contraseña', validators=[DataRequired(), EqualTo('confirm_password', message='Las contraseñas deben coincidir')])
    confirm_password = PasswordField('Confirmar contraseña', validators=[DataRequired()])
    submit = SubmitField('Registrarse')

    def validate_email(self, field):
        if Usuario.query.filter_by(correo=field.data).first():
            raise ValidationError('La dirección de correo electrónico ya se encuentra en uso')



    
