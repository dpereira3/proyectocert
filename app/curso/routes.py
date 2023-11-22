import logging
import os

from flask import abort, render_template, redirect, url_for, request, current_app
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename

from app.auth.decorators import admin_required
from . import curso_bp
from .forms import CursoForm
from .models import Curso

logger = logging.getLogger(__name__)


@curso_bp.route("/cursos")
def index():
    logger.info('Mostrando los cursos')
    page = int(request.args.get('page', 1))
    per_page = current_app.config['ITEMS_PER_PAGE']
    cursos_pagination = Curso.all_paginated(page, per_page)
    return render_template("cursos.html", cursos_pagination=cursos_pagination)

@curso_bp.route("/especialidad/", methods=['GET', 'POST'])
def buscar_especialidad():
    logger.info('Mostrando una especialidad')
    query = request.args.get('especialidad', '') 
    page = int(request.args.get('page', 1))
    per_page = current_app.config['ITEMS_PER_PAGE']
    especialidadbuscada = Curso.get_by_especialidad(query, page, per_page)
    if not especialidadbuscada:
        logger.info(f'La especialidad {query} no fue encontrada')
        abort(404)
    return render_template("cursos.html", cursos_pagination=especialidadbuscada)

@curso_bp.route("/cursos/turno/<string:turno>/", methods=['GET'])
def buscar_turno(turno):
    logger.info('Mostrando un turno')
    #query = request.args.get('especialidad', '') 
    page = int(request.args.get('page', 1))
    per_page = current_app.config['ITEMS_PER_PAGE']
    turnobuscado = Curso.turno_paginated(turno, page, per_page)
    if not turnobuscado:
        logger.info(f'El turno {turno} no fue encontrado')
        abort(404)
    return render_template("cursos.html", cursos_pagination=turnobuscado)

@curso_bp.route("/curso/<string:id>/", methods=['GET', 'POST'])
def detalles_curso(id):
    logger.info('Mostrando un curso')
    logger.debug(f'Id: {id}')
    curso = Curso.get_by_id(id)
    if not curso:
        logger.info(f'El curso {id} no existe')
        abort(404)
    return render_template("curso_detalle.html", curso=curso)

@curso_bp.route("/admin/curso/", methods=['GET', 'POST'])
@login_required
@admin_required
def curso_form():
    """Crea un nuevo curso"""
    form = CursoForm()
    if form.validate_on_submit():
        numero = form.numero.data
        especialidad = form.especialidad.data
        content = form.content.data
        turno = form.turno.data
        lunes = form.lunes.data
        martes = form.martes.data
        miercoles = form.miercoles.data
        jueves = form.jueves.data
        viernes = form.viernes.data
        file = form.post_image.data
        image_name = None
        # Comprueba si se ha subido un fichero
        if file:
            image_name = secure_filename(file.filename)
            images_dir = current_app.config['POSTS_IMAGES_DIR']
            os.makedirs(images_dir, exist_ok=True)
            file_path = os.path.join(images_dir, image_name)
            file.save(file_path)
        curso = Curso(numero=numero, especialidad=especialidad, content=content, turno=turno, lunes=lunes, martes=martes, miercoles=miercoles,jueves=jueves, viernes=viernes)
        curso.image_name = image_name
        curso.save()
        logger.info(f'Guardando nuevo curso {especialidad}')
        return redirect(url_for('curso.index'))
    return render_template("curso_form.html", form=form)


@curso_bp.route("/admin/curso/<int:curso_id>/", methods=['GET', 'POST'])
@login_required
@admin_required
def update_curso_form(curso_id):
    """Actualiza un post existente"""
    curso = Curso.get_by_id(curso_id)
    if curso is None:
        logger.info(f'El curso {curso_id} no existe')
        abort(404)
    # Crea un formulario inicializando los campos con
    # los valores del post.
    form = CursoForm(obj=curso)
    if form.validate_on_submit():
        # Actualiza los campos del post existente
        curso.numero = form.numero.data
        curso.especialidad = form.especialidad.data
        curso.content = form.content.data
        curso.turno = form.turno.data
        curso.lunes = form.lunes.data
        curso.martes = form.martes.data
        curso.miercoles = form.miercoles.data
        curso.jueves = form.jueves.data
        curso.viernes = form.viernes.data
        file = form.post_image.data
        # Comprueba si se ha subido un fichero
        if file:
            image_name = secure_filename(file.filename)
            images_dir = current_app.config['POSTS_IMAGES_DIR']
            os.makedirs(images_dir, exist_ok=True)
            file_path = os.path.join(images_dir, image_name)
            file.save(file_path)
            curso.image_name = image_name
        curso.save()
        logger.info(f'Guardando el curso {curso_id}')
        return redirect(url_for('curso.index'))
    return render_template("curso_form.html", form=form, curso=curso)


@curso_bp.route("/admin/curso/delete/<int:curso_id>/", methods=['POST'])
@login_required
@admin_required
def delete_curso(curso_id):
    logger.info(f'Se va a eliminar el curso {curso_id}')
    curso = Curso.get_by_id(curso_id)
    if curso is None:
        logger.info(f'El curso {curso_id} no existe')
        abort(404)
    curso.delete()
    logger.info(f'El curso {curso_id} ha sido eliminado')
    return redirect(url_for('curso.index'))

