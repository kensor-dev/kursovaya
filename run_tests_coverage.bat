@echo off
echo ====================================
echo Запуск тестов с покрытием кода
echo ====================================
echo.

cd %~dp0
.venv\Scripts\python.exe -m pytest backend\tests\ --cov=backend\app --cov-report=html --cov-report=term-missing -v

echo.
echo ====================================
echo HTML отчет создан: htmlcov\index.html
echo ====================================
echo.
echo Открыть отчет? (y/n)
set /p choice=
if /i "%choice%"=="y" start htmlcov\index.html

pause
