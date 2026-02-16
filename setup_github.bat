@echo off
echo ========================================
echo 游戏启动器 - GitHub 仓库初始化脚本
echo Game Launcher - GitHub Setup Script
echo ========================================
echo.

echo 请在运行此脚本前，确保你已经：
echo 1. 在 GitHub 上创建了新仓库
echo 2. 复制了仓库的 HTTPS URL
echo.

set /p REPO_URL="请输入 GitHub 仓库 URL (例如: https://github.com/username/game-launcher.git): "
echo.

echo [1/6] 初始化 Git 仓库...
git init
if %errorlevel% neq 0 (
    echo 错误：Git 初始化失败！
    pause
    exit /b 1
)
echo.

echo [2/6] 添加所有文件到暂存区...
git add .
if %errorlevel% neq 0 (
    echo 错误：添加文件失败！
    pause
    exit /b 1
)
echo.

echo [3/6] 创建初始提交...
git commit -m "Initial commit: Game Launcher v1.6.0"
if %errorlevel% neq 0 (
    echo 错误：提交失败！
    pause
    exit /b 1
)
echo.

echo [4/6] 添加远程仓库...
git remote add origin %REPO_URL%
if %errorlevel% neq 0 (
    echo 错误：添加远程仓库失败！
    pause
    exit /b 1
)
echo.

echo [5/6] 重命名主分支为 main...
git branch -M main
if %errorlevel% neq 0 (
    echo 错误：重命名分支失败！
    pause
    exit /b 1
)
echo.

echo [6/6] 推送到 GitHub...
git push -u origin main
if %errorlevel% neq 0 (
    echo.
    echo 错误：推送到 GitHub 失败！
    echo 可能的原因：
    echo 1. 仓库 URL 错误
    echo 2. 需要身份验证（GitHub Personal Access Token）
    echo 3. 网络连接问题
    echo.
    echo 请检查错误信息并重试。
    pause
    exit /b 1
)
echo.

echo ========================================
echo 成功！代码已推送到 GitHub
echo ========================================
echo.
echo 下一步：
echo 1. 访问你的 GitHub 仓库页面
echo 2. 创建一个 Release (v1.6.0)
echo 3. 上传 release 目录中的 ZIP 文件
echo.
echo 按任意键打开 GitHub 仓库页面...
pause >nul

start %REPO_URL%