from app import db


class Curso(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    especialidad = db.Column(db.String(256), nullable=False)
    content = db.Column(db.Text)
    created = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    icon = db.Column(db.String)
    