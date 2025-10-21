export interface Parent {
  parent_id: number;
  full_name: string;
  contact_info?: string;
  student_relation?: string;
}

export interface Teacher {
  teacher_id: number;
  full_name: string;
  contact_info?: string;
  position?: string;
}

export interface Subject {
  subject_id: number;
  name: string;
  description?: string;
  teacher_id?: number;
  teacher?: Teacher;
}

export interface SchoolClass {
  class_id: number;
  number_letter: string;
  class_teacher_id?: number;
  class_teacher?: Teacher;
}

export interface Student {
  student_id: number;
  full_name: string;
  date_of_birth?: string;
  class_id?: number;
  contact_info?: string;
  additional_info?: string;
  parent_id?: number;
  school_class?: SchoolClass;
  parent?: Parent;
}

export interface Grade {
  grade_id: number;
  student_id: number;
  subject_id: number;
  teacher_id?: number;
  date_issued?: string;
  grade?: number;
  comment?: string;
  student?: Student;
  subject?: Subject;
}

export interface StudentCreate {
  full_name: string;
  date_of_birth?: string | null;
  class_id?: number | null;
  contact_info?: string | null;
  additional_info?: string | null;
  parent_id?: number | null;
}

export interface TeacherCreate {
  full_name: string;
  contact_info?: string | null;
  position?: string | null;
}

export interface SubjectCreate {
  name: string;
  description?: string | null;
  teacher_id?: number | null;
}

export interface SchoolClassCreate {
  number_letter: string;
  class_teacher_id?: number | null;
}

export interface GradeCreate {
  student_id: number;
  subject_id: number;
  teacher_id?: number | null;
  date_issued?: string | null;
  grade?: number | null;
  comment?: string | null;
}

export interface ParentCreate {
  full_name: string;
  contact_info?: string | null;
  student_relation?: string | null;
}
