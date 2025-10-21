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
import { classesApi } from '@/lib/api';
import { SchoolClass, SchoolClassCreate } from '@/types';

export default function ClassesPage() {
  const [classes, setClasses] = useState<SchoolClass[]>([]);
  const [open, setOpen] = useState(false);
  const [editingClass, setEditingClass] = useState<SchoolClass | null>(null);
  const [formData, setFormData] = useState<SchoolClassCreate>({
    number_letter: '',
    class_teacher_id: null,
  });

  useEffect(() => {
    fetchClasses();
  }, []);

  const fetchClasses = async () => {
    try {
      const response = await classesApi.getAll();
      setClasses(response.data);
    } catch (error) {
      console.error('Ошибка при загрузке классов:', error);
    }
  };

  const handleOpen = (schoolClass?: SchoolClass) => {
    if (schoolClass) {
      setEditingClass(schoolClass);
      setFormData({
        number_letter: schoolClass.number_letter,
        class_teacher_id: schoolClass.class_teacher_id,
      });
    } else {
      setEditingClass(null);
      setFormData({
        number_letter: '',
        class_teacher_id: null,
      });
    }
    setOpen(true);
  };

  const handleClose = () => {
    setOpen(false);
    setEditingClass(null);
  };

  const handleSubmit = async () => {
    try {
      if (editingClass) {
        await classesApi.update(editingClass.class_id, formData);
      } else {
        await classesApi.create(formData);
      }
      handleClose();
      fetchClasses();
    } catch (error) {
      console.error('Ошибка при сохранении класса:', error);
    }
  };

  const handleDelete = async (id: number) => {
    if (confirm('Вы уверены, что хотите удалить этот класс?')) {
      try {
        await classesApi.delete(id);
        fetchClasses();
      } catch (error) {
        console.error('Ошибка при удалении класса:', error);
      }
    }
  };

  return (
    <Box>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 3 }}>
        <Typography variant="h4" component="h1">
          Классы
        </Typography>
        <Button
          variant="contained"
          startIcon={<AddIcon />}
          onClick={() => handleOpen()}
        >
          Добавить класс
        </Button>
      </Box>

      <TableContainer component={Paper}>
        <Table>
          <TableHead>
            <TableRow>
              <TableCell>ID</TableCell>
              <TableCell>Класс</TableCell>
              <TableCell>Классный руководитель</TableCell>
              <TableCell>Действия</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {classes.map((schoolClass) => (
              <TableRow key={schoolClass.class_id}>
                <TableCell>{schoolClass.class_id}</TableCell>
                <TableCell>{schoolClass.number_letter}</TableCell>
                <TableCell>{schoolClass.class_teacher?.full_name || '-'}</TableCell>
                <TableCell>
                  <IconButton
                    size="small"
                    onClick={() => handleOpen(schoolClass)}
                    color="primary"
                  >
                    <EditIcon />
                  </IconButton>
                  <IconButton
                    size="small"
                    onClick={() => handleDelete(schoolClass.class_id)}
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
          {editingClass ? 'Редактировать класс' : 'Добавить класс'}
        </DialogTitle>
        <DialogContent>
          <TextField
            fullWidth
            label="Класс (например: 5А, 11Б)"
            value={formData.number_letter}
            onChange={(e) => setFormData({ ...formData, number_letter: e.target.value })}
            margin="normal"
          />
          <TextField
            fullWidth
            label="ID классного руководителя"
            type="number"
            value={formData.class_teacher_id || ''}
            onChange={(e) => setFormData({ ...formData, class_teacher_id: e.target.value ? Number(e.target.value) : null })}
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
