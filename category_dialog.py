"""
分类管理对话框
用于添加、编辑、删除游戏分类
"""

import tkinter as tk
from tkinter import ttk, messagebox, colorchooser
from typing import Dict, List, Optional, Callable


class CategoryDialog:
    def __init__(self, parent: tk.Tk, categories: List[Dict], games: List[Dict],
                 on_save: Callable[[List[Dict], List[Dict]], None]):
        self.parent = parent
        self.categories = categories
        self.games = games
        self.on_save = on_save
        
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("分类管理")
        self.dialog.geometry("1200x650")
        self.dialog.configure(bg="#f8f9fa")
        self.dialog.transient(parent)
        self.dialog.grab_set()

        # 居中显示
        self.dialog.update_idletasks()
        x = parent.winfo_x() + (parent.winfo_width() - 1200) // 2
        y = parent.winfo_y() + (parent.winfo_height() - 650) // 2
        self.dialog.geometry(f"+{x}+{y}")
        
        self.selected_category = None
        self.selected_games = set()  # 存储选中的游戏名称
        self.create_widgets()
        
    def create_widgets(self):
        """创建界面组件"""
        # 标题
        title_label = tk.Label(
            self.dialog, 
            text="📂 分类管理", 
            font=('Microsoft YaHei', 24, 'bold'),
            bg="#f8f9fa", 
            fg="#4a90e2"
        )
        title_label.pack(pady=15)
        
        # 主框架 - 左右分栏
        main_frame = tk.Frame(self.dialog, bg="#f8f9fa")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 10))
        
        # 左侧 - 分类列表
        left_frame = tk.Frame(main_frame, bg="#f8f9fa")
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))

        tk.Label(
                    left_frame, 
                    text="分类列表", 
                    font=('Microsoft YaHei', 12, 'bold'),
                                bg="#f8f9fa",
                                fg="#2c3e50"                ).pack(anchor=tk.W, pady=(0, 10))
        # 分类按钮 - 横向排列，放在列表上方
        cat_button_frame = tk.Frame(left_frame, bg="#f8f9fa")
        cat_button_frame.pack(fill=tk.X, pady=(0, 10))

        tk.Button(
            cat_button_frame,
            text="➕ 添加",
            command=self.add_category,
            bg="#5cb85c",
            fg="#ffffff",
            font=('Microsoft YaHei', 9, 'bold'),
            padx=12,
            pady=8,
            width=10,
            borderwidth=0,
            relief='flat'
        ).pack(side=tk.LEFT, padx=(0, 5), expand=True, fill=tk.X)

        tk.Button(
            cat_button_frame,
            text="✏️ 编辑",
            command=self.edit_category,
            bg="#4a90e2",
            fg="#ffffff",
            font=('Microsoft YaHei', 9, 'bold'),
            padx=12,
            pady=8,
            width=10,
            borderwidth=0,
            relief='flat'
        ).pack(side=tk.LEFT, padx=(0, 5), expand=True, fill=tk.X)

        tk.Button(
            cat_button_frame,
            text="🗑️ 删除",
            command=self.delete_category,
            bg="#e74c3c",
            fg="#ffffff",
            font=('Microsoft YaHei', 9, 'bold'),
            padx=12,
            pady=8,
            width=10,
            borderwidth=0,
            relief='flat'
        ).pack(side=tk.LEFT, expand=True, fill=tk.X)

        # 分类列表
        columns = ('radio', 'name', 'color', 'count')
        self.category_tree = ttk.Treeview(
            left_frame,
            columns=columns,
            show='headings',
            selectmode='none'
        )

        self.category_tree.heading('radio', text='选择')
        self.category_tree.heading('name', text='分类名称')
        self.category_tree.heading('color', text='颜色')
        self.category_tree.heading('count', text='游戏数量')

        self.category_tree.column('radio', width=50, anchor='center')
        self.category_tree.column('name', width=130)
        self.category_tree.column('color', width=80)
        self.category_tree.column('count', width=60)

        cat_scrollbar = ttk.Scrollbar(left_frame, orient=tk.VERTICAL,
                                      command=self.category_tree.yview)
        self.category_tree.configure(yscrollcommand=cat_scrollbar.set)

        self.category_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        cat_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # 右侧 - 游戏列表
        right_frame = tk.Frame(main_frame, bg="#f8f9fa")
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        tk.Label(
            right_frame,
            text="游戏列表",
            font=('Microsoft YaHei', 12, 'bold'),
            bg="#f8f9fa",
            fg="#2c3e50"
        ).pack(anchor=tk.W, pady=(0, 10))

        # 游戏按钮框架 - 所有按钮都在这里
        game_button_frame = tk.Frame(right_frame, bg="#f8f9fa")
        game_button_frame.pack(fill=tk.X, pady=(0, 10))

        # 第一行：选择按钮
        select_button_frame = tk.Frame(game_button_frame, bg="#f8f9fa")
        select_button_frame.pack(fill=tk.X, pady=(0, 5))

        tk.Button(
            select_button_frame,
            text="📋 全选",
            command=self.select_all_games,
            bg="#f0f0f0",
            fg="#2c3e50",
            font=('Microsoft YaHei', 9, 'bold'),
            padx=12,
            pady=8,
            width=12,
            borderwidth=0,
            relief='flat'
        ).pack(side=tk.LEFT, padx=(0, 5), expand=True, fill=tk.X)

        tk.Button(
            select_button_frame,
            text="❌ 取消选择",
            command=self.deselect_all_games,
            bg="#f0f0f0",
            fg="#2c3e50",
            font=('Microsoft YaHei', 9, 'bold'),
            padx=12,
            pady=8,
            width=12,
            borderwidth=0,
            relief='flat'
        ).pack(side=tk.LEFT, padx=(0, 5), expand=True, fill=tk.X)

        # 第二行：移动按钮
        tk.Button(
            game_button_frame,
            text="➡️ 移动到左侧选中的分类",
            command=self.move_games_to_category,
            bg="#4a90e2",
            fg="#ffffff",
            font=('Microsoft YaHei', 10, 'bold'),
            padx=15,
            pady=10,
            borderwidth=0,
            relief='flat'
        ).pack(fill=tk.X)

        # 游戏列表
        game_columns = ('check', 'name', 'platform', 'current_category')
        self.game_tree = ttk.Treeview(
            right_frame,
            columns=game_columns,
            show='headings',
            selectmode='none'
        )

        self.game_tree.heading('check', text='选择')
        self.game_tree.heading('name', text='游戏名称')
        self.game_tree.heading('platform', text='平台')
        self.game_tree.heading('current_category', text='当前分类')

        self.game_tree.column('check', width=50, anchor='center')
        self.game_tree.column('name', width=180)
        self.game_tree.column('platform', width=70)
        self.game_tree.column('current_category', width=100)

        game_scrollbar = ttk.Scrollbar(right_frame, orient=tk.VERTICAL,
                                       command=self.game_tree.yview)
        self.game_tree.configure(yscrollcommand=game_scrollbar.set)

        self.game_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        game_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)        
        # 加载数据
        self.load_categories()
        self.load_games()
        
        # 绑定点击事件
        self.category_tree.bind('<Button-1>', self.on_category_click)
        self.game_tree.bind('<Button-1>', self.on_game_click)
        
        # 默认选中"全部"分类
        for item in self.category_tree.get_children():
            values = self.category_tree.item(item)['values']
            if values[1] == '全部':
                self.selected_category = '全部'
                self.load_categories()
                break
        
        # 底部按钮
        button_frame = tk.Frame(self.dialog, bg="#f8f9fa")
        button_frame.pack(fill=tk.X, padx=20, pady=(10, 20))
        
        # 保存按钮
        tk.Button(
            button_frame, 
            text="💾 保存", 
            command=self.save_categories,
            bg="#5cb85c", 
            fg="#ffffff",
            font=('Microsoft YaHei', 10, 'bold'),
            padx=20,
            pady=10,
            borderwidth=0,
            relief='flat'
        ).pack(side=tk.RIGHT, padx=(5, 0))
        
        # 取消按钮
        tk.Button(
            button_frame, 
            text="❌ 取消", 
            command=self.dialog.destroy,
            bg="#f0f0f0", 
            fg="#2c3e50",
            font=('Microsoft YaHei', 10, 'bold'),
            padx=20,
            pady=10,
            borderwidth=0,
            relief='flat'
        ).pack(side=tk.RIGHT)
        
    def load_categories(self):
        """加载分类到列表"""
        for item in self.category_tree.get_children():
            self.category_tree.delete(item)
        
        for cat in self.categories:
            # 计算每个分类的游戏数量
            count = 0
            if cat['name'] == '全部':
                count = len(self.games)
            else:
                count = sum(1 for game in self.games if game.get('category', '未分类') == cat['name'])
            
            color_preview = self.create_color_preview(cat['color'])
            # 单选框状态
            radio = '●' if self.selected_category == cat['name'] else '○'
            
            self.category_tree.insert('', tk.END, values=(
                radio,
                cat['name'],
                color_preview,
                count
            ))
    
    def load_games(self):
        """加载所有游戏到列表"""
        for item in self.game_tree.get_children():
            self.game_tree.delete(item)
        
        for game in self.games:
            # 始终显示所有游戏
            display_category = game.get('category', '未分类')
            # 复选框状态
            check = '☑' if game['name'] in self.selected_games else '☐'
            
            self.game_tree.insert('', tk.END, values=(
                check,
                game['name'],
                game['platform'],
                display_category
            ))
    
    def on_category_click(self, event):
        """分类点击事件"""
        # 获取点击的位置
        region = self.category_tree.identify('region', event.x, event.y)
        if region == 'cell':
            # 获取点击的项
            item = self.category_tree.identify_row(event.y)
            if item:
                # 获取点击的列
                column = self.category_tree.identify_column(event.x)
                # 获取分类名称（第二列）
                values = self.category_tree.item(item)['values']
                category_name = values[1]
                
                # 更新选中的分类
                self.selected_category = category_name
                self.load_categories()
    
    def on_game_click(self, event):
        """游戏点击事件"""
        # 获取点击的位置
        region = self.game_tree.identify('region', event.x, event.y)
        if region == 'cell':
            # 获取点击的项
            item = self.game_tree.identify_row(event.y)
            if item:
                # 获取点击的列
                column = self.game_tree.identify_column(event.x)
                # 只有点击第一列（复选框列）时才切换状态
                if column == '#1':
                    # 获取游戏名称（第二列）
                    values = self.game_tree.item(item)['values']
                    game_name = values[1]
                    
                    # 切换选中状态
                    if game_name in self.selected_games:
                        self.selected_games.remove(game_name)
                    else:
                        self.selected_games.add(game_name)
                    
                    # 重新加载游戏列表
                    self.load_games()
    
    def create_color_preview(self, color: str) -> str:
        """创建颜色预览文本"""
        return f"■ {color}"
    
    def add_category(self):
        """添加新分类"""
        self.open_edit_dialog()
    
    def edit_category(self):
        """编辑选中分类"""
        if not self.selected_category:
            messagebox.showwarning("提示", "请先选择一个分类！")
            return
        
        # 找到对应的分类
        for cat in self.categories:
            if cat['name'] == self.selected_category:
                self.open_edit_dialog(cat)
                break
    
    def delete_category(self):
        """删除选中分类"""
        if not self.selected_category:
            messagebox.showwarning("提示", "请先选择一个分类！")
            return
        
        category_name = self.selected_category
        
        # 不允许删除"全部"分类
        if category_name == '全部':
            messagebox.showwarning("提示", "不能删除'全部'分类！")
            return
        
        # 检查是否有游戏使用该分类
        games_in_category = [g for g in self.games if g.get('category', '未分类') == category_name]
        if games_in_category:
            if not messagebox.askyesno("确认删除", 
                f"分类 '{category_name}' 中有 {len(games_in_category)} 个游戏。\n"
                f"删除后这些游戏将变为'未分类'。\n"
                f"确定要删除吗？"):
                return
            # 将游戏分类改为"未分类"
            for game in games_in_category:
                game['category'] = '未分类'
        
        if messagebox.askyesno("确认删除", f"确定要删除分类 '{category_name}' 吗？"):
            self.categories = [cat for cat in self.categories if cat['name'] != category_name]
            self.load_categories()
            messagebox.showinfo("成功", f"分类 '{category_name}' 已删除")
    
    def select_all_games(self):
        """全选游戏"""
        self.selected_games = set(game['name'] for game in self.games)
        self.load_games()
    
    def deselect_all_games(self):
        """取消选择所有游戏"""
        self.selected_games.clear()
        self.load_games()
    
    def move_games_to_category(self):
        """将选中的游戏移动到选中的分类"""
        # 检查是否选择了分类
        if not self.selected_category or self.selected_category == '全部':
            messagebox.showwarning("提示", "请先在左侧选择一个目标分类！")
            return
        
        # 检查是否选择了游戏
        if not self.selected_games:
            messagebox.showwarning("提示", "请先在右侧选择要移动的游戏！")
            return
        
        # 更新游戏分类
        moved_count = 0
        for game in self.games:
            if game['name'] in self.selected_games:
                old_category = game.get('category', '未分类')
                game['category'] = self.selected_category
                moved_count += 1
                print(f"移动游戏 '{game['name']}' 从 '{old_category}' 到 '{self.selected_category}'")
        
        if moved_count > 0:
            self.selected_games.clear()  # 清空选中状态
            self.load_categories()
            self.load_games()
            messagebox.showinfo("成功", f"已将 {moved_count} 个游戏移动到 '{self.selected_category}' 分类")
        else:
            messagebox.showwarning("提示", "没有游戏被移动")
    
    def open_edit_dialog(self, category: Optional[Dict] = None):
        """打开分类编辑对话框"""
        dialog = tk.Toplevel(self.dialog)
        dialog.title("编辑分类" if category else "添加分类")
        dialog.geometry("400x300")
        dialog.configure(bg="#f8f9fa")
        dialog.transient(self.dialog)
        dialog.grab_set()
        
        # 居中显示
        dialog.update_idletasks()
        x = self.dialog.winfo_x() + (self.dialog.winfo_width() - 400) // 2
        y = self.dialog.winfo_y() + (self.dialog.winfo_height() - 300) // 2
        dialog.geometry(f"+{x}+{y}")
        
        form_frame = tk.Frame(dialog, bg="#f8f9fa")
        form_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # 分类名称
        tk.Label(
            form_frame, 
            text="分类名称:", 
            font=('Microsoft YaHei', 10),
            bg="#f8f9fa", 
            fg="#2c3e50"
        ).pack(anchor=tk.W, pady=(0, 5))
        
        name_var = tk.StringVar(value=category['name'] if category else '')
        tk.Entry(
            form_frame, 
            textvariable=name_var, 
            font=('Microsoft YaHei', 10)
        ).pack(fill=tk.X, pady=(0, 15))
        
        # 分类颜色
        tk.Label(
            form_frame, 
            text="分类颜色:", 
            font=('Microsoft YaHei', 10),
            bg="#2c3e50", 
            fg="#ecf0f1"
        ).pack(anchor=tk.W, pady=(0, 5))
        
        color_var = tk.StringVar(value=category['color'] if category else '#3498db')
        color_frame = tk.Frame(form_frame, bg="#f8f9fa")
        color_frame.pack(fill=tk.X, pady=(0, 15))
        
        color_label = tk.Label(
            color_frame, 
            textvariable=color_var, 
            font=('Microsoft YaHei', 10),
            bg=color_var.get(),
            fg="white",
            padx=10,
            pady=5,
            relief=tk.RAISED
        )
        color_label.pack(side=tk.LEFT, padx=(0, 10))
        
        def choose_color():
            color = colorchooser.askcolor(color=color_var.get())[1]
            if color:
                color_var.set(color)
                color_label.config(bg=color, text=color)
        
        tk.Button(
            color_frame, 
            text="选择颜色", 
            command=choose_color,
            bg="#4a90e2", 
            fg="#ffffff",
            font=('Microsoft YaHei', 10, 'bold'),
            borderwidth=0,
            relief='flat'
        ).pack(side=tk.LEFT)
        
        # 更新颜色标签
        def update_color_label(*args):
            color_label.config(bg=color_var.get(), text=color_var.get())
        
        color_var.trace('w', update_color_label)
        
        # 按钮框架
        button_frame = tk.Frame(form_frame, bg="#f8f9fa")
        button_frame.pack(fill=tk.X, pady=(20, 0))
        
        def save():
            name = name_var.get().strip()
            color = color_var.get()
            
            if not name:
                messagebox.showerror("错误", "请输入分类名称！")
                return
            
            # 检查名称是否重复
            for cat in self.categories:
                if cat['name'] == name and cat != category:
                    messagebox.showerror("错误", f"分类名称 '{name}' 已存在！")
                    return
            
            if category:
                # 编辑现有分类
                category['name'] = name
                category['color'] = color
                messagebox.showinfo("成功", f"分类 '{name}' 已更新")
            else:
                # 添加新分类
                self.categories.append({
                    'name': name,
                    'color': color
                })
                messagebox.showinfo("成功", f"分类 '{name}' 已添加")
            
            self.load_categories()
            dialog.destroy()
        
        tk.Button(
            button_frame, 
            text="✅ 保存", 
            command=save,
            bg="#5cb85c", 
            fg="#ffffff",
            font=('Microsoft YaHei', 10, 'bold'),
            padx=15,
            pady=8,
            borderwidth=0,
            relief='flat'
        ).pack(side=tk.LEFT, padx=(0, 10))
        
        tk.Button(
            button_frame, 
            text="❌ 取消", 
            command=dialog.destroy,
            bg="#f0f0f0", 
            fg="#2c3e50",
            font=('Microsoft YaHei', 10, 'bold'),
            padx=15,
            pady=8,
            borderwidth=0,
            relief='flat'
        ).pack(side=tk.LEFT)
    
    def save_categories(self):
        """保存分类和游戏数据"""
        self.on_save(self.categories, self.games)
        messagebox.showinfo("成功", "分类和游戏数据已保存！")
        self.dialog.destroy()