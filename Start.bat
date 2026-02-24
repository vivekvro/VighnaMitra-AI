@echo off
echo Activating virtual environment...
call naradenv\Scripts\activate

echo.
echo Starting FastAPI server...
start cmd /k "python -m uvicorn backend.api.routes:app --reload --host 127.0.0.1 --port 8000"

timeout /t 5

echo.
echo Starting Streamlit frontend...
start cmd /k "python -m streamlit run frontend\app.py"

echo.
echo Project is running...
pause