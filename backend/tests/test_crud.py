import pytest
from datetime import date
from app import crud, schemas

@pytest.mark.unit
class TestStudentCRUD:
    def test_create_student_with_valid_data(self, db_session, sample_class, sample_parent):
        student_data = schemas.StudentCreate(
            full_name="Тестовый Студент",
            date_of_birth=date(2008, 3, 20),
            class_id=sample_class.class_id,
            contact_info="test@student.com",
            additional_info="Тестовая информация",
            parent_id=sample_parent.parent_id
        )
        student = crud.create_student(db_session, student_data)

        assert student.student_id is not None
        assert student.full_name == "Тестовый Студент"
        assert student.class_id == sample_class.class_id
        assert student.parent_id == sample_parent.parent_id

    def test_get_students_with_pagination(self, db_session, sample_class):
        for i in range(15):
            student_data = schemas.StudentCreate(
                full_name=f"Студент {i}",
                class_id=sample_class.class_id
            )
            crud.create_student(db_session, student_data)

        students_page1 = crud.get_students(db_session, skip=0, limit=10)
        students_page2 = crud.get_students(db_session, skip=10, limit=10)

        assert len(students_page1) == 10
        assert len(students_page2) == 5

    def test_get_students_empty_list(self, db_session):
        students = crud.get_students(db_session)
        assert students == []

    def test_get_student_by_id(self, db_session, sample_student):
        student = crud.get_student(db_session, sample_student.student_id)
        assert student is not None
        assert student.student_id == sample_student.student_id
        assert student.full_name == sample_student.full_name

    def test_get_student_nonexistent_id(self, db_session):
        student = crud.get_student(db_session, 99999)
        assert student is None

    def test_update_student(self, db_session, sample_student):
        update_data = schemas.StudentCreate(
            full_name="Обновленное Имя",
            date_of_birth=sample_student.date_of_birth,
            class_id=sample_student.class_id,
            contact_info="new@email.com",
            parent_id=sample_student.parent_id
        )
        updated_student = crud.update_student(db_session, sample_student.student_id, update_data)

        assert updated_student is not None
        assert updated_student.full_name == "Обновленное Имя"
        assert updated_student.contact_info == "new@email.com"

    def test_update_student_nonexistent_id(self, db_session, sample_class):
        update_data = schemas.StudentCreate(
            full_name="Тест",
            class_id=sample_class.class_id
        )
        result = crud.update_student(db_session, 99999, update_data)
        assert result is None

    def test_delete_student(self, db_session, sample_student):
        student_id = sample_student.student_id
        deleted = crud.delete_student(db_session, student_id)

        assert deleted is not None
        assert deleted.student_id == student_id
        assert crud.get_student(db_session, student_id) is None

    def test_delete_student_nonexistent_id(self, db_session):
        result = crud.delete_student(db_session, 99999)
        assert result is None

@pytest.mark.unit
class TestGradeCRUD:
    def test_create_grade_with_valid_data(self, db_session, sample_student, sample_subject, sample_teacher):
        grade_data = schemas.GradeCreate(
            student_id=sample_student.student_id,
            subject_id=sample_subject.subject_id,
            teacher_id=sample_teacher.teacher_id,
            grade="5",
            date_issued=date.today(),
            comment="Отлично выполнено"
        )
        grade = crud.create_grade(db_session, grade_data)

        assert grade.grade_id is not None
        assert grade.grade == "5"
        assert grade.comment == "Отлично выполнено"

    def test_create_grade_with_different_values(self, db_session, sample_student, sample_subject, sample_teacher):
        grade_values = ["5", "4", "3", "2", "1", "П", "Б"]

        for grade_value in grade_values:
            grade_data = schemas.GradeCreate(
                student_id=sample_student.student_id,
                subject_id=sample_subject.subject_id,
                teacher_id=sample_teacher.teacher_id,
                grade=grade_value,
                date_issued=date.today()
            )
            grade = crud.create_grade(db_session, grade_data)
            assert grade.grade == grade_value

    def test_get_grades_filtered_by_subject(self, db_session, sample_student, sample_subject, sample_teacher):
        for i in range(3):
            grade_data = schemas.GradeCreate(
                student_id=sample_student.student_id,
                subject_id=sample_subject.subject_id,
                teacher_id=sample_teacher.teacher_id,
                grade="5"
            )
            crud.create_grade(db_session, grade_data)

        grades = crud.get_grades_filtered(db_session, subject_id=sample_subject.subject_id)
        assert len(grades) == 3

    def test_get_grades_filtered_by_class(self, db_session, sample_student, sample_subject, sample_teacher, sample_class):
        for i in range(2):
            grade_data = schemas.GradeCreate(
                student_id=sample_student.student_id,
                subject_id=sample_subject.subject_id,
                teacher_id=sample_teacher.teacher_id,
                grade="5"
            )
            crud.create_grade(db_session, grade_data)

        grades = crud.get_grades_filtered(db_session, class_id=sample_class.class_id)
        assert len(grades) == 2

    def test_get_grades_filtered_by_subject_and_class(self, db_session, sample_student, sample_subject, sample_teacher, sample_class):
        for i in range(2):
            grade_data = schemas.GradeCreate(
                student_id=sample_student.student_id,
                subject_id=sample_subject.subject_id,
                teacher_id=sample_teacher.teacher_id,
                grade="5"
            )
            crud.create_grade(db_session, grade_data)

        grades = crud.get_grades_filtered(
            db_session,
            subject_id=sample_subject.subject_id,
            class_id=sample_class.class_id
        )
        assert len(grades) == 2
