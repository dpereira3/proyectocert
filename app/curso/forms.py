from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import (StringField, SubmitField, TextAreaField, BooleanField)
from wtforms.validators import DataRequired, Length


class CursoForm(FlaskForm):
    especialidad = StringField('Especialidad', validators=[DataRequired(), Length(max=256)])
    content = TextAreaField('Descripción')
    post_image = FileField('Imagen de cabecera', validators=[
        FileAllowed(['jpg', 'png'], 'Solo se permiten imágenes')
    ])
    submit = SubmitField('Guardar')

