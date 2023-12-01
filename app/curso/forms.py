from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import (StringField, SubmitField, TextAreaField, BooleanField, RadioField, IntegerField, SelectField, HiddenField)
from wtforms.validators import DataRequired, Length


class CursoForm(FlaskForm):
    numero = StringField('Numero', validators=[DataRequired(), Length(max=5)])
    especialidad = SelectField(u'Especialidad', coerce=int)
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
    submit = SubmitField('Guardar', render_kw={"class":"btn btn-primary"})

class EspecialidadForm(FlaskForm):
    familia = StringField('Familia Profesional', validators=[Length(max=40)])
    codigo = StringField('Codigo', validators=[DataRequired(), Length(max=5)])
    nombre = StringField('Especialidad', validators=[DataRequired(), Length(max=256)])
    nivel = RadioField('Nivel de Estudios', choices=[('nivel 1','Nivel I'),('nivel 2','Nivel II'),('nivel 3','Nivel III'),('sin nivel','Sin Nivel')])
    cert = StringField('Certificación', validators=[Length(max=256)])
    resolucion = StringField('Resolución', validators=[Length(max=40)])
    hcat = StringField('Horas Catedra', validators=[Length(max=4)])
    hreloj = StringField('Horas Reloj', validators=[Length(max=4)])
    requisitos = StringField('Requisitos', validators=[Length(max=128)])
    diseno = StringField('Diseño Curricular', validators=[Length(max=40)])
    reemplaza = TextAreaField('Reemplaza a...')
    submit = SubmitField('Guardar', render_kw={"class":"btn btn-primary"})

class ModuloForm(FlaskForm):
    codigo = StringField('Codigo', validators=[DataRequired(), Length(max=10)])
    nombre = StringField('Especialidad', validators=[DataRequired(), Length(max=256)])
    hcat = StringField('Horas Catedra', validators=[Length(max=4)])
    hreloj = StringField('Horas Reloj', validators=[Length(max=4)])
    especialidad = HiddenField('Especialidad')
    submit = SubmitField('Guardar', render_kw={"class":"btn btn-primary"})