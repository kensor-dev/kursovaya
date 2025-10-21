# 📚 Система учёта успеваемости

Полнофункциональная система управления школьными данными с веб-интерфейсом для учета успеваемости учащихся.

## 🎯 Описание проекта

Система предназначена для автоматизации учебного процесса и включает управление:
- 👨‍🎓 Учениками
- 👨‍🏫 Учителями
- 📖 Предметами
- 🏫 Классами
- 📝 Оценками
- 👪 Родителями
- 📔 Журналами успеваемости

## 🛠 Технологический стек

### Backend
- **FastAPI** - современный веб-фреймворк
- **SQLAlchemy** - ORM для работы с БД
- **PostgreSQL** - реляционная база данных
- **Pydantic** - валидация данных
- **Alembic** - миграции базы данных
- **Uvicorn** - ASGI сервер

### Frontend
- **Next.js 15** - React фреймворк с серверным рендерингом
- **TypeScript** - типизированный JavaScript
- **Material-UI (MUI)** - компоненты интерфейса
- **Axios** - HTTP клиент
- **Tailwind CSS** - утилитарные стили

## 📋 Требования

Перед установкой убедитесь, что у вас установлены:
- **Python** 3.8 или выше
- **Node.js** 18 или выше
- **PostgreSQL** 12 или выше
- **Git**

## 🚀 Быстрый старт

### 1. Клонирование репозитория

```bash
git clone <repository-url>
cd kursovaya
```

### 2. Установка зависимостей

#### Установка всех зависимостей одной командой:
```bash
npm run install:all
```

#### Или установка по отдельности:

**Корневые зависимости:**
```bash
npm install
```

**Backend:**
```bash
cd backend
pip install -r requirements.txt
```

**Frontend:**
```bash
cd frontend
npm install
```

### 3. Настройка базы данных

#### Создание базы данных:
```bash
psql -U postgres
CREATE DATABASE kursovaya;
\q
```

#### Настройка переменных окружения:

Создайте файл \`backend/app/.env\`:
```env
DB_CONNECTION_STRING=postgresql://postgres:ваш_пароль@localhost:5432/kursovaya
```

#### Применение миграций:
```bash
cd backend
alembic upgrade head
```

### 4. Запуск приложения

#### Запуск backend и frontend одновременно:
```bash
npm run dev
```

#### Или запуск по отдельности:

**Backend (порт 8000):**
```bash
npm run dev:backend
```

**Frontend (порт 3000):**
```bash
npm run dev:frontend
```

## 📱 Доступ к приложению

После запуска приложение будет доступно по адресам:

- **Frontend:** http://localhost:3000
- **Backend API:** http://localhost:8000
- **API документация (Swagger):** http://localhost:8000/docs
- **API документация (ReDoc):** http://localhost:8000/redoc

## 📊 API Endpoints

### Ученики
- \`GET /students/\` - Список всех учеников
- \`POST /students/\` - Создать ученика
- \`GET /students/{id}\` - Получить ученика по ID
- \`PUT /students/{id}\` - Обновить ученика
- \`DELETE /students/{id}\` - Удалить ученика

### Учителя
- \`GET /teachers/\` - Список всех учителей
- \`POST /teachers/\` - Создать учителя
- \`GET /teachers/{id}\` - Получить учителя по ID
- \`PUT /teachers/{id}\` - Обновить учителя
- \`DELETE /teachers/{id}\` - Удалить учителя

### Предметы
- \`GET /subjects/\` - Список всех предметов
- \`POST /subjects/\` - Создать предмет
- \`GET /subjects/{id}\` - Получить предмет по ID
- \`PUT /subjects/{id}\` - Обновить предмет
- \`DELETE /subjects/{id}\` - Удалить предмет

### Классы
- \`GET /classes/\` - Список всех классов
- \`POST /classes/\` - Создать класс
- \`GET /classes/{id}\` - Получить класс по ID
- \`PUT /classes/{id}\` - Обновить класс
- \`DELETE /classes/{id}\` - Удалить класс

### Оценки
- \`GET /grades/\` - Список всех оценок
- \`POST /grades/\` - Создать оценку
- \`GET /grades/{id}\` - Получить оценку по ID
- \`PUT /grades/{id}\` - Обновить оценку
- \`DELETE /grades/{id}\` - Удалить оценку

### Родители
- \`GET /parents/\` - Список всех родителей
- \`POST /parents/\` - Создать родителя
- \`GET /parents/{id}\` - Получить родителя по ID
- \`PUT /parents/{id}\` - Обновить родителя
- \`DELETE /parents/{id}\` - Удалить родителя

## 🎨 Возможности интерфейса

- ✨ Современный Material Design интерфейс
- 📱 Адаптивная верстка для всех устройств
- 🎯 Интуитивная навигация
- ⚡ Быстрая работа благодаря Next.js
- 🔄 Автоматическое обновление данных
- ✏️ Создание, редактирование и удаление записей
- 📋 Таблицы с данными
- 🔍 Просмотр детальной информации

## 🔧 Управление базой данных

### Создание новой миграции:
```bash
cd backend
alembic revision --autogenerate -m "описание изменений"
```

### Применение миграций:
```bash
alembic upgrade head
```

### Откат последней миграции:
```bash
alembic downgrade -1
```

### Очистка базы данных:
```bash
psql -U postgres -d kursovaya -f drop_tables.sql
```

## 👤 Автор

Курсовая работа по дисциплине "Базы данных"

Остапенко Валентина Михайловна

---

**Статус проекта:** В разработке 
**Версия:** 1.0.0
