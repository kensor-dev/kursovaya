'use client';

import { useState, useEffect } from 'react';
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
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  TextField,
  IconButton,
} from '@mui/material';
import AddIcon from '@mui/icons-material/Add';
import EditIcon from '@mui/icons-material/Edit';
import DeleteIcon from '@mui/icons-material/Delete';
import { gradesApi } from '@/lib/api';
import { Grade, GradeCreate } from '@/types';

export default function GradesPage() {
  const [grades, setGrades] = useState<Grade[]>([]);
  const [open, setOpen] = useState(false);
  const [editingGrade, setEditingGrade] = useState<Grade | null>(null);
  const [formData, setFormData] = useState<GradeCreate>({
    student_id: 0,
    subject_id: 0,
    teacher_id: null,
    date_issued: '',
    grade: null,
    comment: '',
  });

  useEffect(() => {
    fetchGrades();
  }, []);

  const fetchGrades = async () => {
    try {
      const response = await gradesApi.getAll();
      setGrades(response.data);
    } catch (error) {
      console.error('Ошибка при загрузке оценок:', error);
    }
  };

  const handleOpen = (grade?: Grade) => {
    if (grade) {
      setEditingGrade(grade);
      setFormData({
        student_id: grade.student_id,
        subject_id: grade.subject_id,
        teacher_id: grade.teacher_id,
        date_issued: grade.date_issued || '',
        grade: grade.grade,
        comment: grade.comment || '',
      });
    } else {
      setEditingGrade(null);
      setFormData({
        student_id: 0,
        subject_id: 0,
        teacher_id: null,
        date_issued: '',
        grade: null,
        comment: '',
      });
    }
    setOpen(true);
  };

  const handleClose = () => {
    setOpen(false);
    setEditingGrade(null);
  };

  const handleSubmit = async () => {
    try {
      if (editingGrade) {
        await gradesApi.update(editingGrade.grade_id, formData);
      } else {
        await gradesApi.create(formData);
      }
      handleClose();
      fetchGrades();
    } catch (error) {
      console.error('Ошибка при сохранении оценки:', error);
    }
  };

  const handleDelete = async (id: number) => {
    if (confirm('Вы уверены, что хотите удалить эту оценку?')) {
      try {
        await gradesApi.delete(id);
        fetchGrades();
      } catch (error) {
        console.error('Ошибка при удалении оценки:', error);
      }
    }
  };

  return (
    <Box>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 3 }}>
        <Typography variant="h4" component="h1">
          Оценки
        </Typography>
        <Button
          variant="contained"
          startIcon={<AddIcon />}
          onClick={() => handleOpen()}
        >
          Добавить оценку
        </Button>
      </Box>

      <TableContainer component={Paper}>
        <Table>
          <TableHead>
            <TableRow>
              <TableCell>ID</TableCell>
              <TableCell>Ученик</TableCell>
              <TableCell>Предмет</TableCell>
              <TableCell>Оценка</TableCell>
              <TableCell>Дата</TableCell>
              <TableCell>Учитель</TableCell>
              <TableCell>Комментарий</TableCell>
              <TableCell>Действия</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {grades.map((grade) => (
              <TableRow key={grade.grade_id}>
                <TableCell>{grade.grade_id}</TableCell>
                <TableCell>{grade.student?.full_name || grade.student_id}</TableCell>
                <TableCell>{grade.subject?.name || grade.subject_id}</TableCell>
                <TableCell>{grade.grade || '-'}</TableCell>
                <TableCell>{grade.date_issued || '-'}</TableCell>
                <TableCell>{grade.teacher_id || '-'}</TableCell>
                <TableCell>{grade.comment || '-'}</TableCell>
                <TableCell>
                  <IconButton
                    size="small"
                    onClick={() => handleOpen(grade)}
                    color="primary"
                  >
                    <EditIcon />
                  </IconButton>
                  <IconButton
                    size="small"
                    onClick={() => handleDelete(grade.grade_id)}
                    color="error"
                  >
                    <DeleteIcon />
                  </IconButton>
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>

      <Dialog open={open} onClose={handleClose} maxWidth="sm" fullWidth>
        <DialogTitle>
          {editingGrade ? 'Редактировать оценку' : 'Добавить оценку'}
        </DialogTitle>
        <DialogContent>
          <TextField
            fullWidth
            label="ID ученика"
            type="number"
            value={formData.student_id}
            onChange={(e) => setFormData({ ...formData, student_id: Number(e.target.value) })}
            margin="normal"
          />
          <TextField
            fullWidth
            label="ID предмета"
            type="number"
            value={formData.subject_id}
            onChange={(e) => setFormData({ ...formData, subject_id: Number(e.target.value) })}
            margin="normal"
          />
          <TextField
            fullWidth
            label="Оценка"
            type="number"
            value={formData.grade || ''}
            onChange={(e) => setFormData({ ...formData, grade: e.target.value ? Number(e.target.value) : null })}
            margin="normal"
          />
          <TextField
            fullWidth
            label="Дата"
            type="date"
            value={formData.date_issued}
            onChange={(e) => setFormData({ ...formData, date_issued: e.target.value })}
            margin="normal"
            InputLabelProps={{ shrink: true }}
          />
          <TextField
            fullWidth
            label="ID учителя"
            type="number"
            value={formData.teacher_id || ''}
            onChange={(e) => setFormData({ ...formData, teacher_id: e.target.value ? Number(e.target.value) : null })}
            margin="normal"
          />
          <TextField
            fullWidth
            label="Комментарий"
            value={formData.comment}
            onChange={(e) => setFormData({ ...formData, comment: e.target.value })}
            margin="normal"
            multiline
            rows={3}
          />
        </DialogContent>
        <DialogActions>
          <Button onClick={handleClose}>Отмена</Button>
          <Button onClick={handleSubmit} variant="contained">
            Сохранить
          </Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
}
