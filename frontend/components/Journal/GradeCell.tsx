'use client';

import { Box, Button } from '@mui/material';

interface GradeCellProps {
  value?: string;
  onClick: () => void;
}

const getGradeColor = (value?: string) => {
  if (!value) return '#e0e0e0';
  
  switch (value) {
    case '5':
    case '4':
      return '#51f88b';
    case '3':
      return '#F5B048';
    case '2':
    case '1':
      return '#DF4949';
    case 'П':
      return '#BDBDBD';
    case 'Б':
      return '#90CAF9';
    default:
      return '#e0e0e0';
  }
};

export default function GradeCell({ value, onClick }: GradeCellProps) {
  const bgColor = getGradeColor(value);
  
  return (
    <Box
      component="button"
      onClick={onClick}
      sx={{
        minWidth: '40px',
        minHeight: '40px',
        borderRadius: '8px',
        border: 'none',
        backgroundColor: bgColor,
        color: value ? '#000' : '#999',
        fontWeight: '600',
        fontSize: '14px',
        cursor: 'pointer',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        transition: 'all 0.2s',
        '&:hover': {
          opacity: 0.8,
          transform: 'scale(1.05)',
        },
        '&:focus': {
          outline: '2px solid #1976d2',
          outlineOffset: '2px',
        },
      }}
    >
      {value || '+'}
    </Box>
  );
}
