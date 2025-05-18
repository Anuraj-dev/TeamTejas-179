from datetime import datetime
from ..extensions import db

class BaseModel(db.Model):
    """Base model class that all other models will inherit from"""
    __abstract__ = True

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
