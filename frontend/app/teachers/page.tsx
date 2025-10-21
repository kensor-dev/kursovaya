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
import { teachersApi } from '@/lib/api';
import { Teacher, TeacherCreate } from '@/types';

export default function TeachersPage() {
  const [teachers, setTeachers] = useState<Teacher[]>([]);
  const [open, setOpen] = useState(false);
  const [editingTeacher, setEditingTeacher] = useState<Teacher | null>(null);
  const [formData, setFormData] = useState<TeacherCreate>({
    full_name: '',
    contact_info: '',
    position: '',
  });

  useEffect(() => {
    fetchTeachers();
  }, []);

  const fetchTeachers = async () => {
    try {
      const response = await teachersApi.getAll();
      setTeachers(response.data);
    } catch (error) {
      console.error('Ошибка при загрузке учителей:', error);
    }
  };

  const handleOpen = (teacher?: Teacher) => {
    if (teacher) {
      setEditingTeacher(teacher);
      setFormData({
        full_name: teacher.full_name,
        contact_info: teacher.contact_info || '',
        position: teacher.position || '',
      });
    } else {
      setEditingTeacher(null);
      setFormData({
        full_name: '',
        contact_info: '',
        position: '',
      });
    }
    setOpen(true);
  };

  const handleClose = () => {
    setOpen(false);
    setEditingTeacher(null);
  };

  const handleSubmit = async () => {
    try {
      if (editingTeacher) {
        await teachersApi.update(editingTeacher.teacher_id, formData);
      } else {
        await teachersApi.create(formData);
      }
      handleClose();
      fetchTeachers();
    } catch (error) {
      console.error('Ошибка при сохранении учителя:', error);
    }
  };

  const handleDelete = async (id: number) => {
    if (confirm('Вы уверены, что хотите удалить этого учителя?')) {
      try {
        await teachersApi.delete(id);
        fetchTeachers();
      } catch (error) {
        console.error('Ошибка при удалении учителя:', error);
      }
    }
  };

  return (
    <Box>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 3 }}>
        <Typography variant="h4" component="h1">
          Учителя
        </Typography>
        <Button
          variant="contained"
          startIcon={<AddIcon />}
          onClick={() => handleOpen()}
        >
          Добавить учителя
        </Button>
      </Box>

      <TableContainer component={Paper}>
        <Table>
          <TableHead>
            <TableRow>
              <TableCell>ID</TableCell>
              <TableCell>ФИО</TableCell>
              <TableCell>Должность</TableCell>
              <TableCell>Контакты</TableCell>
              <TableCell>Действия</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {teachers.map((teacher) => (
              <TableRow key={teacher.teacher_id}>
                <TableCell>{teacher.teacher_id}</TableCell>
                <TableCell>{teacher.full_name}</TableCell>
                <TableCell>{teacher.position || '-'}</TableCell>
                <TableCell>{teacher.contact_info || '-'}</TableCell>
                <TableCell>
                  <IconButton
                    size="small"
                    onClick={() => handleOpen(teacher)}
                    color="primary"
                  >
                    <EditIcon />
                  </IconButton>
                  <IconButton
                    size="small"
                    onClick={() => handleDelete(teacher.teacher_id)}
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
          {editingTeacher ? 'Редактировать учителя' : 'Добавить учителя'}
        </DialogTitle>
        <DialogContent>
          <TextField
            fullWidth
            label="ФИО"
            value={formData.full_name}
            onChange={(e) => setFormData({ ...formData, full_name: e.target.value })}
            margin="normal"
          />
          <TextField
            fullWidth
            label="Должность"
            value={formData.position}
            onChange={(e) => setFormData({ ...formData, position: e.target.value })}
            margin="normal"
          />
          <TextField
            fullWidth
            label="Контактная информация"
            value={formData.contact_info}
            onChange={(e) => setFormData({ ...formData, contact_info: e.target.value })}
            margin="normal"
            multiline
            rows={2}
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
