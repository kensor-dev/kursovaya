from pydantic import BaseModel
from typing import Optional
from datetime import date

class StudentBase(BaseModel):
    full_name: str
    date_of_birth: Optional[date] = None
    class_id: Optional[int] = None
    contact_info: Optional[str] = None
    additional_info: Optional[str] = None
    parent_id: Optional[int] = None

class StudentCreate(StudentBase):
    pass

class StudentOut(StudentBase):
    student_id: int
    class Config:
        from_attributes = True

class TeacherBase(BaseModel):
    full_name: str
    contact_info: Optional[str] = None
    position: Optional[str] = None

class TeacherCreate(TeacherBase):
    pass

class TeacherOut(TeacherBase):
    teacher_id: int
    class Config:
        from_attributes = True

class SubjectBase(BaseModel):
    name: str
    description: Optional[str] = None
    teacher_id: Optional[int] = None

class SubjectCreate(SubjectBase):
    pass

class SubjectOut(SubjectBase):
    subject_id: int
    class Config:
        from_attributes = True

class SchoolClassBase(BaseModel):
    number_letter: str
    class_teacher_id: Optional[int] = None

class SchoolClassCreate(SchoolClassBase):
    pass

class SchoolClassOut(SchoolClassBase):
    class_id: int
    class Config:
        from_attributes = True

class ParentBase(BaseModel):
    full_name: str
    contact_info: Optional[str] = None
    student_relation: Optional[str] = None

class ParentCreate(ParentBase):
    pass

class ParentOut(ParentBase):
    parent_id: int
    class Config:
        from_attributes = True

class GradeBase(BaseModel):
    student_id: int
    subject_id: int
    teacher_id: Optional[int] = None
    date_issued: Optional[date] = None
    grade: Optional[float] = None
    comment: Optional[str] = None

class GradeCreate(GradeBase):
    pass

class GradeOut(GradeBase):
    grade_id: int
    class Config:
        from_attributes = True
