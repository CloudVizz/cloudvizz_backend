from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Resource(db.Model):
    __tablename__ = 'resources'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    resource_id = db.Column(db.String, unique=True, nullable=False)
    resource_type = db.Column(db.String, nullable=False)
    region = db.Column(db.String, nullable=False)
    details = db.Column(db.JSON, nullable=False)
