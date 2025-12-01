import pytest
from datetime import date

@pytest.mark.api
class TestHealthCheck:
    def test_root_endpoint(self, client):
        response = client.get("/")
        assert response.status_code == 200
        assert response.json() == {"msg": "Kursovaya API alive"}

@pytest.mark.api
class TestStudentsAPI:
    def test_create_student_success(self, client, sample_class, sample_parent):
        student_data = {
            "full_name": "Новый Студент",
            "date_of_birth": "2008-05-15",
            "class_id": sample_class.class_id,
            "contact_info": "student@test.com",
            "additional_info": "Тестовый студент",
            "parent_id": sample_parent.parent_id
        }
        response = client.post("/students/", json=student_data)

        assert response.status_code == 200
        data = response.json()
        assert data["full_name"] == "Новый Студент"
        assert data["student_id"] is not None
        assert data["class_id"] == sample_class.class_id

    def test_create_student_validation_error(self, client):
        student_data = {
            "contact_info": "test@test.com"
        }
        response = client.post("/students/", json=student_data)
        assert response.status_code == 422

    def test_list_students(self, client, sample_student):
        response = client.get("/students/")

        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) >= 1

    def test_list_students_with_pagination(self, client, sample_class):
        for i in range(15):
            client.post("/students/", json={
                "full_name": f"Студент {i}",
                "class_id": sample_class.class_id
            })

        response = client.get("/students/?skip=0&limit=10")
        assert response.status_code == 200
        assert len(response.json()) == 10

        response = client.get("/students/?skip=10&limit=10")
        assert response.status_code == 200
        assert len(response.json()) >= 5

    def test_get_student_by_id(self, client, sample_student):
        response = client.get(f"/students/{sample_student.student_id}")

        assert response.status_code == 200
        data = response.json()
        assert data["student_id"] == sample_student.student_id
        assert data["full_name"] == sample_student.full_name

    def test_get_student_not_found(self, client):
        response = client.get("/students/99999")
        assert response.status_code == 404
        assert "not found" in response.json()["detail"].lower()

    def test_update_student(self, client, sample_student):
        update_data = {
            "full_name": "Обновленное Имя",
            "class_id": sample_student.class_id,
            "parent_id": sample_student.parent_id
        }
        response = client.put(f"/students/{sample_student.student_id}", json=update_data)

        assert response.status_code == 200
        data = response.json()
        assert data["full_name"] == "Обновленное Имя"

    def test_update_student_not_found(self, client, sample_class):
        update_data = {
            "full_name": "Тест",
            "class_id": sample_class.class_id
        }
        response = client.put("/students/99999", json=update_data)
        assert response.status_code == 404

    def test_delete_student(self, client, sample_student):
        student_id = sample_student.student_id
        response = client.delete(f"/students/{student_id}")

        assert response.status_code == 200
        assert "deleted" in response.json()["msg"].lower()

        response = client.get(f"/students/{student_id}")
        assert response.status_code == 404

    def test_delete_student_not_found(self, client):
        response = client.delete("/students/99999")
        assert response.status_code == 404

@pytest.mark.api
class TestTeachersAPI:
    def test_create_teacher(self, client):
        teacher_data = {
            "full_name": "Учитель Тестовый",
            "contact_info": "teacher@test.com",
            "position": "Учитель математики"
        }
        response = client.post("/teachers/", json=teacher_data)

        assert response.status_code == 200
        data = response.json()
        assert data["full_name"] == "Учитель Тестовый"
        assert data["teacher_id"] is not None

    def test_list_teachers(self, client, sample_teacher):
        response = client.get("/teachers/")

        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) >= 1

    def test_get_teacher_by_id(self, client, sample_teacher):
        response = client.get(f"/teachers/{sample_teacher.teacher_id}")

        assert response.status_code == 200
        data = response.json()
        assert data["teacher_id"] == sample_teacher.teacher_id

    def test_update_teacher(self, client, sample_teacher):
        update_data = {
            "full_name": "Обновленное Имя",
            "position": "Директор"
        }
        response = client.put(f"/teachers/{sample_teacher.teacher_id}", json=update_data)

        assert response.status_code == 200
        assert response.json()["full_name"] == "Обновленное Имя"

    def test_delete_teacher(self, client, sample_teacher):
        teacher_id = sample_teacher.teacher_id
        response = client.delete(f"/teachers/{teacher_id}")

        assert response.status_code == 200
        assert "deleted" in response.json()["msg"].lower()

@pytest.mark.api
class TestSubjectsAPI:
    def test_create_subject(self, client, sample_teacher):
        subject_data = {
            "name": "Физика",
            "description": "Молекулярная физика",
            "teacher_id": sample_teacher.teacher_id
        }
        response = client.post("/subjects/", json=subject_data)

        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Физика"
        assert data["subject_id"] is not None

    def test_list_subjects(self, client, sample_subject):
        response = client.get("/subjects/")

        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) >= 1

    def test_get_subject_by_id(self, client, sample_subject):
        response = client.get(f"/subjects/{sample_subject.subject_id}")

        assert response.status_code == 200
        data = response.json()
        assert data["subject_id"] == sample_subject.subject_id

    def test_update_subject(self, client, sample_subject):
        update_data = {
            "name": "Обновленное название",
            "description": "Новое описание"
        }
        response = client.put(f"/subjects/{sample_subject.subject_id}", json=update_data)

        assert response.status_code == 200
        assert response.json()["name"] == "Обновленное название"

    def test_delete_subject(self, client, sample_subject):
        subject_id = sample_subject.subject_id
        response = client.delete(f"/subjects/{subject_id}")

        assert response.status_code == 200

