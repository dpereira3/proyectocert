import logging
import os

from flask import abort, render_template, redirect, url_for, request, current_app
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename

from app.auth.decorators import admin_required
from app.auth.models import User
from . import curso_bp
from .forms import CursoForm, EspecialidadForm  
from .models import Curso, Especialidad, Modulo

logger = logging.getLogger(__name__)


@curso_bp.route("/cursos")
def index():
    logger.info('Mostrando los cursos')
    page = int(request.args.get('page', 1))
    per_page = current_app.config['ITEMS_PER_PAGE']
    cursos_pagination = Curso.all_paginated(page, per_page)
    return render_template("cursos.html", cursos_pagination=cursos_pagination)

@curso_bp.route("/cursos/especialidad/", methods=['GET', 'POST'])
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
    form.especialidad.choices = [(g.id, g.nombre) for g in Especialidad.query.order_by('nombre')]
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
    """Actualiza un curso existente"""
    curso = Curso.get_by_id(curso_id)
    if curso is None:
        logger.info(f'El curso {curso_id} no existe')
        abort(404)
    # Crea un formulario inicializando los campos con
    # los valores del post.
    form = CursoForm(obj=curso)
    form.especialidad.choices = [(g.id, g.nombre) for g in Especialidad.query.order_by('nombre')]
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


@curso_bp.route("/admin/curso/delete/<int:curso_id>/", methods=['POST', ])
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

"""    ESPECIALIDADES    """

@curso_bp.route("/especialidades")
def especialidades():
    logger.info('Mostrando las especialidades')
    page = int(request.args.get('page', 1))
    per_page = current_app.config['ITEMS_PER_PAGE']
    especialidad_pagination = Especialidad.all_paginated(page, per_page)
    return render_template("especialidades.html", especialidad_pagination=especialidad_pagination)

@curso_bp.route("/especialidad/familia/<string:familia>", methods=['GET', 'POST'])
def buscar_familia():
    logger.info('Mostrando una familia')
    query = request.args.get('familia', '') 
    page = int(request.args.get('page', 1))
    per_page = current_app.config['ITEMS_PER_PAGE']
    familiabuscada = Especialidad.get_by_familia(query, page, per_page)
    if not familiabuscada:
        logger.info(f'La familia {query} no fue encontrada')
        abort(404)
    return render_template("especialidades.html", cursos_pagination=familiabuscada)

@curso_bp.route("/especialidad/<string:id>/", methods=['GET', 'POST'])
def detalles_especialidad(id):
    logger.info('Mostrando una especialidad')
    logger.debug(f'Id: {id}')
    especialidad = Especialidad.get_by_id(id)
    if not especialidad:
        logger.info(f'La especialidad {id} no existe')
        abort(404)
    return render_template("especialidad_detalle.html", especialidad=especialidad)

@curso_bp.route("/admin/especialidad/", methods=['GET', 'POST'])
@login_required
@admin_required
def especialidad_form():
    """Crea un nueva especialidad"""
    form = EspecialidadForm()
    if form.validate_on_submit():
        familia = form.familia.data
        codigo = form.codigo.data
        nombre = form.nombre.data
        nivel = form.nivel.data
        cert = form.cert.data
        resolucion = form.resolucion.data
        hcat = form.hcat.data
        hreloj = form.hreloj.data
        requisitos = form.requisitos.data
        diseno = form.diseno.data
        reemplaza = form.reemplaza.data

        especialidad = Especialidad(familia=familia, codigo=codigo, nombre=nombre, nivel=nivel, cert=cert, resolucion=resolucion, hcat=hcat, hreloj=hreloj, requisitos=requisitos, diseno=diseno, reemplaza=reemplaza)
       
        especialidad.save()
        logger.info(f'Guardando nueva especialidad {especialidad}')
        return redirect(url_for('curso.especialidades'))
    return render_template("especialidad_form.html", form=form)


@curso_bp.route("/admin/especialidad/<int:especialidad_id>/", methods=['GET', 'POST'])
@login_required
@admin_required
def update_especialidad_form(especialidad_id):
    """Actualiza una especialidad existente"""
    especialidad = Especialidad.get_by_id(especialidad_id)
    if especialidad is None:
        logger.info(f'La especialidad {especialidad_id} no existe')
        abort(404)
    # Crea un formulario inicializando los campos con
    # los valores del post.
    form = EspecialidadForm(obj=especialidad)
    if form.validate_on_submit():
        # Actualiza los campos del post existente
        especialidad.numero = form.numero.data
        especialidad.especialidad = form.especialidad.data
        especialidad.content = form.content.data
        especialidad.turno = form.turno.data
        especialidad.lunes = form.lunes.data
        especialidad.martes = form.martes.data
        especialidad.miercoles = form.miercoles.data
        especialidad.jueves = form.jueves.data
        especialidad.viernes = form.viernes.data
        
        especialidad.save()
        logger.info(f'Guardando la especialidad {especialidad_id}')
        return redirect(url_for('especialidad.index'))
    return render_template("especialidad_form.html", form=form, especialidad=especialidad)


@curso_bp.route("/admin/especialidad/delete/<int:especialidad_id>/", methods=['POST', ])
@login_required
@admin_required
def delete_especialidad(especialidad_id):
    logger.info(f'Se va a eliminar la especialidad {especialidad_id}')
    especialidad = Especialidad.get_by_id(especialidad_id)
    if especialidad is None:
        logger.info(f'La especialidad {especialidad_id} no existe')
        abort(404)
    especialidad.delete()
    logger.info(f'La especialidad {especialidad_id} ha sido eliminado')
    return redirect(url_for('especialidad.index'))
