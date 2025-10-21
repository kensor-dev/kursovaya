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
import { studentsApi } from '@/lib/api';
import { Student, StudentCreate } from '@/types';

export default function StudentsPage() {
  const [students, setStudents] = useState<Student[]>([]);
  const [open, setOpen] = useState(false);
  const [editingStudent, setEditingStudent] = useState<Student | null>(null);
  const [formData, setFormData] = useState<StudentCreate>({
    full_name: '',
    date_of_birth: '',
    class_id: null,
    contact_info: '',
    additional_info: '',
    parent_id: null,
  });

  useEffect(() => {
    fetchStudents();
  }, []);

  const fetchStudents = async () => {
    try {
      const response = await studentsApi.getAll();
      setStudents(response.data);
    } catch (error) {
      console.error('Ошибка при загрузке учеников:', error);
    }
  };

  const handleOpen = (student?: Student) => {
    if (student) {
      setEditingStudent(student);
      setFormData({
        full_name: student.full_name,
        date_of_birth: student.date_of_birth || '',
        class_id: student.class_id,
        contact_info: student.contact_info || '',
        additional_info: student.additional_info || '',
        parent_id: student.parent_id,
      });
    } else {
      setEditingStudent(null);
      setFormData({
        full_name: '',
        date_of_birth: '',
        class_id: null,
        contact_info: '',
        additional_info: '',
        parent_id: null,
      });
    }
    setOpen(true);
  };

  const handleClose = () => {
    setOpen(false);
    setEditingStudent(null);
  };

  const handleSubmit = async () => {
    try {
      if (editingStudent) {
        await studentsApi.update(editingStudent.student_id, formData);
      } else {
        await studentsApi.create(formData);
      }
      handleClose();
      fetchStudents();
    } catch (error) {
      console.error('Ошибка при сохранении ученика:', error);
    }
  };

  const handleDelete = async (id: number) => {
    if (confirm('Вы уверены, что хотите удалить этого ученика?')) {
      try {
        await studentsApi.delete(id);
        fetchStudents();
      } catch (error) {
        console.error('Ошибка при удалении ученика:', error);
      }
    }
  };

  return (
    <Box>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 3 }}>
        <Typography variant="h4" component="h1">
          Ученики
        </Typography>
        <Button
          variant="contained"
          startIcon={<AddIcon />}
          onClick={() => handleOpen()}
        >
          Добавить ученика
        </Button>
      </Box>

      <TableContainer component={Paper}>
        <Table>
          <TableHead>
            <TableRow>
              <TableCell>ID</TableCell>
              <TableCell>ФИО</TableCell>
              <TableCell>Дата рождения</TableCell>
              <TableCell>Класс</TableCell>
              <TableCell>Контакты</TableCell>
              <TableCell>Действия</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {students.map((student) => (
              <TableRow key={student.student_id}>
                <TableCell>{student.student_id}</TableCell>
                <TableCell>{student.full_name}</TableCell>
                <TableCell>{student.date_of_birth || '-'}</TableCell>
                <TableCell>{student.school_class?.number_letter || '-'}</TableCell>
                <TableCell>{student.contact_info || '-'}</TableCell>
                <TableCell>
                  <IconButton
                    size="small"
                    onClick={() => handleOpen(student)}
                    color="primary"
                  >
                    <EditIcon />
                  </IconButton>
                  <IconButton
                    size="small"
                    onClick={() => handleDelete(student.student_id)}
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
          {editingStudent ? 'Редактировать ученика' : 'Добавить ученика'}
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
            label="Дата рождения"
            type="date"
            value={formData.date_of_birth}
            onChange={(e) => setFormData({ ...formData, date_of_birth: e.target.value })}
            margin="normal"
            InputLabelProps={{ shrink: true }}
          />
          <TextField
            fullWidth
            label="ID класса"
            type="number"
            value={formData.class_id || ''}
            onChange={(e) => setFormData({ ...formData, class_id: e.target.value ? Number(e.target.value) : null })}
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
          <TextField
            fullWidth
            label="Дополнительная информация"
            value={formData.additional_info}
            onChange={(e) => setFormData({ ...formData, additional_info: e.target.value })}
            margin="normal"
            multiline
            rows={2}
          />
          <TextField
            fullWidth
            label="ID родителя"
            type="number"
            value={formData.parent_id || ''}
            onChange={(e) => setFormData({ ...formData, parent_id: e.target.value ? Number(e.target.value) : null })}
            margin="normal"
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
