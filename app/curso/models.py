import datetime
from sqlalchemy.exc import IntegrityError

from app import db


class Curso(db.Model):
    __tablename__ = 'curso'
    id = db.Column(db.Integer, primary_key=True)
    numero = db.Column(db.String(5))
    especialidad = db.Column(db.Integer, db.ForeignKey('especialidad.id'))
    content = db.Column(db.Text)
    turno = db.Column(db.String(15))
    lunes = db.Column(db.String(20))
    martes = db.Column(db.String(20))
    miercoles = db.Column(db.String(20))
    jueves = db.Column(db.String(20))
    viernes = db.Column(db.String(20))
    created = db.Column(db.DateTime, default=datetime.datetime.utcnow)
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

class Especialidad(db.Model):
    __tablename__ = 'especialidad'
    id = db.Column(db.Integer, primary_key=True)
    familia = db.Column(db.String(40))
    codigo = db.Column(db.String(5))
    nombre = db.Column(db.String(256), nullable=False)
    nivel = db.Column(db.String(10))
    cert = db.Column(db.String(256), nullable=False)
    resolucion = db.Column(db.String(40))
    hcat = db.Column(db.String(4))
    hreloj = db.Column(db.String(4))
    requisitos = db.Column(db.String(128))
    modulos = db.relationship('Modulo', backref='especialidad_modulo', lazy=True, cascade='all, delete-orphan',
                               order_by='asc(Modulo.codigo)')
    diseno = db.Column(db.String(40))
    reemplaza = db.Column(db.Text)
    created = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    cursos = db.relationship('Curso', backref='especialidad_curso', lazy=True, cascade='all, delete-orphan',
                               order_by='asc(Curso.numero)')

    def __repr__(self):
        return f'<Especialidad {self.nombre}>'

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
    def get_by_familia(familia, page=1, per_page=20):
        return Especialidad.query.filter_by(familia=familia).\
            order_by(Especialidad.created.asc()).paginate(page=page, per_page=per_page, error_out=False)

    @staticmethod
    def get_by_id(id):
        return Especialidad.query.get(id)

    @staticmethod
    def get_all():
        return Especialidad.query.all()

    @staticmethod
    def all_paginated(page=1, per_page=20):
        return Especialidad.query.order_by(Especialidad.codigo.asc()). \
            paginate(page=page, per_page=per_page, error_out=False)
    
    
class Modulo(db.Model):
    __tablename__ = 'modulo'
    id = db.Column(db.Integer, primary_key=True)
    codigo = db.Column(db.String(10))
    nombre = db.Column(db.String(256), nullable=False)
    hcat = db.Column(db.String(4))
    hreloj = db.Column(db.String(4))
    created = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    especialidad_id = db.Column(db.Integer, db.ForeignKey('especialidad.id'), nullable=False)
    
    def __repr__(self):
        return f'<Modulo {self.nombre}>'

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
    def get_by_id(id):
        return Modulo.query.get(id)

    @staticmethod
    def get_all():
        return Modulo.query.all()

    @staticmethod
    def all_paginated(page=1, per_page=20):
        return Modulo.query.order_by(Modulo.created.asc()). \
            paginate(page=page, per_page=per_page, error_out=False)
    
    @staticmethod
    def get_by_especialidad(especialidad_id):
        return Modulo.query.filter_by(especialidad_id=especialidad_id).order_by(Modulo.codigo.asc())