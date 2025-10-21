import axios from 'axios';
import {
  Student,
  StudentCreate,
  Teacher,
  TeacherCreate,
  Subject,
  SubjectCreate,
  SchoolClass,
  SchoolClassCreate,
  Grade,
  GradeCreate,
  Parent,
  ParentCreate,
} from '@/types';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const studentsApi = {
  getAll: (skip = 0, limit = 100) =>
    api.get<Student[]>('/students/', { params: { skip, limit } }),
  create: (data: StudentCreate) => api.post<Student>('/students/', data),
  getById: (id: number) => api.get<Student>(`/students/${id}`),
  update: (id: number, data: Partial<StudentCreate>) =>
    api.put<Student>(`/students/${id}`, data),
  delete: (id: number) => api.delete(`/students/${id}`),
};

export const teachersApi = {
  getAll: (skip = 0, limit = 100) =>
    api.get<Teacher[]>('/teachers/', { params: { skip, limit } }),
  create: (data: TeacherCreate) => api.post<Teacher>('/teachers/', data),
  getById: (id: number) => api.get<Teacher>(`/teachers/${id}`),
  update: (id: number, data: Partial<TeacherCreate>) =>
    api.put<Teacher>(`/teachers/${id}`, data),
  delete: (id: number) => api.delete(`/teachers/${id}`),
};

export const subjectsApi = {
  getAll: (skip = 0, limit = 100) =>
    api.get<Subject[]>('/subjects/', { params: { skip, limit } }),
  create: (data: SubjectCreate) => api.post<Subject>('/subjects/', data),
  getById: (id: number) => api.get<Subject>(`/subjects/${id}`),
  update: (id: number, data: Partial<SubjectCreate>) =>
    api.put<Subject>(`/subjects/${id}`, data),
  delete: (id: number) => api.delete(`/subjects/${id}`),
};

export const classesApi = {
  getAll: (skip = 0, limit = 100) =>
    api.get<SchoolClass[]>('/classes/', { params: { skip, limit } }),
  create: (data: SchoolClassCreate) =>
    api.post<SchoolClass>('/classes/', data),
  getById: (id: number) => api.get<SchoolClass>(`/classes/${id}`),
  update: (id: number, data: Partial<SchoolClassCreate>) =>
    api.put<SchoolClass>(`/classes/${id}`, data),
  delete: (id: number) => api.delete(`/classes/${id}`),
};

export const gradesApi = {
  getAll: (skip = 0, limit = 100) =>
    api.get<Grade[]>('/grades/', { params: { skip, limit } }),
  create: (data: GradeCreate) => api.post<Grade>('/grades/', data),
  getById: (id: number) => api.get<Grade>(`/grades/${id}`),
  update: (id: number, data: Partial<GradeCreate>) =>
    api.put<Grade>(`/grades/${id}`, data),
  delete: (id: number) => api.delete(`/grades/${id}`),
  getByStudent: (studentId: number) =>
    api.get<Grade[]>(`/students/${studentId}/grades`),
};

export const parentsApi = {
  getAll: (skip = 0, limit = 100) =>
    api.get<Parent[]>('/parents/', { params: { skip, limit } }),
  create: (data: ParentCreate) => api.post<Parent>('/parents/', data),
  getById: (id: number) => api.get<Parent>(`/parents/${id}`),
  update: (id: number, data: Partial<ParentCreate>) =>
    api.put<Parent>(`/parents/${id}`, data),
  delete: (id: number) => api.delete(`/parents/${id}`),
};

export default api;
