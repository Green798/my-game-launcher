# 游戏启动器 - 打包发布指南
# Game Launcher - Build & Release Guide

## 📦 打包说明

### 前置要求
- Python 3.8 或更高版本
- Windows 10/11 操作系统
- 管理员权限（部分功能需要注册表访问）

### 快速打包

#### 方法1：使用打包脚本（推荐）
1. 双击运行 `build.bat`
2. 等待打包完成
3. 可执行文件将生成在 `release` 目录中

#### 方法2：手动打包
1. 安装依赖：
   ```bash
   pip install -r requirements.txt
   ```

2. 使用 PyInstaller 打包：
   ```bash
   pyinstaller --clean game_launcher.spec
   ```

3. 手动创建发布目录并复制文件：
   ```bash
   mkdir release
   copy dist\GameLauncher.exe release\
   copy game_library.json release\
   copy VERSION.txt release\
   ```

### 打包输出

打包成功后，`release` 目录将包含以下文件：
- `GameLauncher.exe` - 主程序（约11MB）
- `game_library.json` - 游戏数据库
- `VERSION.txt` - 版本信息

### 分发给其他用户

#### 完整安装包
1. 将 `release` 目录压缩为 ZIP 文件
2. 重命名为 `GameLauncher-v1.6.0.zip`（版本号根据实际情况）
3. 上传到 GitHub Releases 或其他文件分享平台

#### 便携版（推荐）
1. 用户下载 ZIP 文件
2. 解压到任意目录
3. 双击 `GameLauncher.exe` 运行
4. 无需安装 Python 或其他依赖

## 🔧 开发环境搭建

### 安装依赖
```bash
pip install -r requirements.txt
```

### 运行开发版本
```bash
# 使用批处理文件
run.bat

# 或直接运行 Python
python game_launcher.py
```

## 📂 项目结构

```
QD/
├── game_launcher.py       # 主程序
├── game_scanner.py        # 游戏扫描器
├── scan_dialog.py         # 扫描对话框
├── category_dialog.py     # 分类管理对话框
├── game_library.json      # 游戏数据库
├── requirements.txt       # Python 依赖
├── game_launcher.spec     # PyInstaller 配置
├── build.bat             # 打包脚本
├── run.bat               # 运行脚本
├── VERSION.txt           # 版本信息
├── PROJECT_PLAN.txt      # 项目计划
├── PROJECT_PROGRESS.txt  # 项目进度
├── build/                # 打包临时文件（可删除）
├── dist/                 # PyInstaller 输出（可删除）
└── release/              # 最终发布文件
    ├── GameLauncher.exe
    ├── game_library.json
    └── VERSION.txt
```

## 🚀 发布到 GitHub

### 首次发布

1. **创建 GitHub 仓库**
   - 登录 GitHub
   - 点击 "New repository"
   - 仓库名称：`game-launcher`
   - 描述：`简单的游戏启动器 - Game Launcher`
   - 选择 Public（开源）
   - 创建仓库

2. **初始化 Git 仓库**
   ```bash
   cd D:\QD
   git init
   git add .
   git commit -m "Initial commit: Game Launcher v1.6.0"
   ```

3. **连接到 GitHub 仓库**
   ```bash
   git remote add origin https://github.com/你的用户名/game-launcher.git
   git branch -M main
   git push -u origin main
   ```

4. **创建 Release**
   - 在 GitHub 仓库页面，点击 "Releases"
   - 点击 "Create a new release"
   - Tag: `v1.6.0`
   - Release title: `Game Launcher v1.6.0`
   - Description: 复制 VERSION.txt 的内容
   - Attach binaries: 上传 `release` 目录的 ZIP 文件
   - 点击 "Publish release"

### 更新版本

1. 更新 `VERSION.txt` 中的版本号
2. 运行 `build.bat` 重新打包
3. 提交更改：
   ```bash
   git add .
   git commit -m "Release v1.7.0: 新增功能描述"
   git push
   ```
4. 在 GitHub 创建新的 Release

## 📝 许可证选择

建议使用以下开源许可证之一：

- **MIT License**（推荐）：最宽松，允许任何用途
- **Apache 2.0**：包含专利授权
- **GPL v3**：要求衍生作品也开源

创建 `LICENSE` 文件，包含许可证全文。

## 🐛 常见问题

### 打包失败
- 确保已安装 PyInstaller：`pip install pyinstaller`
- 检查 Python 版本是否 >= 3.8
- 以管理员权限运行命令行

### 运行时报错
- 确保所有文件都在同一目录中
- 检查 `game_library.json` 是否存在
- 以管理员权限运行程序（注册表扫描需要）

### 扫描功能不工作
- 需要管理员权限
- 某些游戏可能不会被识别
- 使用自定义目录扫描作为补充

## 📊 版本信息

当前版本：1.6.0
发布日期：2026年2月15日
Python 版本：3.12.1
打包工具：PyInstaller 6.16.0

## 📧 联系方式

如有问题或建议，请通过以下方式联系：
- GitHub Issues
- Email: [你的邮箱]

---

**注意**：本程序仅用于个人学习和娱乐使用，请勿用于商业用途。