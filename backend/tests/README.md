# Backend Tests

## Быстрый старт

```bash
# Установить зависимости
pip install -r ../requirements.txt

# Запустить все тесты
pytest -v

# С покрытием кода
pytest --cov=app --cov-report=html
```

## Структура

```
tests/
├── conftest.py          # Fixtures и конфигурация
├── test_models.py       # Тесты SQLAlchemy моделей (31 тест)
├── test_crud.py         # Тесты CRUD операций (14 тестов)
├── test_api.py          # Тесты API endpoints (39 тестов)
└── README.md           # Этот файл
```

## Результаты

- **Всего тестов:** 84
- **Покрытие кода:** 95%
- **Время выполнения:** ~18 секунд

## Документация

Полная документация в `kursovaya-docs/`:
- `testing.md` - подробное руководство
- `TESTS-CHECKLIST.md` - чек-лист тестов
- `TESTS-SUMMARY.md` - сводка результатов
