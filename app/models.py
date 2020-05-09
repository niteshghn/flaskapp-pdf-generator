from enum import Enum
from app import db
from sqlalchemy.sql import func

db.Table('question_video',
         db.Column('question_id', db.Integer, db.ForeignKey('catalog_questions.id')),
         db.Column('video_id', db.Integer, db.ForeignKey('videos.id'))
         )


class LevelEnum(Enum):
    easy = 'easy'
    medium = 'medium'
    hard = 'hard'


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    questions_asked = db.relationship('UserQuestion', backref='student', lazy='dynamic')
    last_seen = db.Column(db.DateTime(timezone=True))

    def __repr__(self):
        return '<User {}>'.format(self.username)

    @property
    def serialize(self):
        """Return object data in easily serializable format"""
        return {
            'id': self.id,
            'created_at': self.created_at,
            'question_asked': [q.serialize for q in self.question_asked],
            'email': self.email
        }


class Question(db.Model):
    __tablename__ = 'catalog_questions'
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.Text)
    level = db.Column(db.Enum(LevelEnum))
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    videos = db.relationship('Video', secondary='question_video', backref='questions', lazy='dynamic')

    def __repr__(self):
        return '<Question {}>'.format(self.question)

    @property
    def serialize(self):
        """Return object data in easily serializable format"""
        return {
            'id': self.id,
            'created_at': self.created_at,
            'question': self.question
        }


class UserQuestion(db.Model):
    __tablename__ = 'user_asked_question'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    question_id = db.Column(db.ForeignKey('user.id'))
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    last_video = db.Column(db.ForeignKey('video.id'))

    @property
    def serialize(self):
        """Return object data in easily serializable format"""
        return {
            'id': self.id,
            'created_at': self.created_at,
            'question_id': self.question_id,
            'user_id': self.user_id
        }


class Video(db.Model):
    __tablename__ = 'videos'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, index=True)
