CREATE TABLE parent (
  parent_id SERIAL PRIMARY KEY,
  full_name TEXT NOT NULL,
  contact_info TEXT,
  student_relation TEXT
);

CREATE TABLE teacher (
  teacher_id SERIAL PRIMARY KEY,
  full_name TEXT NOT NULL,
  contact_info TEXT,
  position TEXT
);

CREATE TABLE subject (
  subject_id SERIAL PRIMARY KEY,
  name TEXT NOT NULL,
  description TEXT,
  teacher_id INTEGER,
  FOREIGN KEY (teacher_id) REFERENCES teacher (teacher_id) ON DELETE SET NULL
);

CREATE TABLE school_class (
  class_id SERIAL PRIMARY KEY,
  number_letter TEXT NOT NULL,
  class_teacher_id INTEGER,
  FOREIGN KEY (class_teacher_id) REFERENCES teacher (teacher_id) ON DELETE SET NULL
);

CREATE TABLE student (
  student_id SERIAL PRIMARY KEY,
  full_name TEXT NOT NULL,
  date_of_birth DATE,
  class_id INTEGER,
  contact_info TEXT,
  additional_info TEXT,
  parent_id INTEGER,
  FOREIGN KEY (class_id) REFERENCES school_class (class_id) ON DELETE SET NULL,
  FOREIGN KEY (parent_id) REFERENCES parent (parent_id) ON DELETE SET NULL
);

CREATE TABLE grade (
  grade_id SERIAL PRIMARY KEY,
  student_id INTEGER NOT NULL,
  subject_id INTEGER NOT NULL,
  teacher_id INTEGER,
  date_issued DATE,
  grade REAL,
  comment TEXT,
  FOREIGN KEY (student_id) REFERENCES student (student_id) ON DELETE CASCADE,
  FOREIGN KEY (subject_id) REFERENCES subject (subject_id) ON DELETE CASCADE,
  FOREIGN KEY (teacher_id) REFERENCES teacher (teacher_id) ON DELETE SET NULL
);

CREATE TABLE journal (
  journal_id SERIAL PRIMARY KEY,
  class_id INTEGER,
  subject_id INTEGER,
  grade_list TEXT,
  FOREIGN KEY (class_id) REFERENCES school_class (class_id),
  FOREIGN KEY (subject_id) REFERENCES subject (subject_id)
);
