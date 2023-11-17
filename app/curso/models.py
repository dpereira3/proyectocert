import datetime
from sqlalchemy.exc import IntegrityError

from app import db


class Curso(db.Model):
    __tablename__ = 'curso'
    id = db.Column(db.Integer, primary_key=True)
    numero = db.Column(db.String(5))
    especialidad = db.Column(db.String(256), nullable=False)
    content = db.Column(db.Text)
    turno = db.Column(db.String(15))
    lunes = db.Column(db.String(20))
    martes = db.Column(db.String(20))
    miercoles = db.Column(db.String(20))
    jueves = db.Column(db.String(20))
    viernes = db.Column(db.String(20))
    created = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    familia = db.Column(db.String(30))
    image_name = db.Column(db.String)

    def __repr__(self):
        return f'<Curso {self.especialidad}>'

    def save(self):
        if not self.id:
            db.session.add(self)
        
        saved = False
        count = 0
        while not saved:
            try:
                db.session.commit()
                saved = True
            except IntegrityError:
                db.session.rollback()
                db.session.add(self)
                

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @staticmethod
    def get_by_especialidad(especialidad, page=1, per_page=20):
        return Curso.query.filter_by(especialidad=especialidad).\
            order_by(Curso.created.asc()).paginate(page=page, per_page=per_page, error_out=False)

    @staticmethod
    def get_by_id(id):
        return Curso.query.get(id)

    @staticmethod
    def get_all():
        return Curso.query.all()

    @staticmethod
    def all_paginated(page=1, per_page=20):
        return Curso.query.order_by(Curso.created.asc()). \
            paginate(page=page, per_page=per_page, error_out=False)
    
    @staticmethod
    def turno_paginated(turno, page=1, per_page=20):
        return Curso.query.filter_by(turno=turno).order_by(Curso.especialidad.asc()). \
            paginate(page=page, per_page=per_page, error_out=False)

    