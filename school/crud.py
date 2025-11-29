from datetime import datetime
from sqlalchemy import or_, not_, and_
from .models import Student, Score , Certificate 
from .db import get_db
import uuid


def create_student(first_name: str, last_name: str, birthdate: datetime, bio: str | None = None):
    student = Student(
        first_name=first_name,
        last_name=last_name,
        birthdate=birthdate,
        bio=bio
    )
    
    with get_db() as session:
        session.add(student)
        session.commit()

def get_students() -> list[Student]:
    with get_db() as session:
        students = session.query(Student).all()
    
    return students

def get_one_student(student_id: int) -> Student | None:
    with get_db() as session:
        student = session.query(Student).get(student_id)
    
    return student

def search_students_by_first_name(first_name: str) -> list[Student]:
    with get_db() as session:
        students = session.query(Student).filter(Student.first_name==first_name).all()
    
    return students

def search_students_by_name(name: str) -> list[Student]:
    with get_db() as session:
        students = session.query(Student).filter(
            or_(Student.first_name.like(f'%{name}%'), Student.last_name.like(f'%{name}%'))
        ).all()
    
    return students

def update_student(
    student_id: int | None = None,
    first_name: str | None = None, 
    last_name: str | None = None, 
    birthdate: datetime | None = None, 
    bio: str | None = None
):
    student = get_one_student(student_id)

    if student:
        with get_db() as session:
            student.first_name = first_name if first_name else student.first_name
            student.last_name = last_name if last_name else student.last_name
            student.birthdate = birthdate if birthdate else student.birthdate
            student.bio = bio if bio else student.bio

            session.add(student)
            session.commit()

def delete_student(student_id: int):
    student = get_one_student(student_id)

    if student:
        with get_db() as session:
            session.delete(student)
            session.commit()

def filter_students_by_gender(gender: str) -> list[Student]:
    with get_db() as session:
        # result = session.query(Student).filter(Student.gender==gender).all()
        result = session.query(Student).filter_by(gender=gender).all()

    return result

def filter_students_by_gpa(min_gpa: float, max_gpa: float) -> list[Student]:
    with get_db() as session:
        # result = session.query(Student).filter(Student.gpa >= min_gpa, Student.gpa <= max_gpa).all()
        result = session.query(Student).filter(Student.gpa.between(min_gpa, max_gpa)).all() # between

    return result

def get_sorted_students_by_gpa(by: str = 'asc') -> list[Student]:
    with get_db() as session:
        if by == 'asc':
            result = session.query(Student).order_by(Student.gpa.asc())
        else:
            result = session.query(Student).order_by(Student.gpa.desc())
            
    return result

def add_score(student_id: int, subject: str, ball: float):
    with get_db() as session:
        student: Student = session.query(Student).get(student_id)
        student.scores.append(Score(subject=subject, ball=ball))
        session.commit()

def get_scores(student_id: int) -> list[Score]:
    with get_db() as session:
        student: Student = session.query(Student).get(student_id)
        return student.scores
    
def get_student_with_scores():
    with get_db() as session:
        students: list[Student] = session.query(Student).all()

        result = []
        for student in students:
            result.append({
                'student': student.full_name,
                'total_scores': len(student.scores)
            })
    
    return result
def add_certificate(student_id: int, title: str, content: str, issued_ad):
    with get_db() as session:
        student: Student = session.query(Student).get(student_id)
        code = str(uuid.uuid4())[:8]   
        student.certificates.append(
            Certificate (
                title=title,
                content=content,
                certificate_code=code,
                issued_ad=issued_ad
            )
        )
        session.commit()
def verify_certificate(code: str):
    with get_db() as session:
        cert = session.query(Certificate).filter(Certificate.certificate_code == code)\
                      .first()
        if cert:
            cert.is_verified = True
            session.commit()

        return cert
def get_verified_count():
    with get_db() as session:
        return session.query(Certificate).filter_by(is_verified=True).count()
def get_last_5_certificates():
    with get_db() as session:
        return session.query(Certificate).order_by(Certificate.issued_ad.desc())\
                      .limit(5).all()
def get_certificate_counts_by_student():
    with get_db() as session:
        students = session.query(Student).all()
        results = [(student.full_name, len(student.certificates)) for student in students]
        return results
def get_top_certificate_student():
    with get_db() as session:
        students = session.query(Student).all()
        max_count = 0
        top_student = None
        for student in students:
            total = session.query(Certificate).filter_by(student_id=student.id).count()
            if total > max_count:
                max_count = total
                top_student = student
        if top_student:
            return (top_student.full_name, max_count)
        return None