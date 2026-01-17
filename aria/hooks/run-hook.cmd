@echo off
REM Aria Hooks Runner for Windows
REM 运行指定的 Hook 脚本

setlocal enabledelayedexpansion

REM 配置
set "SCRIPT_DIR=%~dp0"
set "PROJECT_ROOT=%SCRIPT_DIR%..\.."
set "HOOK_NAME=%~1"
set "HOOKS_CONFIG=%SCRIPT_DIR%hooks.json"

REM 颜色设置 (Windows 10+)
set "INFO=[INFO]"
set "SUCCESS=[OK]"
set "WARN=[WARN]"
set "ERROR=[ERROR]"

REM 日志函数
:log_info
echo %INFO% %~1
exit /b

:log_success
echo %SUCCESS% %~1
exit /b

:log_warn
echo %WARN% %~1
exit /b

:log_error
echo %ERROR% %~1
exit /b

REM 主函数
:main
echo.
call :log_info "Aria Hooks - %HOOK_NAME%"
echo ================================

REM 检查参数
if "%HOOK_NAME%"=="" (
    call :log_error "Usage: run-hook.cmd ^<hook-name^>"
    call :log_info "Available hooks: session-start, pre-commit, task-complete"
    exit /b 1
)

REM 检查配置文件
if not exist "%HOOKS_CONFIG%" (
    call :log_warn "Hooks configuration not found: %HOOKS_CONFIG%"
    exit /b 0
)

REM 执行对应的 Hook 脚本
if "%HOOK_NAME%"=="session-start" (
    if exist "%SCRIPT_DIR%session-start.cmd" (
        call "%SCRIPT_DIR%session-start.cmd"
    ) else (
        call :log_info "Session start checks (inline)"
        call :run_session_start
    )
) else if "%HOOK_NAME%"=="pre-commit" (
    call :log_info "Pre-commit hook not yet implemented"
) else if "%HOOK_NAME%"=="task-complete" (
    call :log_info "Task-complete hook not yet implemented"
) else (
    call :log_error "Unknown hook: %HOOK_NAME%"
    exit /b 1
)

echo.
call :log_success "Hook %HOOK_NAME% completed"
echo.
exit /b 0

REM Session start 检查
:run_session_start
REM 检查 Git 状态
call :log_info "Checking Git status..."
if exist ".git" (
    call :log_success "Git repository detected"
) else (
    call :log_info "Not a Git repository"
)

REM 检查子模块
call :log_info "Checking submodules..."
if exist ".gitmodules" (
    call :log_success "Gitmodules found"
)

REM 检查 Python
call :log_info "Checking Python environment..."
where python >nul 2>&1
if %errorlevel% equ 0 (
    for /f "tokens=2" %%v in ('python --version 2^>^&1') do set PYTHON_VERSION=%%v
    call :log_success "Python %PYTHON_VERSION%"
) else (
    call :log_warn "Python not found"
)

REM 检查 Node.js
call :log_info "Checking Node.js environment..."
where node >nul 2>&1
if %errorlevel% equ 0 (
    for /f "tokens=*" %%v in ('node --version') do set NODE_VERSION=%%v
    call :log_success "Node.js %NODE_VERSION%"
) else (
    call :log_info "Node.js not found"
)

exit /b

REM 执行主函数
call :main %*
