@echo off
REM Activate the virtual environment
call venv\Scripts\activate

REM Set environment variables
set PYTHONPATH=.

REM Start the FastAPI server
uvicorn main:app --host 0.0.0.0 --port 8000 --reload

REM Keep the console window open
pause
