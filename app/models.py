from . import db
from datetime import datetime

class Meal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    description = db.Column(db.String(200))
    date_time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    in_diet = db.Column(db.Boolean, nullable=False)
    
    def __repr__(self):
        return f'<Meal {self.name}>'

