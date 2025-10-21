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
import { parentsApi } from '@/lib/api';
import { Parent, ParentCreate } from '@/types';

export default function ParentsPage() {
  const [parents, setParents] = useState<Parent[]>([]);
  const [open, setOpen] = useState(false);
  const [editingParent, setEditingParent] = useState<Parent | null>(null);
  const [formData, setFormData] = useState<ParentCreate>({
    full_name: '',
    contact_info: '',
    student_relation: '',
  });

  useEffect(() => {
    fetchParents();
  }, []);

  const fetchParents = async () => {
    try {
      const response = await parentsApi.getAll();
      setParents(response.data);
    } catch (error) {
      console.error('Ошибка при загрузке родителей:', error);
    }
  };

  const handleOpen = (parent?: Parent) => {
    if (parent) {
      setEditingParent(parent);
      setFormData({
        full_name: parent.full_name,
        contact_info: parent.contact_info || '',
        student_relation: parent.student_relation || '',
      });
    } else {
      setEditingParent(null);
      setFormData({
        full_name: '',
        contact_info: '',
        student_relation: '',
      });
    }
    setOpen(true);
  };

  const handleClose = () => {
    setOpen(false);
    setEditingParent(null);
  };

  const handleSubmit = async () => {
    try {
      if (editingParent) {
        await parentsApi.update(editingParent.parent_id, formData);
      } else {
        await parentsApi.create(formData);
      }
      handleClose();
      fetchParents();
    } catch (error) {
      console.error('Ошибка при сохранении родителя:', error);
    }
  };

  const handleDelete = async (id: number) => {
    if (confirm('Вы уверены, что хотите удалить этого родителя?')) {
      try {
        await parentsApi.delete(id);
        fetchParents();
      } catch (error) {
        console.error('Ошибка при удалении родителя:', error);
      }
    }
  };

  return (
    <Box>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 3 }}>
        <Typography variant="h4" component="h1">
          Родители
        </Typography>
        <Button
          variant="contained"
          startIcon={<AddIcon />}
          onClick={() => handleOpen()}
        >
          Добавить родителя
        </Button>
      </Box>

      <TableContainer component={Paper}>
        <Table>
          <TableHead>
            <TableRow>
              <TableCell>ID</TableCell>
              <TableCell>ФИО</TableCell>
              <TableCell>Контакты</TableCell>
              <TableCell>Связь с учеником</TableCell>
              <TableCell>Действия</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {parents.map((parent) => (
              <TableRow key={parent.parent_id}>
                <TableCell>{parent.parent_id}</TableCell>
                <TableCell>{parent.full_name}</TableCell>
                <TableCell>{parent.contact_info || '-'}</TableCell>
                <TableCell>{parent.student_relation || '-'}</TableCell>
                <TableCell>
                  <IconButton
                    size="small"
                    onClick={() => handleOpen(parent)}
                    color="primary"
                  >
                    <EditIcon />
                  </IconButton>
                  <IconButton
                    size="small"
                    onClick={() => handleDelete(parent.parent_id)}
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
          {editingParent ? 'Редактировать родителя' : 'Добавить родителя'}
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
            label="Контактная информация"
            value={formData.contact_info}
            onChange={(e) => setFormData({ ...formData, contact_info: e.target.value })}
            margin="normal"
            multiline
            rows={2}
          />
          <TextField
            fullWidth
            label="Связь с учеником (мать, отец, опекун)"
            value={formData.student_relation}
            onChange={(e) => setFormData({ ...formData, student_relation: e.target.value })}
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
