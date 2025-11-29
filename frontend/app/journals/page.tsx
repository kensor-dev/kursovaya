'use client';

import { useState, useEffect } from 'react';
import {
  Box,
  Typography,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  Paper,
} from '@mui/material';
import { Subject, SchoolClass, Student, Grade } from '@/types';
import { subjectsApi, classesApi, studentsApi, gradesApi } from '@/lib/api';
import JournalTable from '@/components/Journal/JournalTable';

export default function JournalsPage() {
  const [subjects, setSubjects] = useState<Subject[]>([]);
  const [classes, setClasses] = useState<SchoolClass[]>([]);
  const [students, setStudents] = useState<Student[]>([]);
  const [grades, setGrades] = useState<Grade[]>([]);
  
  const [selectedSubjectId, setSelectedSubjectId] = useState<number | null>(null);
  const [selectedClassId, setSelectedClassId] = useState<number | null>(null);

  useEffect(() => {
    fetchSubjects();
    fetchClasses();
  }, []);

  useEffect(() => {
    if (selectedClassId) {
      fetchStudents();
    }
  }, [selectedClassId]);

  useEffect(() => {
    if (selectedSubjectId && selectedClassId) {
      fetchGrades();
    }
  }, [selectedSubjectId, selectedClassId]);

  const fetchSubjects = async () => {
    try {
      const response = await subjectsApi.getAll();
      setSubjects(response.data);
    } catch (error) {
      console.error('Ошибка при загрузке предметов:', error);
    }
  };

  const fetchClasses = async () => {
    try {
      const response = await classesApi.getAll();
      setClasses(response.data);
    } catch (error) {
      console.error('Ошибка при загрузке классов:', error);
    }
  };

  const fetchStudents = async () => {
    try {
      const response = await studentsApi.getAll(0, 1000);
      const filteredStudents = response.data.filter(
        (s) => s.class_id === selectedClassId
      );
      setStudents(filteredStudents);
    } catch (error) {
      console.error('Ошибка при загрузке учеников:', error);
    }
  };

  const fetchGrades = async () => {
    try {
      if (selectedSubjectId && selectedClassId) {
        const response = await gradesApi.getFiltered(
          selectedSubjectId,
          selectedClassId,
          0,
          1000
        );
        setGrades(response.data);
      }
    } catch (error) {
      console.error('Ошибка при загрузке оценок:', error);
    }
  };

  const selectedSubject = subjects.find((s) => s.subject_id === selectedSubjectId);
  const selectedClass = classes.find((c) => c.class_id === selectedClassId);

  return (
    <Box>
      <Typography variant="h4" component="h1" sx={{ mb: 3 }}>
        Журналы успеваемости
      </Typography>

      <Paper sx={{ p: 3, mb: 3 }}>
        <Box sx={{ display: 'flex', gap: 2, mb: 3 }}>
          <FormControl sx={{ minWidth: 200 }}>
            <InputLabel>Предмет</InputLabel>
            <Select
              value={selectedSubjectId || ''}
              label="Предмет"
              onChange={(e) => setSelectedSubjectId(Number(e.target.value))}
            >
              {subjects.map((subject) => (
                <MenuItem key={subject.subject_id} value={subject.subject_id}>
                  {subject.name}
                </MenuItem>
              ))}
            </Select>
          </FormControl>

          <FormControl sx={{ minWidth: 200 }}>
            <InputLabel>Класс</InputLabel>
            <Select
              value={selectedClassId || ''}
              label="Класс"
              onChange={(e) => setSelectedClassId(Number(e.target.value))}
            >
              {classes.map((cls) => (
                <MenuItem key={cls.class_id} value={cls.class_id}>
                  {cls.number_letter}
                </MenuItem>
              ))}
            </Select>
          </FormControl>
        </Box>

        {selectedSubject && selectedClass && (
          <Box sx={{ mb: 2 }}>
            <Typography variant="h6">
              {selectedSubject.name}
            </Typography>
            <Typography variant="body2" color="text.secondary">
              Класс: {selectedClass.number_letter}
              {selectedClass.class_teacher && ` • Классный руководитель: ${selectedClass.class_teacher.full_name}`}
            </Typography>
            {selectedSubject.teacher && (
              <Typography variant="body2" color="text.secondary">
                Преподаватель: {selectedSubject.teacher.full_name}
              </Typography>
            )}
          </Box>
        )}
      </Paper>

      {selectedSubjectId && selectedClassId && students.length > 0 && (
        <JournalTable
          students={students}
          grades={grades}
          subjectId={selectedSubjectId}
          classId={selectedClassId}
          teacherId={selectedSubject?.teacher_id}
          onGradesChange={fetchGrades}
        />
      )}

      {selectedSubjectId && selectedClassId && students.length === 0 && (
        <Paper sx={{ p: 3 }}>
          <Typography color="text.secondary">
            В выбранном классе нет учеников
          </Typography>
        </Paper>
      )}
    </Box>
  );
}
