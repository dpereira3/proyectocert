from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import (StringField, SubmitField, TextAreaField, BooleanField, RadioField)
from wtforms.validators import DataRequired, Length


class CursoForm(FlaskForm):
    numero = StringField('Numero', validators=[DataRequired(), Length(max=5)])
    especialidad = StringField('Especialidad', validators=[DataRequired(), Length(max=256)])
    content = TextAreaField('Descripción')
    turno = RadioField('Turno', choices=[('mañana','Mañana'),('tarde','Tarde'),('vespertino','Vespertino')])
    lunes = StringField('Lunes', validators=[Length(max=20)])
    martes = StringField('Martes', validators=[Length(max=20)])
    miercoles = StringField('Miercoles', validators=[Length(max=20)])
    jueves = StringField('Jueves', validators=[Length(max=20)])
    viernes = StringField('Viernes', validators=[Length(max=20)])
    post_image = FileField('Imagen de cabecera', validators=[
        FileAllowed(['jpg', 'png'], 'Solo se permiten imágenes')
    ])
    submit = SubmitField('Guardar')

