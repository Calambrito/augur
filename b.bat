@echo off
echo Starting ML Pipeline Execution...
echo.

echo Running flow1.py...
python flow1.py
if errorlevel 1 (
    echo Error: flow1.py failed
    pause
    exit /b 1
)
echo flow1.py completed successfully.
echo.

echo Running flow2.py...
python flow2.py
if errorlevel 1 (
    echo Error: flow2.py failed
    pause
    exit /b 1
)
echo flow2.py completed successfully.
echo.

echo Running flow3.py...
python flow3.py
if errorlevel 1 (
    echo Error: flow3.py failed
    pause
    exit /b 1
)
echo flow3.py completed successfully.
echo.

echo Running flow4.py...
python flow4.py
if errorlevel 1 (
    echo Error: flow4.py failed
    pause
    exit /b 1
)
echo flow3.py completed successfully.
echo.

echo Running buildrf.py...
python buildrf.py
if errorlevel 1 (
    echo Error: build.py failed
    pause
    exit /b 1
)
echo build.py completed successfully.
echo.

echo Running validaterf.py...
python validaterf.py
if errorlevel 1 (
    echo Error: validate.py failed
    pause
    exit /b 1
)
echo validate.py completed successfully.
echo.

echo Running testrf.py...
python testrf.py
if errorlevel 1 (
    echo Error: test.py failed
    pause
    exit /b 1
)
echo test.py completed successfully.
echo.

echo ===========================================
echo All pipeline steps completed successfully!
echo ===========================================
pause