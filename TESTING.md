# Инструкция по запуску тестов

## 🚀 Быстрый запуск

### Вариант 1: Двойной клик (Windows)

1. **Обычный запуск тестов:**
   - Дважды кликните на `run_tests.bat`

2. **Запуск с покрытием кода:**
   - Дважды кликните на `run_tests_coverage.bat`

### Вариант 2: Командная строка

```bash
# Обычный запуск
.venv\Scripts\python.exe -m pytest backend\tests\ -v

# С покрытием кода
.venv\Scripts\python.exe -m pytest backend\tests\ --cov=backend\app --cov-report=html

# Быстрый запуск (без traceback)
.venv\Scripts\python.exe -m pytest backend\tests\ --tb=no -q
```

### Вариант 3: Из активированного venv

```bash
# Активировать виртуальное окружение
.venv\Scripts\activate

# Запустить тесты
cd backend
pytest tests/ -v

# С покрытием
pytest tests/ --cov=app --cov-report=html
```

## 📊 Результаты

После запуска вы увидите:
- ✅ **84 теста** должны пройти
- ⏱️ **~18-20 секунд** время выполнения
- 📈 **95% покрытие кода**

## 📝 Дополнительная документация

Полная документация по тестам находится в:
- `kursovaya-docs/testing.md` - подробное руководство
- `kursovaya-docs/TESTS-CHECKLIST.md` - чек-лист тестов
- `kursovaya-docs/TESTS-SUMMARY.md` - сводка результатов

## ❗ Решение проблем

**Ошибка: `No module named 'httpx'`**
```bash
# Переустановить зависимости
.venv\Scripts\python.exe -m pip install -r backend\requirements.txt
```

**Ошибка: `ModuleNotFoundError: No module named 'app'`**
```bash
# Убедитесь что запускаете из корня проекта
cd C:\Users\Public\projects\kursovaya
```

**Тесты не находятся:**
```bash
# Убедитесь что находитесь в правильной директории
cd backend
pytest tests/ -v
```
