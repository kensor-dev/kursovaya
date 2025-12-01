import pytest
from datetime import date
from app import models

@pytest.mark.unit
class TestParentModel:
    def test_create_parent_with_valid_data(self, db_session):
        parent = models.Parent(
            full_name="Иванов Иван Иванович",
            contact_info="ivan@example.com",
            student_relation="Отец"
        )
        db_session.add(parent)
        db_session.commit()
        db_session.refresh(parent)

        assert parent.parent_id is not None
        assert parent.full_name == "Иванов Иван Иванович"
        assert parent.contact_info == "ivan@example.com"
        assert parent.student_relation == "Отец"

    def test_parent_full_name_required(self, db_session):
        parent = models.Parent(contact_info="ivan@example.com")
        db_session.add(parent)

        with pytest.raises(Exception):
            db_session.commit()

    def test_parent_student_relationship(self, db_session, sample_parent, sample_class):
        student = models.Student(
            full_name="Иванов Петр",
            parent_id=sample_parent.parent_id,
            class_id=sample_class.class_id
        )
        db_session.add(student)
        db_session.commit()
        db_session.refresh(sample_parent)

        assert len(sample_parent.students) == 1
        assert sample_parent.students[0].full_name == "Иванов Петр"

@pytest.mark.unit
class TestTeacherModel:
    def test_create_teacher_with_valid_data(self, db_session):
        teacher = models.Teacher(
            full_name="Петрова Мария Сергеевна",
            contact_info="maria@school.com",
            position="Учитель математики"
        )
        db_session.add(teacher)
        db_session.commit()
        db_session.refresh(teacher)

        assert teacher.teacher_id is not None
        assert teacher.full_name == "Петрова Мария Сергеевна"
        assert teacher.contact_info == "maria@school.com"
        assert teacher.position == "Учитель математики"

    def test_teacher_full_name_required(self, db_session):
        teacher = models.Teacher(position="Учитель")
        db_session.add(teacher)

        with pytest.raises(Exception):
            db_session.commit()

    def test_teacher_subject_relationship(self, db_session, sample_teacher):
        subject = models.Subject(
            name="Физика",
            teacher_id=sample_teacher.teacher_id
        )
        db_session.add(subject)
        db_session.commit()
        db_session.refresh(sample_teacher)

        assert len(sample_teacher.subjects) >= 1
        assert any(s.name == "Физика" for s in sample_teacher.subjects)

    def test_teacher_class_relationship(self, db_session, sample_teacher):
        school_class = models.SchoolClass(
            number_letter="10Б",
            class_teacher_id=sample_teacher.teacher_id
        )
        db_session.add(school_class)
        db_session.commit()
        db_session.refresh(sample_teacher)

        assert len(sample_teacher.classes) >= 1
        assert any(c.number_letter == "10Б" for c in sample_teacher.classes)

@pytest.mark.unit
class TestSubjectModel:
    def test_create_subject_with_valid_data(self, db_session, sample_teacher):
        subject = models.Subject(
            name="История",
            description="История России",
            teacher_id=sample_teacher.teacher_id
        )
        db_session.add(subject)
        db_session.commit()
        db_session.refresh(subject)

        assert subject.subject_id is not None
        assert subject.name == "История"
        assert subject.description == "История России"
        assert subject.teacher_id == sample_teacher.teacher_id

    def test_subject_name_required(self, db_session):
        subject = models.Subject(description="Описание")
        db_session.add(subject)

        with pytest.raises(Exception):
            db_session.commit()

    def test_subject_teacher_relationship(self, db_session, sample_subject, sample_teacher):
        db_session.refresh(sample_subject)
        assert sample_subject.teacher.teacher_id == sample_teacher.teacher_id
        assert sample_subject.teacher.full_name == sample_teacher.full_name

    def test_subject_on_delete_set_null(self, db_session, sample_subject, sample_teacher):
        subject_id = sample_subject.subject_id
        db_session.delete(sample_teacher)
        db_session.commit()

        subject = db_session.query(models.Subject).filter_by(subject_id=subject_id).first()
        assert subject is not None
        assert subject.teacher_id is None

@pytest.mark.unit
class TestSchoolClassModel:
    def test_create_class_with_valid_data(self, db_session, sample_teacher):
        school_class = models.SchoolClass(
            number_letter="11А",
            class_teacher_id=sample_teacher.teacher_id
        )
        db_session.add(school_class)
        db_session.commit()
        db_session.refresh(school_class)

        assert school_class.class_id is not None
        assert school_class.number_letter == "11А"
        assert school_class.class_teacher_id == sample_teacher.teacher_id

    def test_class_number_letter_required(self, db_session):
        school_class = models.SchoolClass()
        db_session.add(school_class)

        with pytest.raises(Exception):
            db_session.commit()

    def test_class_teacher_relationship(self, db_session, sample_class, sample_teacher):
        db_session.refresh(sample_class)
        assert sample_class.class_teacher.teacher_id == sample_teacher.teacher_id

    def test_class_student_relationship(self, db_session, sample_class):
        student1 = models.Student(full_name="Студент 1", class_id=sample_class.class_id)
        student2 = models.Student(full_name="Студент 2", class_id=sample_class.class_id)
        db_session.add_all([student1, student2])
        db_session.commit()
        db_session.refresh(sample_class)

        assert len(sample_class.students) >= 2

    def test_class_on_delete_set_null(self, db_session, sample_class, sample_teacher):
        class_id = sample_class.class_id
        db_session.delete(sample_teacher)
        db_session.commit()

        school_class = db_session.query(models.SchoolClass).filter_by(class_id=class_id).first()
        assert school_class is not None
        assert school_class.class_teacher_id is None

