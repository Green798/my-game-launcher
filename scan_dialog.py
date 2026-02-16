"""
扫描对话框模块
用于显示扫描结果和进度
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from typing import List, Dict, Callable, Optional

class ScanDialog:
    """扫描对话框类"""
    
    def __init__(self, parent, existing_games: List[Dict], on_add_selected: Callable):
        """初始化扫描对话框"""
        self.parent = parent
        self.existing_games = existing_games
        self.on_add_selected = on_add_selected
        self.scanned_games: List[Dict] = []
        self.selected_games: List[Dict] = []
        self.custom_directories: List[str] = []
        
        # 创建对话框窗口
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("扫描游戏")
        self.dialog.geometry("800x650")
        self.dialog.configure(bg="#2c3e50")
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        # 居中显示
        self.dialog.update_idletasks()
        x = parent.winfo_x() + (parent.winfo_width() - 800) // 2
        y = parent.winfo_y() + (parent.winfo_height() - 650) // 2
        self.dialog.geometry(f"+{x}+{y}")
        
        # 创建界面
        self.create_widgets()
    
    def create_widgets(self):
        """创建界面组件"""
        # 主框架
        main_frame = tk.Frame(self.dialog, bg="#2c3e50")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # 标题
        title_label = tk.Label(main_frame, text="🔍 扫描游戏", 
                               font=('Microsoft YaHei', 18, 'bold'),
                               bg="#2c3e50", fg="#ecf0f1")
        title_label.pack(pady=(0, 20))
        
        # 扫描选项
        options_frame = tk.LabelFrame(main_frame, text="扫描选项", bg="#2c3e50", fg="#ecf0f1")
        options_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.scan_registry_var = tk.BooleanVar(value=True)
        tk.Checkbutton(options_frame, text="扫描注册表", 
                       variable=self.scan_registry_var,
                       bg="#2c3e50", fg="#ecf0f1", selectcolor="#2c3e50").pack(anchor=tk.W, padx=10, pady=5)
        
        # 自定义目录选择
        dir_frame = tk.Frame(options_frame, bg="#2c3e50")
        dir_frame.pack(fill=tk.X, padx=10, pady=5)
        
        self.scan_custom_var = tk.BooleanVar(value=False)
        tk.Checkbutton(dir_frame, text="扫描自定义目录", 
                       variable=self.scan_custom_var,
                       bg="#2c3e50", fg="#ecf0f1", selectcolor="#2c3e50",
                       command=self.toggle_custom_dir_ui).pack(side=tk.LEFT)
        
        self.custom_dir_button = tk.Button(dir_frame, text="选择目录...", 
                                        command=self.browse_directory,
                                        state=tk.DISABLED, bg="#3498db", fg="#ecf0f1")
        self.custom_dir_button.pack(side=tk.LEFT, padx=(10, 0))
        
        self.custom_dir_label = tk.Label(dir_frame, text="", 
                                      bg="#2c3e50", fg="#bdc3c7")
        self.custom_dir_label.pack(side=tk.LEFT, padx=(10, 0))
        
        # 进度条
        progress_frame = tk.Frame(main_frame, bg="#2c3e50")
        progress_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.progress_var = tk.DoubleVar(value=0)
        self.progress_bar = ttk.Progressbar(progress_frame, variable=self.progress_var,
                                           maximum=100, mode='determinate')
        self.progress_bar.pack(fill=tk.X)
        
        self.status_label = tk.Label(progress_frame, text="准备扫描...",
                                     bg="#2c3e50", fg="#bdc3c7")
        self.status_label.pack(anchor=tk.W, pady=(5, 0))
        
        # 扫描按钮
        button_frame = tk.Frame(main_frame, bg="#2c3e50")
        button_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.scan_button = tk.Button(button_frame, text="开始扫描",
                                     command=self.start_scan, bg="#3498db", fg="#ecf0f1")
        self.scan_button.pack(side=tk.LEFT, padx=(0, 10))
        
        self.stop_button = tk.Button(button_frame, text="停止扫描",
                                     command=self.stop_scan, state=tk.DISABLED, bg="#e74c3c", fg="#ecf0f1")
        self.stop_button.pack(side=tk.LEFT)
        
        # 扫描结果列表
        results_frame = tk.LabelFrame(main_frame, text="扫描结果", bg="#2c3e50", fg="#ecf0f1")
        results_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        # 创建Treeview
        columns = ('select', 'name', 'platform', 'size', 'path')
        self.results_tree = ttk.Treeview(results_frame, columns=columns, show='headings',
                                         selectmode='extended')
        
        self.results_tree.heading('select', text='')
        self.results_tree.heading('name', text='游戏名称')
        self.results_tree.heading('platform', text='平台')
        self.results_tree.heading('size', text='大小')
        self.results_tree.heading('path', text='路径')
        
        self.results_tree.column('select', width=40, anchor='center')
        self.results_tree.column('name', width=250)
        self.results_tree.column('platform', width=100)
        self.results_tree.column('size', width=100)
        self.results_tree.column('path', width=250)
        
        # 滚动条
        scrollbar = ttk.Scrollbar(results_frame, orient=tk.VERTICAL, 
                                   command=self.results_tree.yview)
        self.results_tree.configure(yscrollcommand=scrollbar.set)
        
        self.results_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # 底部按钮
        bottom_frame = tk.Frame(main_frame, bg="#2c3e50")
        bottom_frame.pack(fill=tk.X)
        
        self.add_button = tk.Button(bottom_frame, text="添加选中游戏",
                                     command=self.add_selected_games, state=tk.DISABLED, bg="#27ae60", fg="#ecf0f1")
        self.add_button.pack(side=tk.LEFT, padx=(0, 10))
        
        self.select_all_button = tk.Button(bottom_frame, text="全选",
                                            command=self.select_all, state=tk.DISABLED, bg="#f39c12", fg="#ecf0f1")
        self.select_all_button.pack(side=tk.LEFT, padx=(0, 10))
        
        self.deselect_all_button = tk.Button(bottom_frame, text="取消全选",
                                              command=self.deselect_all, state=tk.DISABLED, bg="#95a5a6", fg="#ecf0f1")
        self.deselect_all_button.pack(side=tk.LEFT, padx=(0, 10))
        
        tk.Button(bottom_frame, text="关闭", command=self.dialog.destroy, bg="#7f8c8d", fg="#ecf0f1").pack(side=tk.RIGHT)
    
    def toggle_custom_dir_ui(self):
        """切换自定义目录UI状态"""
        if self.scan_custom_var.get():
            self.custom_dir_button.config(state=tk.NORMAL)
        else:
            self.custom_dir_button.config(state=tk.DISABLED)
            self.custom_dir_label.config(text="")
            self.custom_directories = []
    
    def browse_directory(self):
        """浏览选择目录"""
        directory = filedialog.askdirectory(title="选择游戏目录")
        if directory:
            self.custom_directories = [directory]
            self.custom_dir_label.config(text=directory)
    
    def start_scan(self):
        """开始扫描"""
        from game_scanner import GameScanner
        
        # 清空结果
        for item in self.results_tree.get_children():
            self.results_tree.delete(item)
        self.scanned_games = []
        
        # 更新按钮状态
        self.scan_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)
        
        # 创建扫描器
        self.scanner = GameScanner(self.existing_games)
        
        # 如果启用了自定义目录，设置自定义目录
        if self.scan_custom_var.get() and self.custom_directories:
            self.scanner.set_custom_directories(self.custom_directories)
        
        self.scanner.set_scan_callback(self.on_game_found)
        self.scanner.set_progress_callback(self.on_progress_update)
        
        # 开始扫描
        self.scanner.start_scan(scan_custom_dirs=self.scan_custom_var.get())
        
        # 定期检查扫描状态
        self.check_scan_complete()
    
    def stop_scan(self):
        """停止扫描"""
        if hasattr(self, 'scanner'):
            self.scanner.is_scanning = False
            self.status_label.config(text="扫描已停止")
            self.scan_button.config(state=tk.NORMAL)
            self.stop_button.config(state=tk.DISABLED)
    
    def check_scan_complete(self):
        """检查扫描是否完成"""
        if hasattr(self, 'scanner') and not self.scanner.is_scanning:
            # 扫描完成
            self.status_label.config(text=f"扫描完成，找到 {len(self.scanned_games)} 个游戏")
            self.scan_button.config(state=tk.NORMAL)
            self.stop_button.config(state=tk.DISABLED)
            
            # 启用按钮
            if self.scanned_games:
                self.add_button.config(state=tk.NORMAL)
                self.select_all_button.config(state=tk.NORMAL)
                self.deselect_all_button.config(state=tk.NORMAL)
        else:
            # 继续检查
            self.dialog.after(100, self.check_scan_complete)
    
    def on_game_found(self, game: Dict):
        """游戏发现回调"""
        self.scanned_games.append(game)
        self.results_tree.insert('', tk.END, values=(
            False,  # 未选中
            game['name'],
            game['platform'],
            game['size'],
            game['directory'] or game['executable']
        ))
    
    def on_progress_update(self, progress: int, message: str):
        """进度更新回调"""
        self.progress_var.set(progress)
        self.status_label.config(text=message)
    
    def select_all(self):
        """全选"""
        for item in self.results_tree.get_children():
            self.results_tree.set(item, 'select', True)
    
    def deselect_all(self):
        """取消全选"""
        for item in self.results_tree.get_children():
            self.results_tree.set(item, 'select', False)
    
    def add_selected_games(self):
        """添加选中的游戏"""
        selected_items = self.results_tree.selection()
        selected_games = []
        
        for item in selected_items:
            values = self.results_tree.item(item)['values']
            if values[0]:  # 已选中
                game_name = values[1]
                for game in self.scanned_games:
                    if game['name'] == game_name:
                        selected_games.append(game)
                        break
        
        if selected_games:
            self.on_add_selected(selected_games)
            messagebox.showinfo("成功", f"已添加 {len(selected_games)} 个游戏")
            self.dialog.destroy()
        else:
            messagebox.showwarning("警告", "请先选择要添加的游戏")