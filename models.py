from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

class SearchHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    topic = db.Column(db.String(200))
    notes = db.Column(db.Text)
    formulas = db.Column(db.Text)
    mindmap = db.Column(db.Text)
    mcq = db.Column(db.Text)  # Add this for MCQ responses
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'topic': self.topic,
            'notes': self.notes,
            'formulas': self.formulas,
            'mindmap': self.mindmap,
            'mcq': self.mcq,
            'timestamp': self.timestamp.strftime('%Y-%m-%d %H:%M')
        }
