CREATE TABLE Parent (
  parent_id SERIAL PRIMARY KEY,
  full_name TEXT,
  contact_info TEXT,
  student_relation TEXT
);

CREATE TABLE Teacher (
  teacher_id SERIAL PRIMARY KEY,
  full_name TEXT,
  subject_id INTEGER,
  contact_info TEXT,
  position TEXT
);

CREATE TABLE Classs (
  classs_id SERIAL PRIMARY KEY,
  number_letter TEXT,
  classs_teacher_id INTEGER,
  student_list TEXT,
  FOREIGN KEY (classs_teacher_id) REFERENCES Teacher (teacher_id)
);

CREATE TABLE Student (
  student_id SERIAL PRIMARY KEY,
  full_name TEXT,
  date_of_birth DATE,
  classs_id INTEGER,
  contact_info TEXT,
  additional_info TEXT,
  FOREIGN KEY (classs_id) REFERENCES Class (classs_id)
);



CREATE TABLE Subject (
  subject_id SERIAL PRIMARY KEY,
  name TEXT,
  description TEXT,
  teacher_id INTEGER,
  FOREIGN KEY (teacher_id) REFERENCES Teacher (teacher_id)
);

ALTER TABLE Teacher
ADD CONSTRAINT fk_subject_id
FOREIGN KEY (subject_id) REFERENCES Subject (subject_id);


CREATE TABLE Grade (
  grade_id SERIAL PRIMARY KEY,
  student_id INTEGER,
  subject_id INTEGER,
  teacher_id INTEGER,
  date_issued DATE,
  grade REAL,
  comment TEXT,
  FOREIGN KEY (student_id) REFERENCES Student (student_id),
  FOREIGN KEY (subject_id) REFERENCES Subject (subject_id),
  FOREIGN KEY (teacher_id) REFERENCES Teacher (teacher_id)
);

CREATE TABLE Journal (
  journal_id SERIAL PRIMARY KEY,
  classs_id INTEGER,
  subject_id INTEGER,
  grade_list TEXT,
  FOREIGN KEY (classs_id) REFERENCES Classs (classs_id),
  FOREIGN KEY (subject_id) REFERENCES Subject (subject_id)
);