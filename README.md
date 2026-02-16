# 🎮 游戏启动器 (Game Launcher)

一个简单易用的游戏管理工具，帮助你轻松管理和启动电脑中的游戏。

![Version](https://img.shields.io/badge/version-1.6.0-blue.svg)
![Python](https://img.shields.io/badge/python-3.8+-green.svg)
![Platform](https://img.shields.io/badge/platform-Windows-blue.svg)
![License](https://img.shields.io/badge/license-MIT-yellow.svg)

## ✨ 功能特性

### 🎯 核心功能
- ✅ **游戏管理** - 添加、编辑、删除游戏
- ✅ **快速启动** - 一键启动游戏，支持工作目录和启动参数
- ✅ **智能扫描** - 自动扫描注册表和自定义目录中的游戏
- ✅ **分类管理** - 自定义游戏分类，批量管理游戏
- ✅ **搜索筛选** - 快速搜索游戏，按分类筛选
- ✅ **数据持久化** - 自动保存游戏数据到 JSON 文件

### 🎨 界面特性
- 🌈 现代化扁平设计
- 🖼️ 清新明亮的浅色主题
- 📱 响应式布局，支持滚动
- 🎯 统一的视觉风格
- ✨ 流畅的用户体验

### 🔧 技术特性
- 🐍 Python 3.8+ + Tkinter
- 💾 JSON 数据存储
- 🚀 多线程扫描
- 📊 自动计算游戏大小
- 🖥️ 无控制台窗口启动

## 📸 界面预览

### 主界面
- 游戏列表展示（名称、分类、平台、大小）
- 搜索和分类筛选
- 游戏详细信息显示
- 一键启动按钮

### 分类管理
- 自定义分类创建、编辑、删除
- 批量移动游戏到分类
- 颜色选择器
- 智能布局

## 🚀 快速开始

### 下载运行

1. 从 [Releases](https://github.com/你的用户名/game-launcher/releases) 页面下载最新版本
2. 解压到任意目录
3. 双击 `GameLauncher.exe` 运行
4. 开始使用！

### 从源码运行

```bash
# 克隆仓库
git clone https://github.com/你的用户名/game-launcher.git
cd game-launcher

# 安装依赖（本项目主要使用标准库，无需额外依赖）
pip install -r requirements.txt

# 运行程序
python game_launcher.py
```

## 📖 使用说明

### 添加游戏

1. 点击 "➕ 添加游戏" 按钮
2. 选择游戏可执行文件（.exe）
3. 填写游戏信息（自动填充）
4. 点击 "✅ 添加"

### 扫描游戏

1. 点击 "🔍 扫描游戏" 按钮
2. 选择扫描方式：
   - **注册表扫描**：自动扫描系统注册表
   - **自定义目录**：选择特定文件夹扫描
3. 点击 "开始扫描"
4. 查看扫描结果，选择要添加的游戏
5. 点击 "添加选中游戏"

### 分类管理

1. 点击 "📂 管理分类" 按钮
2. 添加新分类：
   - 点击 "添加分类"
   - 输入分类名称
   - 选择分类颜色
3. 移动游戏到分类：
   - 选择目标分类
   - 选择要移动的游戏
   - 点击 "移动到左侧选中的分类"
4. 编辑或删除分类

### 启动游戏

1. 在游戏列表中选择游戏
2. 点击 "🚀 启动游戏" 按钮
3. 游戏将自动启动

## 🔨 开发指南

### 项目结构

```
game-launcher/
├── game_launcher.py       # 主程序
├── game_scanner.py        # 游戏扫描器
├── scan_dialog.py         # 扫描对话框
├── category_dialog.py     # 分类管理对话框
├── game_library.json      # 游戏数据库
├── requirements.txt       # Python 依赖
├── game_launcher.spec     # PyInstaller 配置
├── build.bat             # 打包脚本
└── README.md             # 本文件
```

### 打包发布

详细的打包和发布指南，请参阅 [BUILD_GUIDE.md](BUILD_GUIDE.md)。

快速打包：
```bash
# 运行打包脚本
build.bat

# 或手动打包
pip install pyinstaller
pyinstaller --clean game_launcher.spec
```

## 🛠️ 系统要求

- **操作系统**: Windows 10/11
- **Python**: 3.8+（仅开发需要）
- **内存**: 建议 4GB+
- **磁盘空间**: 50MB+
- **权限**: 部分功能需要管理员权限（注册表扫描）

## 📊 支持的游戏平台

- Steam
- Epic Games
- WeGame
- Origin
- Uplay
- 独立游戏
- 其他平台

## 🤝 贡献指南

欢迎贡献代码、报告问题或提出建议！

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 创建 Pull Request

## 📝 更新日志

### v1.6.0 (2026-02-15) - 用户体验优化版
- 🎯 添加游戏列表分类列，直观显示游戏分类
- 🎯 调整列表列宽，优化空间分配
- 🎯 列表内容居中对齐，视觉更整齐
- 🐛 修复分类管理编辑按钮无作用问题
- 🐛 修复分类管理删除按钮无作用问题

### v1.5.0 (2026-02-15) - 界面优化版
- 🎨 界面全面优化，采用扁平化设计
- 🎨 改为清新明亮的浅色主题
- 🎨 优化配色方案，提升可读性

### v1.4.0 (2026-02-15) - 分类管理版
- 🎉 添加游戏分类管理功能
- 🎉 支持自定义分类创建、编辑、删除
- 🎉 支持批量移动游戏到分类

### v1.3.0 (2026-02-15) - 游戏启动优化版
- 🐛 修复游戏启动工作目录问题
- 🐛 添加启动参数支持功能

### v1.2.0 (2026-02-14) - 功能增强版
- 🎉 添加编辑游戏功能
- 🎉 添加删除游戏功能
- 🎉 添加自动扫描游戏功能

### v1.0.0 (2026-02-14) - 初始版本
- 🎉 初始版本发布

## 📄 许可证

本项目采用 MIT 许可证 - 详见 [LICENSE](LICENSE) 文件。

## 📧 联系方式

- **项目主页**: [GitHub](https://github.com/你的用户名/game-launcher)
- **问题反馈**: [GitHub Issues](https://github.com/你的用户名/game-launcher/issues)
- **Email**: [你的邮箱]

## 🙏 致谢

感谢所有为本项目做出贡献的开发者！

---

**注意**: 本程序仅用于个人学习和娱乐使用，请勿用于商业用途。