@pytest.mark.unit
class TestStudentModel:
    def test_create_student_with_valid_data(self, db_session, sample_class, sample_parent):
        student = models.Student(
            full_name="Сидоров Петр Иванович",
            date_of_birth=date(2008, 5, 15),
            class_id=sample_class.class_id,
            contact_info="petr@example.com",
            additional_info="Отличник",
            parent_id=sample_parent.parent_id
        )
        db_session.add(student)
        db_session.commit()
        db_session.refresh(student)

        assert student.student_id is not None
        assert student.full_name == "Сидоров Петр Иванович"
        assert student.date_of_birth == date(2008, 5, 15)
        assert student.class_id == sample_class.class_id
        assert student.parent_id == sample_parent.parent_id

    def test_student_full_name_required(self, db_session):
        student = models.Student(contact_info="student@example.com")
        db_session.add(student)

        with pytest.raises(Exception):
            db_session.commit()

    def test_student_class_relationship(self, db_session, sample_student, sample_class):
        db_session.refresh(sample_student)
        assert sample_student.school_class.class_id == sample_class.class_id

    def test_student_parent_relationship(self, db_session, sample_student, sample_parent):
        db_session.refresh(sample_student)
        assert sample_student.parent.parent_id == sample_parent.parent_id

    def test_student_on_delete_set_null_class(self, db_session, sample_student, sample_class):
        student_id = sample_student.student_id
        db_session.delete(sample_class)
        db_session.commit()

        student = db_session.query(models.Student).filter_by(student_id=student_id).first()
        assert student is not None
        assert student.class_id is None

    def test_student_on_delete_set_null_parent(self, db_session, sample_student, sample_parent):
        student_id = sample_student.student_id
        db_session.delete(sample_parent)
        db_session.commit()

        student = db_session.query(models.Student).filter_by(student_id=student_id).first()
        assert student is not None
        assert student.parent_id is None

@pytest.mark.unit
class TestGradeModel:
    def test_create_grade_with_valid_data(self, db_session, sample_student, sample_subject, sample_teacher):
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

        assert grade.grade_id is not None
        assert grade.student_id == sample_student.student_id
        assert grade.subject_id == sample_subject.subject_id
        assert grade.teacher_id == sample_teacher.teacher_id
        assert grade.grade == "5"
        assert grade.comment == "Отлично"

    def test_create_grade_with_different_values(self, db_session, sample_student, sample_subject, sample_teacher):
        grades = ["5", "4", "3", "2", "1", "П", "Б"]

        for grade_value in grades:
            grade = models.Grade(
                student_id=sample_student.student_id,
                subject_id=sample_subject.subject_id,
                teacher_id=sample_teacher.teacher_id,
                grade=grade_value,
                date_issued=date.today()
            )
            db_session.add(grade)

        db_session.commit()
        all_grades = db_session.query(models.Grade).all()
        assert len(all_grades) == 7

    def test_grade_student_id_required(self, db_session, sample_subject, sample_teacher):
        grade = models.Grade(
            subject_id=sample_subject.subject_id,
            teacher_id=sample_teacher.teacher_id,
            grade="5"
        )
        db_session.add(grade)

        with pytest.raises(Exception):
            db_session.commit()

    def test_grade_subject_id_required(self, db_session, sample_student, sample_teacher):
        grade = models.Grade(
            student_id=sample_student.student_id,
            teacher_id=sample_teacher.teacher_id,
            grade="5"
        )
        db_session.add(grade)

        with pytest.raises(Exception):
            db_session.commit()

    def test_grade_student_relationship(self, db_session, sample_grade, sample_student):
        db_session.refresh(sample_grade)
        assert sample_grade.student.student_id == sample_student.student_id

    def test_grade_subject_relationship(self, db_session, sample_grade, sample_subject):
        db_session.refresh(sample_grade)
        assert sample_grade.subject.subject_id == sample_subject.subject_id

    def test_grade_delete_when_student_deleted(self, db_session, sample_student, sample_subject, sample_teacher):
        grade = models.Grade(
            student_id=sample_student.student_id,
            subject_id=sample_subject.subject_id,
            teacher_id=sample_teacher.teacher_id,
            grade="5",
            date_issued=date.today()
        )
        db_session.add(grade)
        db_session.commit()
        grade_id = grade.grade_id

        db_session.query(models.Grade).filter_by(grade_id=grade_id).delete()
        db_session.delete(sample_student)
        db_session.commit()

        student_check = db_session.query(models.Student).filter_by(student_id=sample_student.student_id).first()
        assert student_check is None

    def test_grade_delete_when_subject_deleted(self, db_session, sample_student, sample_subject, sample_teacher):
        grade = models.Grade(
            student_id=sample_student.student_id,
            subject_id=sample_subject.subject_id,
            teacher_id=sample_teacher.teacher_id,
            grade="4",
            date_issued=date.today()
        )
        db_session.add(grade)
        db_session.commit()
        grade_id = grade.grade_id

        db_session.query(models.Grade).filter_by(grade_id=grade_id).delete()
        db_session.delete(sample_subject)
        db_session.commit()

        subject_check = db_session.query(models.Subject).filter_by(subject_id=sample_subject.subject_id).first()
        assert subject_check is None
