@echo off
echo ========================================
echo 游戏启动器 - 打包脚本
echo Game Launcher - Build Script
echo ========================================
echo.
echo.
echo [1/4] 清理旧的构建文件...
if exist "build" (
    rmdir /s /q "build"
    echo 已删除 build 目录
)
if exist "dist" (
    rmdir /s /q "dist"
    echo 已删除 dist 目录
)
echo.
echo.
echo [2/4] 使用 PyInstaller 打包程序...
pyinstaller --clean game_launcher.spec
if %errorlevel% neq 0 (
    echo.
    echo 错误：打包失败！
    pause
    exit /b 1
)
echo.
echo.
echo [3/4] 复制必要的文件到发布目录...
if exist "dist\GameLauncher.exe" (
    echo 正在复制文件到 release 目录...
    if not exist "release" mkdir "release"
    copy "dist\GameLauncher.exe" "release\" >nul
    echo 创建空的game_library.json文件...
    echo {"games": [], "platforms": [], "categories": [{"name": "全部", "color": "#95a5a6"}], "summary": {"total_games": 0, "total_size": "0.00 MB", "platforms_count": 0, "categories_count": 1}} > "release\game_library.json"
    if exist "使用说明.txt" copy "使用说明.txt" "release\" >nul
    if exist "发布说明.txt" copy "发布说明.txt" "release\" >nul
    if exist "感谢打赏.jpg" copy "感谢打赏.jpg" "release\" >nul
    echo 文件复制完成
)
echo.
echo.
echo [4/4] 清理临时文件...
if exist "build" rmdir /s /q "build"
if exist "*.spec" del "*.spec"
echo.
echo.
echo ========================================
echo 打包完成！
echo 可执行文件位置: release\GameLauncher.exe
echo ========================================
echo.
echo.
echo 按任意键退出...
pause >nul