@pytest.mark.api
class TestClassesAPI:
    def test_create_class(self, client, sample_teacher):
        class_data = {
            "number_letter": "10В",
            "class_teacher_id": sample_teacher.teacher_id
        }
        response = client.post("/classes/", json=class_data)

        assert response.status_code == 200
        data = response.json()
        assert data["number_letter"] == "10В"
        assert data["class_id"] is not None

    def test_list_classes(self, client, sample_class):
        response = client.get("/classes/")

        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) >= 1

    def test_get_class_by_id(self, client, sample_class):
        response = client.get(f"/classes/{sample_class.class_id}")

        assert response.status_code == 200
        data = response.json()
        assert data["class_id"] == sample_class.class_id

    def test_update_class(self, client, sample_class):
        update_data = {
            "number_letter": "10А-updated",
            "class_teacher_id": sample_class.class_teacher_id
        }
        response = client.put(f"/classes/{sample_class.class_id}", json=update_data)

        assert response.status_code == 200
        assert response.json()["number_letter"] == "10А-updated"

    def test_delete_class(self, client, sample_class):
        class_id = sample_class.class_id
        response = client.delete(f"/classes/{class_id}")

        assert response.status_code == 200

@pytest.mark.api
class TestParentsAPI:
    def test_create_parent(self, client):
        parent_data = {
            "full_name": "Родитель Тестовый",
            "contact_info": "parent@test.com",
            "student_relation": "Отец"
        }
        response = client.post("/parents/", json=parent_data)

        assert response.status_code == 200
        data = response.json()
        assert data["full_name"] == "Родитель Тестовый"
        assert data["parent_id"] is not None

    def test_list_parents(self, client, sample_parent):
        response = client.get("/parents/")

        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) >= 1

    def test_get_parent_by_id(self, client, sample_parent):
        response = client.get(f"/parents/{sample_parent.parent_id}")

        assert response.status_code == 200
        data = response.json()
        assert data["parent_id"] == sample_parent.parent_id

    def test_update_parent(self, client, sample_parent):
        update_data = {
            "full_name": "Обновленное Имя",
            "contact_info": "new@parent.com"
        }
        response = client.put(f"/parents/{sample_parent.parent_id}", json=update_data)

        assert response.status_code == 200
        assert response.json()["full_name"] == "Обновленное Имя"

    def test_delete_parent(self, client, sample_parent):
        parent_id = sample_parent.parent_id
        response = client.delete(f"/parents/{parent_id}")

        assert response.status_code == 200

@pytest.mark.api
class TestGradesAPI:
    def test_create_grade(self, client, sample_student, sample_subject, sample_teacher):
        grade_data = {
            "student_id": sample_student.student_id,
            "subject_id": sample_subject.subject_id,
            "teacher_id": sample_teacher.teacher_id,
            "grade": "5",
            "date_issued": str(date.today()),
            "comment": "Отлично"
        }
        response = client.post("/grades/", json=grade_data)

        assert response.status_code == 200
        data = response.json()
        assert data["grade"] == "5"
        assert data["grade_id"] is not None

    def test_create_grade_with_different_values(self, client, sample_student, sample_subject, sample_teacher):
        grade_values = ["5", "4", "3", "2", "1", "П", "Б"]

        for grade_value in grade_values:
            grade_data = {
                "student_id": sample_student.student_id,
                "subject_id": sample_subject.subject_id,
                "teacher_id": sample_teacher.teacher_id,
                "grade": grade_value,
                "date_issued": str(date.today())
            }
            response = client.post("/grades/", json=grade_data)
            assert response.status_code == 200
            assert response.json()["grade"] == grade_value

    def test_list_grades(self, client, sample_grade):
        response = client.get("/grades/")

        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) >= 1

    def test_list_grades_filtered_by_subject(self, client, sample_student, sample_subject, sample_teacher):
        for i in range(3):
            client.post("/grades/", json={
                "student_id": sample_student.student_id,
                "subject_id": sample_subject.subject_id,
                "teacher_id": sample_teacher.teacher_id,
                "grade": "5"
            })

        response = client.get(f"/grades/?subject_id={sample_subject.subject_id}")
        assert response.status_code == 200
        data = response.json()
        assert len(data) >= 3

    def test_list_grades_filtered_by_class(self, client, sample_student, sample_subject, sample_teacher, sample_class):
        for i in range(2):
            client.post("/grades/", json={
                "student_id": sample_student.student_id,
                "subject_id": sample_subject.subject_id,
                "teacher_id": sample_teacher.teacher_id,
                "grade": "5"
            })

        response = client.get(f"/grades/?class_id={sample_class.class_id}")
        assert response.status_code == 200
        data = response.json()
        assert len(data) >= 2

    def test_list_grades_filtered_by_subject_and_class(self, client, sample_student, sample_subject, sample_teacher, sample_class):
        response = client.get(f"/grades/?subject_id={sample_subject.subject_id}&class_id={sample_class.class_id}")
        assert response.status_code == 200

    def test_get_grade_by_id(self, client, sample_grade):
        response = client.get(f"/grades/{sample_grade.grade_id}")

        assert response.status_code == 200
        data = response.json()
        assert data["grade_id"] == sample_grade.grade_id

    def test_update_grade(self, client, sample_grade):
        update_data = {
            "student_id": sample_grade.student_id,
            "subject_id": sample_grade.subject_id,
            "teacher_id": sample_grade.teacher_id,
            "grade": "4",
            "comment": "Хорошо"
        }
        response = client.put(f"/grades/{sample_grade.grade_id}", json=update_data)

        assert response.status_code == 200
        assert response.json()["grade"] == "4"

    def test_delete_grade(self, client, sample_grade):
        grade_id = sample_grade.grade_id
        response = client.delete(f"/grades/{grade_id}")

        assert response.status_code == 200
