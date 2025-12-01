import pytest
from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient

from app.database import Base
from app.main import app
from app.deps import get_db

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

@event.listens_for(engine, "connect")
def set_sqlite_pragma(dbapi_conn, connection_record):
    cursor = dbapi_conn.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="function")
def db_session():
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="function")
def client(db_session):
    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    app.dependency_overrides.clear()

@pytest.fixture
def sample_parent(db_session):
    from app import models
    parent = models.Parent(
        full_name="Иванов Иван Иванович",
        contact_info="ivan@example.com",
        student_relation="Отец"
    )
    db_session.add(parent)
    db_session.commit()
    db_session.refresh(parent)
    return parent

@pytest.fixture
def sample_teacher(db_session):
    from app import models
    teacher = models.Teacher(
        full_name="Петрова Мария Сергеевна",
        contact_info="maria@school.com",
        position="Учитель математики"
    )
    db_session.add(teacher)
    db_session.commit()
    db_session.refresh(teacher)
    return teacher

@pytest.fixture
def sample_subject(db_session, sample_teacher):
    from app import models
    subject = models.Subject(
        name="Математика",
        description="Алгебра и геометрия",
        teacher_id=sample_teacher.teacher_id
    )
    db_session.add(subject)
    db_session.commit()
    db_session.refresh(subject)
    return subject

@pytest.fixture
def sample_class(db_session, sample_teacher):
    from app import models
    school_class = models.SchoolClass(
        number_letter="9А",
        class_teacher_id=sample_teacher.teacher_id
    )
    db_session.add(school_class)
    db_session.commit()
    db_session.refresh(school_class)
    return school_class

@pytest.fixture
def sample_student(db_session, sample_class, sample_parent):
    from app import models
    from datetime import date
    student = models.Student(
        full_name="Сидоров Петр Иванович",
        date_of_birth=date(2008, 5, 15),
        class_id=sample_class.class_id,
        contact_info="petr@example.com",
        additional_info="Хорошо учится",
        parent_id=sample_parent.parent_id
    )
    db_session.add(student)
    db_session.commit()
    db_session.refresh(student)
    return student

@pytest.fixture
def sample_grade(db_session, sample_student, sample_subject, sample_teacher):
    from app import models
    from datetime import date
    grade = models.Grade(
        student_id=sample_student.student_id,
        subject_id=sample_subject.subject_id,
        teacher_id=sample_teacher.teacher_id,
        grade="5",
        date_issued=date.today(),
        comment="Отлично"
    )
    db_session.add(grade)
    db_session.commit()
    db_session.refresh(grade)
    return grade
