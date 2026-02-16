"""
游戏启动器 - 简单易用的游戏管理工具
支持查看游戏信息、快速启动游戏、添加新游戏
"""

import json
import os
import sys
import subprocess
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from typing import Dict, List, Optional
from game_scanner import GameScanner
from scan_dialog import ScanDialog
from category_dialog import CategoryDialog

class GameLauncher:
    def __init__(self, data_file: str = None):
        if data_file is None:
            script_dir = os.path.dirname(os.path.abspath(__file__))
            data_file = os.path.join(script_dir, "game_library.json")
        
        self.data_file = data_file
        self.games: List[Dict] = []
        self.platforms: List[Dict] = []
        self.categories: List[Dict] = []
        
        print(f"数据文件路径: {self.data_file}")
        print(f"文件是否存在: {os.path.exists(self.data_file)}")
        
        self.load_data()
        
        self.root = tk.Tk()
        self.root.title("游戏启动器")
        self.root.geometry("1200x900")
        self.root.configure(bg="#f8f9fa")
        
        self.setup_styles()
        self.create_widgets()
        
    def setup_styles(self):
        style = ttk.Style()
        available_themes = style.theme_names()
        print(f"可用主题: {available_themes}")
        
        if 'clam' in available_themes:
            style.theme_use('clam')
        elif 'alt' in available_themes:
            style.theme_use('alt')
        else:
            style.theme_use(available_themes[0])
        
        style.configure('Title.TLabel', font=('Microsoft YaHei', 32, 'bold'),
                       background='#f8f9fa', foreground='#4a90e2')
        style.configure('GameList.Treeview', font=('Microsoft YaHei', 10),
                       background='#ffffff', foreground='#2c3e50', fieldbackground='#ffffff',
                       rowheight=30, borderwidth=1, relief='solid')
        style.configure('GameList.Treeview.Heading', font=('Microsoft YaHei', 11, 'bold'),
                       background='#e9ecef', foreground='#4a90e2', relief='flat', borderwidth=0)
        style.map('GameList.Treeview', 
                  background=[('selected', '#4a90e2')],
                  foreground=[('selected', '#ffffff')])
        style.configure('Launch.TButton', font=('Microsoft YaHei', 11, 'bold'),
                       background='#4a90e2', foreground='#ffffff', borderwidth=0, focuscolor='none',
                       relief='flat', padx=15, pady=10)
        style.map('Launch.TButton', 
                  background=[('active', '#357abd'), ('pressed', '#2a5a8f')])
        style.configure('Add.TButton', font=('Microsoft YaHei', 11, 'bold'),
                       background='#5cb85c', foreground='#ffffff', borderwidth=0, focuscolor='none',
                       relief='flat', padx=15, pady=10)
        style.map('Add.TButton', 
                  background=[('active', '#4cae4c'), ('pressed', '#3d8b3d')])
        style.configure('Refresh.TButton', font=('Microsoft YaHei', 10),
                       background='#f0f0f0', foreground='#2c3e50', borderwidth=0, focuscolor='none',
                       relief='flat', padx=12, pady=8)
        style.map('Refresh.TButton', 
                  background=[('active', '#e0e0e0'), ('pressed', '#d0d0d0')])
        style.configure('Platform.TButton', font=('Microsoft YaHei', 10),
                       background='#f0ad4e', foreground='#ffffff', borderwidth=0, focuscolor='none',
                       relief='flat', padx=12, pady=8)
        style.map('Platform.TButton', 
                  background=[('active', '#ec971f'), ('pressed', '#d58512')])
        style.configure('Scan.TButton', font=('Microsoft YaHei', 10),
                       background='#9b59b6', foreground='#ffffff', borderwidth=0, focuscolor='none',
                       relief='flat', padx=12, pady=8)
        style.map('Scan.TButton', 
                  background=[('active', '#8e44ad'), ('pressed', '#7d3c98')])
        style.configure('Info.TLabel', font=('Microsoft YaHei', 10),
                       background='#f8f9fa', foreground='#7f8c8d')
        style.configure('Value.TLabel', font=('Microsoft YaHei', 10, 'bold'),
                       background='#f8f9fa', foreground='#2c3e50')
        style.configure('TLabelframe.Label', font=('Microsoft YaHei', 11, 'bold'),
                       background='#f8f9fa', foreground='#4a90e2')
        style.configure('TLabelframe', background='#f8f9fa', borderwidth=0, relief='flat')
        style.configure('TButton', borderwidth=0, focuscolor='none', relief='flat')
        style.configure('TFrame', background='#f8f9fa')
        style.configure('TLabel', background='#f8f9fa')
        style.configure('TCombobox', fieldbackground='#ffffff', background='#ffffff',
                       foreground='#2c3e50', borderwidth=1, relief='solid',
                       arrowcolor='#4a90e2')
        
    def load_data(self):
        try:
            if not os.path.exists(self.data_file):
                print(f"数据文件不存在，创建初始数据文件 - {self.data_file}")
                # 创建空的初始数据文件
                initial_data = {
                    "games": [],
                    "platforms": [],
                    "categories": [{"name": "全部", "color": "#95a5a6"}],
                    "summary": {
                        "total_games": 0,
                        "total_size": "0.00 MB",
                        "platforms_count": 0,
                        "categories_count": 1
                    }
                }
                with open(self.data_file, 'w', encoding='utf-8') as f:
                    json.dump(initial_data, f, ensure_ascii=False, indent=2)
                self.games = []
                self.platforms = []
                self.categories = [{'name': '全部', 'color': '#95a5a6'}]
                return
            
            with open(self.data_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.games = data.get('games', [])
                self.platforms = data.get('platforms', [])
                self.categories = data.get('categories', [{'name': '全部', 'color': '#95a5a6'}])
            
            print(f"成功加载 {len(self.games)} 个游戏")
            print(f"成功加载 {len(self.platforms)} 个平台")
            print(f"成功加载 {len(self.categories)} 个分类")
        except json.JSONDecodeError as e:
            print(f"JSON解析错误: {e}")
            messagebox.showerror("错误", f"数据文件格式错误:\n{str(e)}")
            self.games = []
            self.platforms = []
            self.categories = [{'name': '全部', 'color': '#95a5a6'}]
        except Exception as e:
            print(f"加载数据时出错: {e}")
            messagebox.showerror("错误", f"加载数据失败:\n{str(e)}")
            self.games = []
            self.platforms = []
            self.categories = [{'name': '全部', 'color': '#95a5a6'}]
    
    def create_widgets(self):
        title_label = ttk.Label(self.root, text="🎮 游戏启动器", style='Title.TLabel')
        title_label.pack(pady=20)
        
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        left_frame = ttk.Frame(main_frame)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        search_frame = ttk.Frame(left_frame)
        search_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(search_frame, text="搜索游戏:", font=('Microsoft YaHei', 10),
                 background='#f8f9fa', foreground='#7f8c8d').pack(side=tk.LEFT, padx=(0, 10))
        
        self.search_var = tk.StringVar()
        self.search_var.trace('w', self.filter_games)
        search_entry = ttk.Entry(search_frame, textvariable=self.search_var, font=('Microsoft YaHei', 10))
        search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # 分类选择器
        category_frame = ttk.Frame(left_frame)
        category_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(category_frame, text="游戏分类:", font=('Microsoft YaHei', 10),
                 background='#2c3e50', foreground='#bdc3c7').pack(side=tk.LEFT, padx=(0, 10))
        
        self.current_category = tk.StringVar(value="全部")
        self.category_var = tk.StringVar()
        self.category_var.trace('w', self.on_category_change)
        self.category_combo = ttk.Combobox(category_frame, textvariable=self.category_var, 
                                          font=('Microsoft YaHei', 10), state='readonly')
        self.category_combo.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        
        # 分类管理按钮
        ttk.Button(category_frame, text="📂 管理分类", 
                  command=self.open_category_dialog).pack(side=tk.LEFT)
        
        columns = ('name', 'category', 'platform', 'size')
        self.game_tree = ttk.Treeview(left_frame, columns=columns, show='headings', style='GameList.Treeview')
        
        self.game_tree.heading('name', text='游戏名称')
        self.game_tree.heading('category', text='分类')
        self.game_tree.heading('platform', text='平台')
        self.game_tree.heading('size', text='大小')
        
        self.game_tree.column('name', width=350, anchor='center')
        self.game_tree.column('category', width=120, anchor='center')
        self.game_tree.column('platform', width=120, anchor='center')
        self.game_tree.column('size', width=100, anchor='center')
        
        scrollbar = ttk.Scrollbar(left_frame, orient=tk.VERTICAL, command=self.game_tree.yview)
        self.game_tree.configure(yscrollcommand=scrollbar.set)
        
        self.game_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.game_tree.bind('<<TreeviewSelect>>', self.on_game_select)
        self.load_games_to_list()

        # 右侧滚动容器
        right_container = ttk.Frame(main_frame, width=380)
        right_container.pack(side=tk.RIGHT, fill=tk.BOTH, padx=(20, 0))

        # 创建Canvas和Scrollbar
        right_canvas = tk.Canvas(right_container, bg="#f8f9fa", highlightthickness=0)
        right_scrollbar = ttk.Scrollbar(right_container, orient=tk.VERTICAL, command=right_canvas.yview)
        right_scrollable_frame = ttk.Frame(right_canvas)

        right_scrollable_frame.bind(
            "<Configure>",
            lambda e: right_canvas.configure(scrollregion=right_canvas.bbox("all"))
        )

        right_canvas.create_window((0, 0), window=right_scrollable_frame, anchor="nw")
        right_canvas.configure(yscrollcommand=right_scrollbar.set)

        right_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        right_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # 鼠标滚轮支持
        def _on_mousewheel(event):
            right_canvas.yview_scroll(int(-1*(event.delta/120)), "units")

        right_canvas.bind_all("<MouseWheel>", _on_mousewheel)

        # 内部框架
        right_frame = ttk.Frame(right_scrollable_frame)
        right_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        info_frame = ttk.LabelFrame(right_frame, text="游戏信息")
        info_frame.pack(fill=tk.X, pady=(0, 10))

        self.info_labels = {}
        info_fields = [('name', '游戏名称:'), ('platform', '平台:'), ('size', '大小:'),
                      ('executable', '启动程序:'), ('directory', '安装目录:')]

        for key, label_text in info_fields:
            frame = ttk.Frame(info_frame)
            frame.pack(fill=tk.X, padx=10, pady=5)
            ttk.Label(frame, text=label_text, style='Info.TLabel').pack(anchor=tk.W)
            self.info_labels[key] = ttk.Label(frame, text='-', style='Value.TLabel', wraplength=300)
            self.info_labels[key].pack(anchor=tk.W)

        button_frame = ttk.Frame(right_frame)
        button_frame.pack(fill=tk.X, pady=(10, 0))

        self.launch_button = ttk.Button(button_frame, text="🚀 启动游戏",
                                       style='Launch.TButton', command=self.launch_game, state=tk.DISABLED)
        self.launch_button.pack(fill=tk.X, pady=5)

        ttk.Button(button_frame, text="➕ 添加游戏", style='Add.TButton',
                  command=self.open_add_game_dialog).pack(fill=tk.X, pady=5)

        ttk.Button(button_frame, text="🔄 刷新数据", style='Refresh.TButton',
                  command=self.refresh_data).pack(fill=tk.X, pady=5)

        # 扫描游戏按钮
        ttk.Button(button_frame, text="🔍 扫描游戏", style='Scan.TButton',
                  command=self.open_scan_dialog).pack(fill=tk.X, pady=5)

        # 编辑和删除按钮
        edit_delete_frame = tk.Frame(button_frame, bg="#f8f9fa")
        edit_delete_frame.pack(fill=tk.X, pady=5)

        self.edit_button = ttk.Button(edit_delete_frame, text="✏️ 编辑游戏",
                                         command=self.edit_game, state=tk.DISABLED)
        self.edit_button.pack(side=tk.LEFT, padx=(0, 5))

        self.delete_button = ttk.Button(edit_delete_frame, text="🗑️ 删除游戏",
                                          command=self.delete_game, state=tk.DISABLED)
        self.delete_button.pack(side=tk.LEFT, padx=(0, 5))

        platform_frame = ttk.LabelFrame(right_frame, text="平台启动器")
        platform_frame.pack(fill=tk.X, pady=(10, 0))

        for platform in self.platforms:
            btn = ttk.Button(platform_frame, text=f"📱 {platform['name']}",
                      style='Platform.TButton', command=lambda p=platform: self.launch_platform(p))
            btn.pack(fill=tk.X, padx=10, pady=5)

        stats_frame = ttk.LabelFrame(right_frame, text="统计信息")
        stats_frame.pack(fill=tk.X, pady=(10, 0))

        total_games = len(self.games)
        total_size = self.calculate_total_size()

        ttk.Label(stats_frame, text=f"总游戏数: {total_games}", style='Info.TLabel').pack(anchor=tk.W, padx=10, pady=5)
        ttk.Label(stats_frame, text=f"总大小: {total_size}", style='Info.TLabel').pack(anchor=tk.W, padx=10, pady=5)
        ttk.Label(stats_frame, text=f"数据文件:", style='Info.TLabel').pack(anchor=tk.W, padx=10, pady=5)
        ttk.Label(stats_frame, text=self.data_file, style='Info.TLabel', wraplength=300).pack(anchor=tk.W, padx=10, pady=(0, 5))
        
        # 打赏按钮
        donate_button = ttk.Button(stats_frame, text="💖 打赏作者", command=self.show_donate_dialog)
        donate_button.pack(fill=tk.X, padx=10, pady=(10, 5))
        
    def load_games_to_list(self):
        # 初始化分类列表
        self.update_category_list()
        # 加载游戏（使用filter_games方法）
        self.filter_games()
    
    def on_game_select(self, event):
        selection = self.game_tree.selection()
        if not selection:
            self.edit_button.config(state=tk.DISABLED)
            self.delete_button.config(state=tk.DISABLED)
            return
        item = self.game_tree.item(selection[0])
        values = item['values']
        for game in self.games:
            if game['name'] == values[0]:
                self.info_labels['name'].config(text=game['name'])
                self.info_labels['platform'].config(text=game['platform'])
                self.info_labels['size'].config(text=game['size'])
                self.info_labels['executable'].config(text=game['executable'])
                self.info_labels['directory'].config(text=game['directory'])
                self.launch_button.config(state=tk.NORMAL)
                self.edit_button.config(state=tk.NORMAL)
                self.delete_button.config(state=tk.NORMAL)
                break
    
    def launch_game(self):
        selection = self.game_tree.selection()
        if not selection:
            return
        item = self.game_tree.item(selection[0])
        values = item['values']
        for game in self.games:
            if game['name'] == values[0]:
                executable = game['executable']
                game_dir = game.get('directory', '')
                if os.path.exists(executable):
                    # 设置工作目录为游戏安装目录，确保游戏能找到数据文件
                    working_dir = game_dir if os.path.exists(game_dir) else os.path.dirname(executable)
                    # 获取启动参数
                    args = game.get('args', '')
                    cmd = [executable]
                    if args:
                        cmd.extend(args.split())
                    subprocess.Popen(cmd, cwd=working_dir)
                    messagebox.showinfo("成功", f"正在启动: {game['name']}")
                else:
                    messagebox.showerror("错误", f"游戏文件不存在:\n{executable}")
                break
    
    def launch_platform(self, platform: Dict):
        if 'executable' in platform and platform['executable']:
            if os.path.exists(platform['executable']):
                subprocess.Popen([platform['executable']])
                messagebox.showinfo("成功", f"正在启动: {platform['name']}")
            else:
                messagebox.showerror("错误", f"平台文件不存在:\n{platform['executable']}")
    
    def update_category_list(self):
        """更新分类列表"""
        category_names = [cat['name'] for cat in self.categories]
        self.category_combo['values'] = category_names
        self.category_var.set(self.current_category.get())
    
    def on_category_change(self, *args):
        """分类改变时筛选游戏"""
        self.current_category.set(self.category_var.get())
        self.filter_games()
    
    def filter_games(self, *args):
        """根据搜索和分类筛选游戏"""
        search_text = self.search_var.get().lower()
        category_name = self.current_category.get()
        
        for item in self.game_tree.get_children():
            self.game_tree.delete(item)
        
        for game in self.games:
            # 检查搜索匹配
            search_match = (search_text in game['name'].lower() or 
                          search_text in game['platform'].lower())
            
            # 检查分类匹配
            category_match = (category_name == '全部' or 
                            game.get('category', '未分类') == category_name)
            
            if search_match and category_match:
                self.game_tree.insert('', tk.END, values=(
                    game['name'],
                    game.get('category', '未分类'),
                    game['platform'], 
                    game['size']
                ))
    
    def open_category_dialog(self):
        """打开分类管理对话框"""
        dialog = CategoryDialog(self.root, self.categories.copy(), self.games.copy(),
                               self.on_categories_saved)
    
    def on_categories_saved(self, updated_categories, updated_games):
        """分类保存回调"""
        self.categories = updated_categories
        self.games = updated_games
        self.update_category_list()
        self.save_data()
        self.filter_games()  # 重新筛选游戏列表
    
    def open_add_game_dialog(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("添加新游戏")
        dialog.geometry("600x450")
        dialog.configure(bg="#f8f9fa")
        dialog.transient(self.root)
        dialog.grab_set()
        
        dialog.update_idletasks()
        x = self.root.winfo_x() + (self.root.winfo_width() - dialog.winfo_width()) // 2
        y = self.root.winfo_y() + (self.root.winfo_height() - dialog.winfo_height()) // 2
        dialog.geometry(f"+{x}+{y}")
        
        form_frame = ttk.Frame(dialog)
        form_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        ttk.Label(form_frame, text="游戏名称:", font=('Microsoft YaHei', 10),
                 background='#f8f9fa', foreground='#2c3e50').pack(anchor=tk.W)
        name_var = tk.StringVar()
        ttk.Entry(form_frame, textvariable=name_var, font=('Microsoft YaHei', 10)).pack(fill=tk.X, pady=(5, 10))
        
        ttk.Label(form_frame, text="游戏平台:", font=('Microsoft YaHei', 10),
                 background='#2c3e50', foreground='#ecf0f1').pack(anchor=tk.W)
        platform_names = [p['name'] for p in self.platforms]
        platform_names.extend(["Steam", "Epic Games", "独立游戏", "其他"])
        platform_var = tk.StringVar(value="独立游戏")
        ttk.Combobox(form_frame, textvariable=platform_var, values=platform_names,
                    font=('Microsoft YaHei', 10)).pack(fill=tk.X, pady=(5, 10))
        
        ttk.Label(form_frame, text="游戏可执行文件 (.exe):", font=('Microsoft YaHei', 10),
                 background='#2c3e50', foreground='#ecf0f1').pack(anchor=tk.W)
        file_frame = ttk.Frame(form_frame)
        file_frame.pack(fill=tk.X, pady=(5, 10))
        
        exe_var = tk.StringVar()
        ttk.Entry(file_frame, textvariable=exe_var, font=('Microsoft YaHei', 10)).pack(side=tk.LEFT, fill=tk.X, expand=True)
        ttk.Button(file_frame, text="浏览...", command=lambda: self.browse_file(exe_var, dialog)).pack(side=tk.LEFT, padx=(5, 0))
        
        ttk.Label(form_frame, text="游戏大小:", font=('Microsoft YaHei', 10),
                 background='#2c3e50', foreground='#ecf0f1').pack(anchor=tk.W)
        size_var = tk.StringVar(value="未选择文件")
        ttk.Label(form_frame, textvariable=size_var, font=('Microsoft YaHei', 10),
                 background='#2c3e50', foreground='#ecf0f1').pack(anchor=tk.W, pady=(5, 10))
        
        ttk.Label(form_frame, text="安装目录:", font=('Microsoft YaHei', 10),
                 background='#2c3e50', foreground='#ecf0f1').pack(anchor=tk.W)
        dir_var = tk.StringVar(value="未选择文件")
        ttk.Label(form_frame, textvariable=dir_var, font=('Microsoft YaHei', 10),
                 background='#2c3e50', foreground='#ecf0f1', wraplength=550).pack(anchor=tk.W, pady=(5, 10))
        
        def on_file_changed(*args):
            exe = exe_var.get()
            if exe and os.path.exists(exe):
                game_dir = os.path.dirname(exe)
                size = self.calculate_directory_size(game_dir)
                size_var.set(size)
                dir_var.set(game_dir)
                if not name_var.get():
                    game_name = os.path.splitext(os.path.basename(exe))[0]
                    name_var.set(game_name)
            else:
                size_var.set("未选择文件")
                dir_var.set("未选择文件")
        
        exe_var.trace('w', on_file_changed)
        
        button_frame = ttk.Frame(form_frame)
        button_frame.pack(fill=tk.X, pady=(20, 0))
        
        def add_game():
            game_name = name_var.get().strip()
            platform = platform_var.get()
            exe = exe_var.get().strip()
            size = size_var.get()
            directory = dir_var.get()
            
            if not game_name:
                messagebox.showerror("错误", "请输入游戏名称！")
                return
            
            if not exe or not os.path.exists(exe):
                messagebox.showerror("错误", "请选择有效的游戏可执行文件！")
                return
            
            new_game = {"name": game_name, "platform": platform, "executable": exe, "size": size, "directory": directory}
            self.games.append(new_game)
            self.save_data()
            self.refresh_data()
            messagebox.showinfo("成功", f"游戏 '{game_name}' 已成功添加！")
            dialog.destroy()
        
        ttk.Button(button_frame, text="✅ 添加", style='Launch.TButton', command=add_game).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(button_frame, text="❌ 取消", style='Refresh.TButton', command=dialog.destroy).pack(side=tk.LEFT)
    
    def browse_file(self, var, parent):
        filename = filedialog.askopenfilename(title="选择游戏可执行文件",
            filetypes=[("可执行文件", "*.exe"), ("所有文件", "*.*")], parent=parent)
        if filename:
            var.set(filename)
    
    def calculate_directory_size(self, directory):
        try:
            total_size = 0
            for dirpath, dirnames, filenames in os.walk(directory):
                for filename in filenames:
                    filepath = os.path.join(dirpath, filename)
                    try:
                        total_size += os.path.getsize(filepath)
                    except:
                        pass
            if total_size >= 1073741824:
                return f"{total_size / 1073741824:.2f} GB"
            elif total_size >= 1048576:
                return f"{total_size / 1048576:.2f} MB"
            elif total_size >= 1024:
                return f"{total_size / 1024:.2f} KB"
            else:
                return f"{total_size} Bytes"
        except:
            return "计算失败"
    
    def save_data(self):
        try:
            data = {"games": self.games, "platforms": self.platforms, "categories": self.categories,
                   "summary": {"total_games": len(self.games), "total_size": self.calculate_total_size(),
                              "platforms_count": len(self.platforms), "categories_count": len(self.categories)}}
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            messagebox.showerror("错误", f"保存失败：{str(e)}")
    
    def refresh_data(self):
        self.game_tree.delete(*self.game_tree.get_children())
        self.load_data()
        self.load_games_to_list()
        for label in self.info_labels.values():
            label.config(text='-')
        self.launch_button.config(state=tk.DISABLED)
    
    def calculate_total_size(self):
        total_mb = 0
        for game in self.games:
            size_str = game['size']
            if 'GB' in size_str:
                total_mb += float(size_str.replace(' GB', '')) * 1024
            elif 'MB' in size_str:
                total_mb += float(size_str.replace(' MB', ''))
        if total_mb >= 1024:
            return f"{total_mb/1024:.2f} GB"
        else:
            return f"{total_mb:.2f} MB"
    

    def edit_game(self):
        selection = self.game_tree.selection()
        if not selection:
            return
        item = self.game_tree.item(selection[0])
        values = item["values"]
        for game in self.games:
            if game["name"] == values[0]:
                self.open_edit_dialog(game)
                break
    
    def delete_game(self):
        selection = self.game_tree.selection()
        if not selection:
            return
        item = self.game_tree.item(selection[0])
        values = item["values"]
        game_name = values[0]
        if messagebox.askyesno("确认删除", "确定要删除游戏 '" + game_name + "' 吗？"):
            self.games = [g for g in self.games if g["name"] != game_name]
            self.save_data()
            self.refresh_data()
            messagebox.showinfo("成功", "游戏 '" + game_name + "' 已删除")
    
    def open_edit_dialog(self, game):
        dialog = tk.Toplevel(self.root)
        dialog.title("编辑游戏")
        dialog.geometry("500x520")
        dialog.configure(bg="#2c3e50")
        dialog.transient(self.root)
        dialog.grab_set()
        dialog.update_idletasks()
        x = self.root.winfo_x() + (self.root.winfo_width() - 500) // 2
        y = self.root.winfo_y() + (self.root.winfo_height() - 520) // 2
        dialog.geometry("+" + str(x) + "+" + str(y))
        form_frame = tk.Frame(dialog, bg="#2c3e50")
        form_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        tk.Label(form_frame, text="游戏名称:", font=("Microsoft YaHei", 10), bg="#2c3e50", fg="#ecf0f1").pack(anchor=tk.W, pady=(0, 5))
        name_var = tk.StringVar(value=game["name"])
        ttk.Entry(form_frame, textvariable=name_var, font=("Microsoft YaHei", 10)).pack(fill=tk.X, pady=(0, 10))
        tk.Label(form_frame, text="游戏平台:", font=("Microsoft YaHei", 10), bg="#2c3e50", fg="#ecf0f1").pack(anchor=tk.W, pady=(0, 5))
        platform_names = ["Steam", "Epic Games", "WeGame", "Origin", "Uplay", "独立游戏", "其他"]
        platform_var = tk.StringVar(value=game["platform"])
        ttk.Combobox(form_frame, textvariable=platform_var, values=platform_names, font=("Microsoft YaHei", 10)).pack(fill=tk.X, pady=(0, 10))
        tk.Label(form_frame, text="游戏分类:", font=("Microsoft YaHei", 10), bg="#2c3e50", fg="#ecf0f1").pack(anchor=tk.W, pady=(0, 5))
        category_names = [cat['name'] for cat in self.categories if cat['name'] != '全部']
        category_var = tk.StringVar(value=game.get('category', '未分类'))
        ttk.Combobox(form_frame, textvariable=category_var, values=category_names, font=("Microsoft YaHei", 10)).pack(fill=tk.X, pady=(0, 10))
        tk.Label(form_frame, text="可执行文件:", font=("Microsoft YaHei", 10), bg="#2c3e50", fg="#ecf0f1").pack(anchor=tk.W, pady=(0, 5))
        exe_var = tk.StringVar(value=game["executable"])
        ttk.Entry(form_frame, textvariable=exe_var, font=("Microsoft YaHei", 10)).pack(fill=tk.X, pady=(0, 5))
        tk.Button(form_frame, text="浏览...", command=lambda: self.browse_file_for_edit(exe_var), bg="#3498db", fg="#ecf0f1").pack(anchor=tk.W, pady=(0, 10))
        tk.Label(form_frame, text="安装目录:", font=("Microsoft YaHei", 10), bg="#2c3e50", fg="#ecf0f1").pack(anchor=tk.W, pady=(0, 5))
        dir_var = tk.StringVar(value=game["directory"])
        ttk.Entry(form_frame, textvariable=dir_var, font=("Microsoft YaHei", 10)).pack(fill=tk.X, pady=(0, 10))
        tk.Label(form_frame, text="游戏大小:", font=("Microsoft YaHei", 10), bg="#2c3e50", fg="#ecf0f1").pack(anchor=tk.W, pady=(0, 5))
        size_var = tk.StringVar(value=game["size"])
        ttk.Entry(form_frame, textvariable=size_var, font=("Microsoft YaHei", 10)).pack(fill=tk.X, pady=(0, 10))
        button_frame = tk.Frame(form_frame, bg="#2c3e50")
        button_frame.pack(fill=tk.X, pady=(20, 0))
        def save_edit():
            new_name = name_var.get().strip()
            new_platform = platform_var.get()
            new_category = category_var.get()
            new_exe = exe_var.get().strip()
            new_directory = dir_var.get().strip()
            new_size = size_var.get().strip()
            if not new_name:
                messagebox.showerror("错误", "游戏名称不能为空！")
                return
            if not new_exe or not os.path.exists(new_exe):
                messagebox.showerror("错误", "可执行文件不存在！")
                return
            game["name"] = new_name
            game["platform"] = new_platform
            game["category"] = new_category
            game["executable"] = new_exe
            game["directory"] = new_directory
            game["size"] = new_size
            self.save_data()
            self.refresh_data()
            messagebox.showinfo("成功", "游戏 '" + new_name + "' 信息已更新")
            dialog.destroy()
        tk.Button(button_frame, text="✅ 保存修改", command=save_edit, bg="#27ae60", fg="#ecf0f1", font=("Microsoft YaHei", 10, "bold"), padx=15, pady=5).pack(side=tk.LEFT, padx=(0, 10))
        tk.Button(button_frame, text="❌ 取消", command=dialog.destroy, bg="#e74c3c", fg="#ecf0f1", font=("Microsoft YaHei", 10), padx=15, pady=5).pack(side=tk.LEFT)
    

    def open_scan_dialog(self):
        """打开扫描对话框"""
        dialog = ScanDialog(self.root, self.games, self.on_scanned_games_added)
    
    def on_scanned_games_added(self, games):
        """处理扫描到的游戏添加"""
        for game in games:
            is_duplicate = False
            for existing in self.games:
                if existing['name'] == game['name']:
                    is_duplicate = True
                    break
            if not is_duplicate:
                self.games.append(game)
        self.save_data()
        self.refresh_data()
        messagebox.showinfo("成功", f"成功添加 {len(games)} 个游戏到游戏库！")

    def browse_file_for_edit(self, var):
        from tkinter import filedialog
        filename = filedialog.askopenfilename(title="选择游戏可执行文件", filetypes=[("可执行文件", "*.exe"), ("所有文件", "*.*")])
        if filename:
            var.set(filename)
    
    def show_donate_dialog(self):
        """显示打赏对话框"""
        dialog = tk.Toplevel(self.root)
        dialog.title("感谢您的支持")
        dialog.geometry("350x280")
        dialog.configure(bg="#f8f9fa")
        dialog.transient(self.root)
        dialog.grab_set()
        
        # 居中显示
        dialog.update_idletasks()
        x = self.root.winfo_x() + (self.root.winfo_width() - 350) // 2
        y = self.root.winfo_y() + (self.root.winfo_height() - 280) // 2
        dialog.geometry(f"+{x}+{y}")
        
        # 标题
        title_label = tk.Label(dialog, text="💖 感谢您的支持", 
                             font=("Microsoft YaHei", 16, "bold"),
                             bg="#f8f9fa", fg="#4a90e2")
        title_label.pack(pady=(15, 10))
        
        # 说明文字
        info_label = tk.Label(dialog, text="如果您觉得这个软件对您有帮助，\n欢迎打赏支持作者继续开发！",
                            font=("Microsoft YaHei", 9),
                            bg="#f8f9fa", fg="#7f8c8d",
                            justify=tk.CENTER)
        info_label.pack(pady=(0, 15))
        
        # 打开图片按钮
        def open_donate_image():
            script_dir = os.path.dirname(os.path.abspath(__file__))
            donate_image_path = os.path.join(script_dir, "感谢打赏.jpg")
            if os.path.exists(donate_image_path):
                try:
                    os.startfile(donate_image_path)
                except Exception as e:
                    messagebox.showerror("错误", f"无法打开图片: {str(e)}")
            else:
                messagebox.showerror("错误", "未找到打赏二维码图片")
        
        open_button = tk.Button(dialog, text="📷 打开微信收款码",
                              font=("Microsoft YaHei", 10, "bold"),
                              bg="#5cb85c", fg="white",
                              activebackground="#4cae4c",
                              activeforeground="white",
                              relief="flat",
                              padx=20, pady=10,
                              command=open_donate_image)
        open_button.pack(pady=(0, 15))
        
        # 感谢文字
        thanks_label = tk.Label(dialog, text="再次感谢您的支持！🙏",
                              font=("Microsoft YaHei", 10, "bold"),
                              bg="#f8f9fa", fg="#5cb85c")
        thanks_label.pack(pady=(0, 15))
        
        # 关闭按钮
        close_button = tk.Button(dialog, text="关闭",
                               font=("Microsoft YaHei", 9),
                               bg="#4a90e2", fg="white",
                               activebackground="#357abd",
                               activeforeground="white",
                               relief="flat",
                               padx=25, pady=6,
                               command=dialog.destroy)
        close_button.pack()

    def run(self):
        try:
            self.root.mainloop()
        except Exception as e:
            print(f"程序运行出错: {e}")
            messagebox.showerror("错误", f"程序运行出错:\n{str(e)}")

if __name__ == "__main__":
    try:
        print("=" * 50)
        print("游戏启动器启动中...")
        print("=" * 50)
        
        data_file = None
        if len(sys.argv) > 1:
            data_file = sys.argv[1]
            print(f"使用指定的数据文件: {data_file}")
        
        launcher = GameLauncher(data_file)
        launcher.run()
    except Exception as e:
        print(f"程序启动失败: {e}")
        messagebox.showerror("错误", f"程序启动失败:\n{str(e)}")