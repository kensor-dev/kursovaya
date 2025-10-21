# backend/app/models.py
from sqlalchemy import Column, Integer, Text, Date, Float, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base

class Parent(Base):
    __tablename__ = "parent"
    parent_id = Column(Integer, primary_key=True, index=True)
    full_name = Column(Text, nullable=False)
    contact_info = Column(Text)
    student_relation = Column(Text)

    students = relationship("Student", back_populates="parent")

class Teacher(Base):
    __tablename__ = "teacher"
    teacher_id = Column(Integer, primary_key=True, index=True)
    full_name = Column(Text, nullable=False)
    contact_info = Column(Text)
    position = Column(Text)
    subjects = relationship("Subject", back_populates="teacher")
    classes = relationship("SchoolClass", back_populates="class_teacher")

class Subject(Base):
    __tablename__ = "subject"
    subject_id = Column(Integer, primary_key=True, index=True)
    name = Column(Text, nullable=False)
    description = Column(Text)
    teacher_id = Column(Integer, ForeignKey("teacher.teacher_id", ondelete="SET NULL"))
    teacher = relationship("Teacher", back_populates="subjects")
    grades = relationship("Grade", back_populates="subject")
    journals = relationship("Journal", back_populates="subject")

class SchoolClass(Base):
    __tablename__ = "school_class"
    class_id = Column(Integer, primary_key=True, index=True)
    number_letter = Column(Text, nullable=False)
    class_teacher_id = Column(Integer, ForeignKey("teacher.teacher_id", ondelete="SET NULL"))

    class_teacher = relationship("Teacher", back_populates="classes")
    students = relationship("Student", back_populates="school_class")
    journals = relationship("Journal", back_populates="school_class")

class Student(Base):
    __tablename__ = "student"
    student_id = Column(Integer, primary_key=True, index=True)
    full_name = Column(Text, nullable=False)
    date_of_birth = Column(Date)
    class_id = Column(Integer, ForeignKey("school_class.class_id", ondelete="SET NULL"))
    contact_info = Column(Text)
    additional_info = Column(Text)
    parent_id = Column(Integer, ForeignKey("parent.parent_id", ondelete="SET NULL"))

    school_class = relationship("SchoolClass", back_populates="students")
    parent = relationship("Parent", back_populates="students")
    grades = relationship("Grade", back_populates="student")

class Grade(Base):
    __tablename__ = "grade"
    grade_id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("student.student_id", ondelete="CASCADE"), nullable=False)
    subject_id = Column(Integer, ForeignKey("subject.subject_id", ondelete="CASCADE"), nullable=False)
    teacher_id = Column(Integer, ForeignKey("teacher.teacher_id", ondelete="SET NULL"))
    date_issued = Column(Date)
    grade = Column(Float)
    comment = Column(Text)

    student = relationship("Student", back_populates="grades")
    subject = relationship("Subject", back_populates="grades")

class Journal(Base):
    __tablename__ = "journal"
    journal_id = Column(Integer, primary_key=True, index=True)
    class_id = Column(Integer, ForeignKey("school_class.class_id"))
    subject_id = Column(Integer, ForeignKey("subject.subject_id"))
    grade_list = Column(Text)

    school_class = relationship("SchoolClass", back_populates="journals")
    subject = relationship("Subject", back_populates="journals")
