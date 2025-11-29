'use client';

import { useState, useEffect } from 'react';
import {
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  Button,
  TextField,
  Select,
  MenuItem,
  FormControl,
  InputLabel,
  Box,
} from '@mui/material';
import { Grade, GradeCreate } from '@/types';

interface GradeModalProps {
  open: boolean;
  onClose: () => void;
  grade?: Grade | null;
  studentId: number;
  subjectId: number;
  teacherId?: number;
  defaultDate: string;
  onSave: (data: GradeCreate) => void;
  onDelete?: (gradeId: number) => void;
}

const gradeValues = ['5', '4', '3', '2', '1', 'П', 'Б'];

export default function GradeModal({
  open,
  onClose,
  grade,
  studentId,
  subjectId,
  teacherId,
  defaultDate,
  onSave,
  onDelete,
}: GradeModalProps) {
  const [value, setValue] = useState('5');
  const [date, setDate] = useState(defaultDate);
  const [comment, setComment] = useState('');

  useEffect(() => {
    if (grade) {
      setValue(grade.grade || '5');
      setDate(grade.date_issued || defaultDate);
      setComment(grade.comment || '');
    } else {
      setValue('5');
      setDate(defaultDate);
      setComment('');
    }
  }, [grade, defaultDate]);

  const handleSave = () => {
    onSave({
      student_id: studentId,
      subject_id: subjectId,
      teacher_id: teacherId || null,
      grade: value,
      date_issued: date,
      comment: comment || null,
    });
    onClose();
  };

  const handleDelete = () => {
    if (grade && onDelete) {
      onDelete(grade.grade_id);
      onClose();
    }
  };

  return (
    <Dialog open={open} onClose={onClose} maxWidth="sm" fullWidth>
      <DialogTitle>
        {grade ? 'Редактировать оценку' : 'Добавить оценку'}
      </DialogTitle>
      <DialogContent>
        <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2, mt: 1 }}>
          <FormControl fullWidth>
            <InputLabel>Оценка</InputLabel>
            <Select
              value={value}
              label="Оценка"
              onChange={(e) => setValue(e.target.value)}
            >
              {gradeValues.map((val) => (
                <MenuItem key={val} value={val}>
                  {val}
                </MenuItem>
              ))}
            </Select>
          </FormControl>

          <TextField
            fullWidth
            label="Дата"
            type="date"
            value={date}
            onChange={(e) => setDate(e.target.value)}
            InputLabelProps={{ shrink: true }}
          />

          <TextField
            fullWidth
            label="Дополнительная информация"
            multiline
            rows={3}
            value={comment}
            onChange={(e) => setComment(e.target.value)}
            placeholder="Комментарий учителя"
          />
        </Box>
      </DialogContent>
      <DialogActions>
        {grade && onDelete && (
          <Button onClick={handleDelete} color="error" sx={{ mr: 'auto' }}>
            Удалить
          </Button>
        )}
        <Button onClick={onClose}>Отмена</Button>
        <Button onClick={handleSave} variant="contained">
          Сохранить
        </Button>
      </DialogActions>
    </Dialog>
  );
}
