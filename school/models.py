from datetime import datetime
from sqlalchemy import (
    Column, Integer, String, Date, DateTime, Text, Float, ForeignKey, Boolean
)
from sqlalchemy.orm import relationship
from .db import Base


class Student(Base):
    __tablename__ = 'students'

    student_id = Column('id', Integer, primary_key=True, nullable=False)
    first_name = Column('first_name', String(length=64), nullable=False)
    last_name = Column('last_name', String(length=64), nullable=False)
    birthdate = Column('birthdate', Date, nullable=False)
    gender = Column('gender', String(length=20), nullable=False)
    bio = Column('bio', Text)
    gpa = Column('gpa', Float, nullable=False)
    certificates = relationship("Certificate", back_populates="student")

    scores = relationship('Score', back_populates='student')

    created_at = Column('created_at', DateTime, default=datetime.now)
    updated_at = Column('updated_at', DateTime, default=datetime.now, onupdate=datetime.now)

    def __str__(self):
        return f'Student(id={self.student_id}, name="{self.first_name} {self.last_name}")'

    def __repr__(self):
        return f'Student(id={self.student_id}, name="{self.first_name} {self.last_name}")'
    
    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'


class Score(Base):
    __tablename__ = 'scores'

    score_id = Column('id', Integer, primary_key=True, nullable=False)
    subject = Column('subject', String(length=64), nullable=False)
    ball = Column('ball', Float, nullable=False)
    student_id = Column('student_id', ForeignKey('students.id', ondelete='CASCADE'))

    student = relationship('Student', back_populates='scores')

    def __str__(self):
        return f'Score(id={self.score_id}, name="{self.subject}", ball={self.ball}, student={self.student_id})'

    def __repr__(self):
        return f'Score(id={self.score_id}, name="{self.subject}", ball={self.ball}, student={self.student_id})'
class Certificate(Base):
    __tablename__ = "certificates"
    id = Column(Integer, primary_key=True)
    title = Column(String)
    content = Column(String)
    certificate_code = Column(String)
    issued_ad = Column(DateTime)
    is_verified = Column(Boolean, default=False)
    student_id = Column(Integer, ForeignKey("students.id"))
    student = relationship("Student", back_populates="certificates")