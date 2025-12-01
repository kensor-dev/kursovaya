@echo off
echo ====================================
echo Запуск тестов kursovaya
echo ====================================
echo.

cd %~dp0
.venv\Scripts\python.exe -m pytest backend\tests\ -v --tb=short

echo.
echo ====================================
echo Тесты завершены
echo ====================================
pause
