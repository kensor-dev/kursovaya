from sqlalchemy.orm import Session
from . import models, schemas

def create_student(db: Session, student: schemas.StudentCreate):
    db_student = models.Student(**student.model_dump())
    db.add(db_student)
    db.commit()
    db.refresh(db_student)
    return db_student

def get_students(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Student).offset(skip).limit(limit).all()

def get_student(db: Session, student_id: int):
    return db.query(models.Student).filter(models.Student.student_id == student_id).first()

def update_student(db: Session, student_id: int, student: schemas.StudentCreate):
    db_student = get_student(db, student_id)
    if db_student:
        for key, value in student.model_dump().items():
            setattr(db_student, key, value)
        db.commit()
        db.refresh(db_student)
    return db_student

def delete_student(db: Session, student_id: int):
    db_student = get_student(db, student_id)
    if db_student:
        db.delete(db_student)
        db.commit()
    return db_student

def create_teacher(db: Session, teacher: schemas.TeacherCreate):
    db_teacher = models.Teacher(**teacher.model_dump())
    db.add(db_teacher)
    db.commit()
    db.refresh(db_teacher)
    return db_teacher

def get_teachers(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Teacher).offset(skip).limit(limit).all()

def get_teacher(db: Session, teacher_id: int):
    return db.query(models.Teacher).filter(models.Teacher.teacher_id == teacher_id).first()

def update_teacher(db: Session, teacher_id: int, teacher: schemas.TeacherCreate):
    db_teacher = get_teacher(db, teacher_id)
    if db_teacher:
        for key, value in teacher.model_dump().items():
            setattr(db_teacher, key, value)
        db.commit()
        db.refresh(db_teacher)
    return db_teacher

def delete_teacher(db: Session, teacher_id: int):
    db_teacher = get_teacher(db, teacher_id)
    if db_teacher:
        db.delete(db_teacher)
        db.commit()
    return db_teacher

def create_subject(db: Session, subject: schemas.SubjectCreate):
    db_subject = models.Subject(**subject.model_dump())
    db.add(db_subject)
    db.commit()
    db.refresh(db_subject)
    return db_subject

def get_subjects(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Subject).offset(skip).limit(limit).all()

def get_subject(db: Session, subject_id: int):
    return db.query(models.Subject).filter(models.Subject.subject_id == subject_id).first()

def update_subject(db: Session, subject_id: int, subject: schemas.SubjectCreate):
    db_subject = get_subject(db, subject_id)
    if db_subject:
        for key, value in subject.model_dump().items():
            setattr(db_subject, key, value)
        db.commit()
        db.refresh(db_subject)
    return db_subject

def delete_subject(db: Session, subject_id: int):
    db_subject = get_subject(db, subject_id)
    if db_subject:
        db.delete(db_subject)
        db.commit()
    return db_subject

def create_class(db: Session, school_class: schemas.SchoolClassCreate):
    db_class = models.SchoolClass(**school_class.model_dump())
    db.add(db_class)
    db.commit()
    db.refresh(db_class)
    return db_class

def get_classes(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.SchoolClass).offset(skip).limit(limit).all()

def get_class(db: Session, class_id: int):
    return db.query(models.SchoolClass).filter(models.SchoolClass.class_id == class_id).first()

def update_class(db: Session, class_id: int, school_class: schemas.SchoolClassCreate):
    db_class = get_class(db, class_id)
    if db_class:
        for key, value in school_class.model_dump().items():
            setattr(db_class, key, value)
        db.commit()
        db.refresh(db_class)
    return db_class

def delete_class(db: Session, class_id: int):
    db_class = get_class(db, class_id)
    if db_class:
        db.delete(db_class)
        db.commit()
    return db_class

def create_parent(db: Session, parent: schemas.ParentCreate):
    db_parent = models.Parent(**parent.model_dump())
    db.add(db_parent)
    db.commit()
    db.refresh(db_parent)
    return db_parent

def get_parents(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Parent).offset(skip).limit(limit).all()

def get_parent(db: Session, parent_id: int):
    return db.query(models.Parent).filter(models.Parent.parent_id == parent_id).first()

def update_parent(db: Session, parent_id: int, parent: schemas.ParentCreate):
    db_parent = get_parent(db, parent_id)
    if db_parent:
        for key, value in parent.model_dump().items():
            setattr(db_parent, key, value)
        db.commit()
        db.refresh(db_parent)
    return db_parent

def delete_parent(db: Session, parent_id: int):
    db_parent = get_parent(db, parent_id)
    if db_parent:
        db.delete(db_parent)
        db.commit()
    return db_parent

def create_grade(db: Session, grade: schemas.GradeCreate):
    db_grade = models.Grade(**grade.model_dump())
    db.add(db_grade)
    db.commit()
    db.refresh(db_grade)
    return db_grade

def get_grades(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Grade).offset(skip).limit(limit).all()

def get_grade(db: Session, grade_id: int):
    return db.query(models.Grade).filter(models.Grade.grade_id == grade_id).first()

def update_grade(db: Session, grade_id: int, grade: schemas.GradeCreate):
    db_grade = get_grade(db, grade_id)
    if db_grade:
        for key, value in grade.model_dump().items():
            setattr(db_grade, key, value)
        db.commit()
        db.refresh(db_grade)
    return db_grade

def delete_grade(db: Session, grade_id: int):
    db_grade = get_grade(db, grade_id)
    if db_grade:
        db.delete(db_grade)
        db.commit()
    return db_grade
