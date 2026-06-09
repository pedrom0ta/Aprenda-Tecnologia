from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length, Optional, URL, ValidationError
import re

def validar_youtube(form, field):
    url = field.data or ''
    patterns = [
        r'(?:v=)([a-zA-Z0-9_-]{11})',
        r'(?:youtu\.be/)([a-zA-Z0-9_-]{11})',
        r'(?:embed/)([a-zA-Z0-9_-]{11})',
        r'(?:shorts/)([a-zA-Z0-9_-]{11})',
    ]
    for pattern in patterns:
        if re.search(pattern, url):
            return
    raise ValidationError('URL inválida. Cole um link do YouTube válido (ex: https://www.youtube.com/watch?v=...)')

class LoginForm(FlaskForm):
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    senha = PasswordField('Senha', validators=[DataRequired()])
    submit = SubmitField('Entrar')

class VideoAulaForm(FlaskForm):
    titulo = StringField('Título', validators=[DataRequired(), Length(min=3, max=200)])
    descricao = TextAreaField('Descrição', validators=[DataRequired(), Length(min=10)])
    categoria_id = SelectField('Categoria', coerce=int, validators=[DataRequired()])
    youtube_url = StringField('Link do YouTube', validators=[DataRequired(), validar_youtube])
    submit = SubmitField('Salvar')

class CategoriaForm(FlaskForm):
    nome = StringField('Nome', validators=[DataRequired(), Length(min=2, max=100)])
    descricao = TextAreaField('Descrição', validators=[Optional()])
    icone = StringField('Ícone Bootstrap (ex: bi-cpu)', validators=[Optional(), Length(max=50)])
    submit = SubmitField('Salvar')
