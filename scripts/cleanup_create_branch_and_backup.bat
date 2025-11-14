@echo off
REM iLoveExcel - Cleanup: Create Branch and Backup
REM Creates a git branch and full repository backup before cleanup begins

setlocal enabledelayedexpansion

echo ==========================================
echo iLoveExcel - Cleanup Phase 0
echo Create Branch and Backup
echo ==========================================
echo.

REM Get project root
set SCRIPT_DIR=%~dp0
set PROJECT_ROOT=%SCRIPT_DIR%..
cd /d "%PROJECT_ROOT%"

echo Project root: %PROJECT_ROOT%
echo.

REM Generate timestamp
for /f "tokens=2 delims==" %%I in ('wmic os get localdatetime /format:list') do set datetime=%%I
set TIMESTAMP=%datetime:~0,8%_%datetime:~8,6%
set BRANCH_NAME=cleanup/%TIMESTAMP%
set BACKUP_FILE=cleanup\backup_%TIMESTAMP%.zip

REM Check if we're in a git repo
if not exist ".git" (
    echo [ERROR] Not in a git repository
    pause
    exit /b 1
)

REM Check for uncommitted changes
git diff-index --quiet HEAD -- >nul 2>&1
if errorlevel 1 (
    echo [WARNING] You have uncommitted changes
    echo.
    git status --short
    echo.
    set /p REPLY="Commit these changes before proceeding? (y/n): "
    if /i "!REPLY!"=="y" (
        echo.
        set /p COMMIT_MSG="Enter commit message: "
        git add -A
        git commit -m "!COMMIT_MSG!"
        echo [OK] Changes committed
    ) else (
        echo [WARNING] Proceeding with uncommitted changes...
    )
    echo.
)

REM Create cleanup branch
echo ^> Creating cleanup branch: %BRANCH_NAME%
git checkout -b "%BRANCH_NAME%"
if errorlevel 1 (
    echo [ERROR] Failed to create branch
    pause
    exit /b 1
)
echo [OK] Branch created and checked out
echo.

REM Create backup (using tar if available, otherwise 7z or PowerShell)
echo ^> Creating full repository backup...
cd ..
for %%I in ("%PROJECT_ROOT%") do set REPO_NAME=%%~nxI

REM Try PowerShell Compress-Archive
powershell -Command "Compress-Archive -Path '%REPO_NAME%' -DestinationPath '%PROJECT_ROOT%\%BACKUP_FILE%' -Force" >nul 2>&1

cd /d "%PROJECT_ROOT%"

if exist "%BACKUP_FILE%" (
    for %%A in ("%BACKUP_FILE%") do set BACKUP_SIZE=%%~zA
    echo [OK] Backup created: %BACKUP_FILE% (!BACKUP_SIZE! bytes)
) else (
    echo [ERROR] Backup failed
    pause
    exit /b 1
)
echo.

REM Run baseline tests
echo ^> Running baseline test suite...
echo.

set TEST_LOG=cleanup\test_results\baseline_%TIMESTAMP%.log
if not exist cleanup\test_results mkdir cleanup\test_results

where pytest >nul 2>&1
if %errorlevel% equ 0 (
    pytest tests/ -v > "%TEST_LOG%" 2>&1
    if %errorlevel% equ 0 (
        set TEST_RESULT=PASS
        echo [OK] All tests passed
    ) else (
        set TEST_RESULT=FAIL
        echo [ERROR] Some tests failed (see %TEST_LOG%)
        echo.
        echo Last lines of test output:
        powershell -Command "Get-Content '%TEST_LOG%' -Tail 20"
        echo.
        echo [NOTE] This is the baseline. Cleanup should not make it worse.
    )
) else (
    echo [WARNING] pytest not found, skipping baseline tests
    set TEST_RESULT=SKIPPED
)

echo.
echo Baseline test result: !TEST_RESULT! > cleanup\test_results\baseline_status.txt

REM Create cleanup state file
(
    echo CLEANUP_TIMESTAMP=%TIMESTAMP%
    echo CLEANUP_BRANCH=%BRANCH_NAME%
    echo CLEANUP_BACKUP=%BACKUP_FILE%
    echo BASELINE_TEST_RESULT=!TEST_RESULT!
    echo BASELINE_TEST_LOG=%TEST_LOG%
    echo PHASE_COMPLETED=0
    echo CURRENT_PHASE=Phase 0: Preparation
) > cleanup\cleanup_state.txt

echo ==========================================
echo [OK] Phase 0 Complete
echo ==========================================
echo.
echo Branch: %BRANCH_NAME%
echo Backup: %BACKUP_FILE%
echo Baseline tests: !TEST_RESULT!
echo.
echo Next steps:
echo   1. Run: scripts\cleanup_scan_candidates.bat
echo   2. Review: cleanup\cleanup_candidates.md
echo   3. Run: scripts\cleanup_present_and_confirm.bat
echo.
echo [WARNING] All cleanup operations will be done on branch: %BRANCH_NAME%
echo.

pause
