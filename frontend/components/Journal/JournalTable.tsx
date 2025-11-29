'use client';

import { useState } from 'react';
import {
  Box,
  Button,
  Paper,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Typography,
  IconButton,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  TextField,
} from '@mui/material';
import AddIcon from '@mui/icons-material/Add';
import DeleteIcon from '@mui/icons-material/Delete';
import EditIcon from '@mui/icons-material/Edit';
import { Student, Grade, GradeCreate } from '@/types';
import GradeCell from './GradeCell';
import GradeModal from './GradeModal';
import { gradesApi } from '@/lib/api';

interface JournalTableProps {
  students: Student[];
  grades: Grade[];
  subjectId: number;
  classId: number;
  teacherId?: number;
  onGradesChange: () => void;
}

export default function JournalTable({
  students,
  grades,
  subjectId,
  classId,
  teacherId,
  onGradesChange,
}: JournalTableProps) {
  const [dates, setDates] = useState<string[]>([]);
  const [selectedGrade, setSelectedGrade] = useState<Grade | null>(null);
  const [selectedCell, setSelectedCell] = useState<{ studentId: number; date: string } | null>(null);
  const [modalOpen, setModalOpen] = useState(false);
  const [dateDialogOpen, setDateDialogOpen] = useState(false);
  const [newDate, setNewDate] = useState('');
  const [editingDateIndex, setEditingDateIndex] = useState<number | null>(null);

  const uniqueDates = Array.from(new Set(grades.map(g => g.date_issued).filter(Boolean))).sort() as string[];

  useState(() => {
    setDates(uniqueDates.length > 0 ? uniqueDates : []);
  });

  const getGradeForCell = (studentId: number, date: string) => {
    return grades.find(
      (g) => g.student_id === studentId && g.date_issued === date
    );
  };

  const handleCellClick = (studentId: number, date: string) => {
    const grade = getGradeForCell(studentId, date);
    if (grade) {
      setSelectedGrade(grade);
    } else {
      setSelectedCell({ studentId, date });
    }
    setModalOpen(true);
  };

  const handleSaveGrade = async (data: GradeCreate) => {
    try {
      if (selectedGrade) {
        await gradesApi.update(selectedGrade.grade_id, data);
      } else {
        await gradesApi.create(data);
      }
      onGradesChange();
      setSelectedGrade(null);
      setSelectedCell(null);
    } catch (error) {
      console.error('Ошибка при сохранении оценки:', error);
    }
  };

  const handleDeleteGrade = async (gradeId: number) => {
    try {
      await gradesApi.delete(gradeId);
      onGradesChange();
      setSelectedGrade(null);
    } catch (error) {
      console.error('Ошибка при удалении оценки:', error);
    }
  };

  const handleAddDate = () => {
    setNewDate(new Date().toISOString().split('T')[0]);
    setEditingDateIndex(null);
    setDateDialogOpen(true);
  };

  const handleEditDate = (index: number) => {
    setNewDate(dates[index]);
    setEditingDateIndex(index);
    setDateDialogOpen(true);
  };

  const handleSaveDate = () => {
    if (editingDateIndex !== null) {
      const oldDate = dates[editingDateIndex];
      const newDates = [...dates];
      newDates[editingDateIndex] = newDate;
      setDates(newDates.sort());
      
      grades.forEach(async (grade) => {
        if (grade.date_issued === oldDate) {
          await gradesApi.update(grade.grade_id, { ...grade, date_issued: newDate });
        }
      });
    } else {
      if (!dates.includes(newDate)) {
        setDates([...dates, newDate].sort());
      }
    }
    setDateDialogOpen(false);
    onGradesChange();
  };

  const handleDeleteDate = async (date: string) => {
    if (confirm(`Удалить колонку с датой ${date}? Все оценки за эту дату будут удалены.`)) {
      const gradesToDelete = grades.filter((g) => g.date_issued === date);
      for (const grade of gradesToDelete) {
        await gradesApi.delete(grade.grade_id);
      }
      setDates(dates.filter((d) => d !== date));
      onGradesChange();
    }
  };

  const formatDate = (dateStr: string) => {
    const date = new Date(dateStr);
    return date.toLocaleDateString('ru-RU', { day: '2-digit', month: '2-digit', year: '2-digit' });
  };

  return (
    <Box>
      <Box sx={{ display: 'flex', gap: 2, mb: 2 }}>
        <Button
          variant="contained"
          startIcon={<AddIcon />}
          onClick={handleAddDate}
        >
          Добавить дату
        </Button>
      </Box>

      <TableContainer component={Paper}>
        <Table sx={{ minWidth: 650 }} size="small">
          <TableHead>
            <TableRow>
              <TableCell sx={{ fontWeight: 'bold', minWidth: 200 }}>
                Ученик
              </TableCell>
              {dates.map((date, index) => (
                <TableCell key={date} align="center" sx={{ minWidth: 80 }}>
                  <Box sx={{ display: 'flex', flexDirection: 'column', alignItems: 'center', gap: 0.5 }}>
                    <Typography variant="caption">{formatDate(date)}</Typography>
                    <Box>
                      <IconButton size="small" onClick={() => handleEditDate(index)}>
                        <EditIcon fontSize="small" />
                      </IconButton>
                      <IconButton size="small" onClick={() => handleDeleteDate(date)} color="error">
                        <DeleteIcon fontSize="small" />
                      </IconButton>
                    </Box>
                  </Box>
                </TableCell>
              ))}
            </TableRow>
          </TableHead>
          <TableBody>
            {students.map((student) => (
              <TableRow key={student.student_id}>
                <TableCell>{student.full_name}</TableCell>
                {dates.map((date) => {
                  const grade = getGradeForCell(student.student_id, date);
                  return (
                    <TableCell key={`${student.student_id}-${date}`} align="center">
                      <GradeCell
                        value={grade?.grade}
                        onClick={() => handleCellClick(student.student_id, date)}
                      />
                    </TableCell>
                  );
                })}
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>

      {modalOpen && (
        <GradeModal
          open={modalOpen}
          onClose={() => {
            setModalOpen(false);
            setSelectedGrade(null);
            setSelectedCell(null);
          }}
          grade={selectedGrade}
          studentId={selectedGrade?.student_id || selectedCell?.studentId || 0}
          subjectId={subjectId}
          teacherId={teacherId}
          defaultDate={selectedGrade?.date_issued || selectedCell?.date || new Date().toISOString().split('T')[0]}
          onSave={handleSaveGrade}
          onDelete={selectedGrade ? handleDeleteGrade : undefined}
        />
      )}

      <Dialog open={dateDialogOpen} onClose={() => setDateDialogOpen(false)}>
        <DialogTitle>
          {editingDateIndex !== null ? 'Редактировать дату' : 'Добавить дату'}
        </DialogTitle>
        <DialogContent>
          <TextField
            fullWidth
            type="date"
            value={newDate}
            onChange={(e) => setNewDate(e.target.value)}
            sx={{ mt: 2 }}
            InputLabelProps={{ shrink: true }}
          />
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setDateDialogOpen(false)}>Отмена</Button>
          <Button onClick={handleSaveDate} variant="contained">Сохранить</Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
}
