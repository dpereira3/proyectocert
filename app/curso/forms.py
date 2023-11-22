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

class EspecialidadForm(FlaskForm):
    familia = StringField('Familia Profesional', validators=[Length(max=20)])
    codigo = StringField('Codigo', validators=[DataRequired(), Length(max=5)])
    nombre = StringField('Especialidad', validators=[DataRequired(), Length(max=256)])
    nivel = RadioField('Nivel de Estudios', choices=[('mañana','Mañana'),('tarde','Tarde'),('vespertino','Vespertino')])
    cert = StringField('Certificación', validators=[Length(max=20)])
    resolucion = StringField('Resolución', validators=[Length(max=20)])
    hcat = StringField('Horas Catedra', validators=[Length(max=20)])
    hreloj = StringField('Horas Reloj', validators=[Length(max=20)])
    requisitos = StringField('Requisitos', validators=[Length(max=20)])
    diseno = StringField('Diseño Curricular', validators=[Length(max=20)])
    reemplaza = TextAreaField('Reemplaza a...')
