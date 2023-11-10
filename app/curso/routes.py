import logging

from flask import abort, render_template, redirect, url_for, request, current_app
from flask_login import current_user


from . import curso_bp
#from .forms import CommentForm

logger = logging.getLogger(__name__)


@curso_bp.route("/cursos")
def index():
    logger.info('Mostrando los cursos')
    # page = int(request.args.get('page', 1))
    # per_page = current_app.config['ITEMS_PER_PAGE']
    # post_pagination = Post.all_paginated(page, per_page)
    return render_template("cursos.html",)