from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from . import models, schemas, crud
from .database import engine, Base
from .deps import get_db

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Учёт успеваемости - API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"msg": "Kursovaya API alive"}

@app.post("/students/", response_model=schemas.StudentOut)
def create_student(student: schemas.StudentCreate, db: Session = Depends(get_db)):
    return crud.create_student(db=db, student=student)

@app.get("/students/", response_model=list[schemas.StudentOut])
def list_students(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_students(db=db, skip=skip, limit=limit)

@app.post("/grades/", response_model=schemas.GradeOut)
def create_grade(grade: schemas.GradeCreate, db: Session = Depends(get_db)):
    return crud.create_grade(db=db, grade=grade)

@app.get("/teachers/", response_model=list[schemas.TeacherOut])
def list_teachers(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_teachers(db=db, skip=skip, limit=limit)

@app.post("/teachers/", response_model=schemas.TeacherOut)
def create_teacher(teacher: schemas.TeacherCreate, db: Session = Depends(get_db)):
    return crud.create_teacher(db=db, teacher=teacher)


@app.get("/students/{student_id}", response_model=schemas.StudentOut)
def get_student(student_id: int, db: Session = Depends(get_db)):
    db_student = crud.get_student(db, student_id)
    if not db_student:
        raise HTTPException(status_code=404, detail="Student not found")
    return db_student

@app.put("/students/{student_id}", response_model=schemas.StudentOut)
def update_student(student_id: int, student: schemas.StudentCreate, db: Session = Depends(get_db)):
    db_student = crud.update_student(db, student_id, student)
    if not db_student:
        raise HTTPException(status_code=404, detail="Student not found")
    return db_student

@app.delete("/students/{student_id}")
def delete_student(student_id: int, db: Session = Depends(get_db)):
    db_student = crud.delete_student(db, student_id)
    if not db_student:
        raise HTTPException(status_code=404, detail="Student not found")
    return {"msg": "Student deleted"}

@app.post("/teachers/", response_model=schemas.TeacherOut)
def create_teacher(teacher: schemas.TeacherCreate, db: Session = Depends(get_db)):
    return crud.create_teacher(db=db, teacher=teacher)

@app.get("/teachers/", response_model=list[schemas.TeacherOut])
def list_teachers(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_teachers(db=db, skip=skip, limit=limit)

@app.get("/teachers/{teacher_id}", response_model=schemas.TeacherOut)
def get_teacher(teacher_id: int, db: Session = Depends(get_db)):
    db_teacher = crud.get_teacher(db, teacher_id)
    if not db_teacher:
        raise HTTPException(status_code=404, detail="Teacher not found")
    return db_teacher

@app.put("/teachers/{teacher_id}", response_model=schemas.TeacherOut)
def update_teacher(teacher_id: int, teacher: schemas.TeacherCreate, db: Session = Depends(get_db)):
    db_teacher = crud.update_teacher(db, teacher_id, teacher)
    if not db_teacher:
        raise HTTPException(status_code=404, detail="Teacher not found")
    return db_teacher

@app.delete("/teachers/{teacher_id}")
def delete_teacher(teacher_id: int, db: Session = Depends(get_db)):
    db_teacher = crud.delete_teacher(db, teacher_id)
    if not db_teacher:
        raise HTTPException(status_code=404, detail="Teacher not found")
    return {"msg": "Teacher deleted"}

@app.post("/subjects/", response_model=schemas.SubjectOut)
def create_subject(subject: schemas.SubjectCreate, db: Session = Depends(get_db)):
    return crud.create_subject(db=db, subject=subject)

@app.get("/subjects/", response_model=list[schemas.SubjectOut])
def list_subjects(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_subjects(db=db, skip=skip, limit=limit)

@app.get("/subjects/{subject_id}", response_model=schemas.SubjectOut)
def get_subject(subject_id: int, db: Session = Depends(get_db)):
    db_subject = crud.get_subject(db, subject_id)
    if not db_subject:
        raise HTTPException(status_code=404, detail="Subject not found")
    return db_subject

@app.put("/subjects/{subject_id}", response_model=schemas.SubjectOut)
def update_subject(subject_id: int, subject: schemas.SubjectCreate, db: Session = Depends(get_db)):
    db_subject = crud.update_subject(db, subject_id, subject)
    if not db_subject:
        raise HTTPException(status_code=404, detail="Subject not found")
    return db_subject

@app.delete("/subjects/{subject_id}")
def delete_subject(subject_id: int, db: Session = Depends(get_db)):
    db_subject = crud.delete_subject(db, subject_id)
    if not db_subject:
        raise HTTPException(status_code=404, detail="Subject not found")
    return {"msg": "Subject deleted"}

@app.post("/classes/", response_model=schemas.SchoolClassOut)
def create_class(school_class: schemas.SchoolClassCreate, db: Session = Depends(get_db)):
    return crud.create_class(db=db, school_class=school_class)

@app.get("/classes/", response_model=list[schemas.SchoolClassOut])
def list_classes(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_classes(db=db, skip=skip, limit=limit)

@app.get("/classes/{class_id}", response_model=schemas.SchoolClassOut)
def get_class(class_id: int, db: Session = Depends(get_db)):
    db_class = crud.get_class(db, class_id)
    if not db_class:
        raise HTTPException(status_code=404, detail="Class not found")
    return db_class

@app.put("/classes/{class_id}", response_model=schemas.SchoolClassOut)
def update_class(class_id: int, school_class: schemas.SchoolClassCreate, db: Session = Depends(get_db)):
    db_class = crud.update_class(db, class_id, school_class)
    if not db_class:
        raise HTTPException(status_code=404, detail="Class not found")
    return db_class

@app.delete("/classes/{class_id}")
def delete_class(class_id: int, db: Session = Depends(get_db)):
    db_class = crud.delete_class(db, class_id)
    if not db_class:
        raise HTTPException(status_code=404, detail="Class not found")
    return {"msg": "Class deleted"}

@app.post("/parents/", response_model=schemas.ParentOut)
def create_parent(parent: schemas.ParentCreate, db: Session = Depends(get_db)):
    return crud.create_parent(db=db, parent=parent)

@app.get("/parents/", response_model=list[schemas.ParentOut])
def list_parents(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_parents(db=db, skip=skip, limit=limit)

@app.get("/parents/{parent_id}", response_model=schemas.ParentOut)
def get_parent(parent_id: int, db: Session = Depends(get_db)):
    db_parent = crud.get_parent(db, parent_id)
    if not db_parent:
        raise HTTPException(status_code=404, detail="Parent not found")
    return db_parent

@app.put("/parents/{parent_id}", response_model=schemas.ParentOut)
def update_parent(parent_id: int, parent: schemas.ParentCreate, db: Session = Depends(get_db)):
    db_parent = crud.update_parent(db, parent_id, parent)
    if not db_parent:
        raise HTTPException(status_code=404, detail="Parent not found")
    return db_parent

@app.delete("/parents/{parent_id}")
def delete_parent(parent_id: int, db: Session = Depends(get_db)):
    db_parent = crud.delete_parent(db, parent_id)
    if not db_parent:
        raise HTTPException(status_code=404, detail="Parent not found")
    return {"msg": "Parent deleted"}

@app.get("/grades/", response_model=list[schemas.GradeOut])
def list_grades(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_grades(db=db, skip=skip, limit=limit)

@app.get("/grades/{grade_id}", response_model=schemas.GradeOut)
def get_grade(grade_id: int, db: Session = Depends(get_db)):
    db_grade = crud.get_grade(db, grade_id)
    if not db_grade:
        raise HTTPException(status_code=404, detail="Grade not found")
    return db_grade

@app.put("/grades/{grade_id}", response_model=schemas.GradeOut)
def update_grade(grade_id: int, grade: schemas.GradeCreate, db: Session = Depends(get_db)):
    db_grade = crud.update_grade(db, grade_id, grade)
    if not db_grade:
        raise HTTPException(status_code=404, detail="Grade not found")
    return db_grade

@app.delete("/grades/{grade_id}")
def delete_grade(grade_id: int, db: Session = Depends(get_db)):
    db_grade = crud.delete_grade(db, grade_id)
    if not db_grade:
        raise HTTPException(status_code=404, detail="Grade not found")
    return {"msg": "Grade deleted"}
