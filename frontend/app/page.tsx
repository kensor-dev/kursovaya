'use client';

import { Box, Grid, Paper, Typography } from '@mui/material';
import SchoolIcon from '@mui/icons-material/School';
import PersonIcon from '@mui/icons-material/Person';
import BookIcon from '@mui/icons-material/Book';
import ClassIcon from '@mui/icons-material/Class';
import GradeIcon from '@mui/icons-material/Grade';
import PeopleIcon from '@mui/icons-material/People';

const dashboardCards = [
  { title: 'Ученики', icon: <SchoolIcon sx={{ fontSize: 48 }} />, color: '#1976d2', link: '/students' },
  { title: 'Учителя', icon: <PersonIcon sx={{ fontSize: 48 }} />, color: '#dc004e', link: '/teachers' },
  { title: 'Предметы', icon: <BookIcon sx={{ fontSize: 48 }} />, color: '#388e3c', link: '/subjects' },
  { title: 'Классы', icon: <ClassIcon sx={{ fontSize: 48 }} />, color: '#f57c00', link: '/classes' },
  { title: 'Оценки', icon: <GradeIcon sx={{ fontSize: 48 }} />, color: '#7b1fa2', link: '/grades' },
  { title: 'Родители', icon: <PeopleIcon sx={{ fontSize: 48 }} />, color: '#0288d1', link: '/parents' },
];

export default function Home() {
  return (
    <Box>
      <Typography variant="h4" component="h1" gutterBottom>
        Система управления школой
      </Typography>
      <Typography variant="body1" paragraph color="text.secondary">
        Добро пожаловать в систему учёта успеваемости
      </Typography>
      <Grid container spacing={3} sx={{ mt: 2 }}>
        {dashboardCards.map((card) => (
          <Grid item xs={12} sm={6} md={4} key={card.title}>
            <Paper
              sx={{
                p: 3,
                display: 'flex',
                flexDirection: 'column',
                alignItems: 'center',
                cursor: 'pointer',
                transition: 'transform 0.2s',
                '&:hover': {
                  transform: 'scale(1.05)',
                  boxShadow: 4,
                },
              }}
              onClick={() => window.location.href = card.link}
            >
              <Box sx={{ color: card.color, mb: 2 }}>
                {card.icon}
              </Box>
              <Typography variant="h6" component="h2">
                {card.title}
              </Typography>
            </Paper>
          </Grid>
        ))}
      </Grid>
    </Box>
  );
}
