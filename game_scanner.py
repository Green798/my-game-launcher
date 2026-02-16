"""
游戏扫描器模块
用于扫描电脑中的游戏
"""

import os
import winreg
import threading
from typing import List, Dict, Optional

class GameScanner:
    """游戏扫描器类"""
    
    # 游戏识别关键词
    GAME_KEYWORDS = [
        'game', 'game', '游戏', 'steam', 'epic', 'wegame', 
        'origin', 'uplay', 'rockstar', 'ea games', 'ubisoft',
        'bethesda', 'activision', 'blizzard', 'square enix',
        'capcom', 'konami', 'nintendo', 'sony', 'microsoft',
        'wrc', 'fifa', 'nba', 'nfs', 'cod', 'battlefield',
        'assassin', 'gta', 'resident evil', 'monster hunter',
        'elden ring', 'cyberpunk', 'witcher', 'skyrim',
        'minecraft', 'pubg', 'valorant', 'league of legends',
        'overwatch', 'dota', 'cs:go', 'hearthstone', 'world of warcraft'
    ]
    
    # 排除的关键词（非游戏软件）
    EXCLUDE_KEYWORDS = [
        'microsoft visual', 'visual studio', '.net framework',
        'microsoft office', 'adobe', 'nvidia', 'amd', 'intel',
        'java', 'python', 'node', 'google chrome', 'firefox',
        '浏览器', 'driver', '驱动', 'update', '更新',
        'microsoft sql', 'microsoft onedrive', 'microsoft edge',
        'microsoft store', 'windows defender', 'microsoft teams',
        'microsoft outlook', 'microsoft word', 'microsoft excel',
        'microsoft powerpoint', 'microsoft access', 'microsoft visio',
        'microsoft project', 'microsoft sharepoint', 'microsoft dynamics',
        'microsoft azure', 'microsoft 365', 'microsoft security',
        'microsoft management', 'microsoft framework', 'microsoft runtime',
        'microsoft components', 'microsoft tools', 'microsoft sdk',
        'microsoft redistributable', 'microsoft directx', 'microsoft vc',
        'microsoft xml', 'microsoft c++', 'microsoft .net', 'microsoft silverlight',
        'microsoft expression', 'microsoft expression web', 'microsoft expression design',
        'microsoft expression blend', 'microsoft expression studio',
        'microsoft small business', 'microsoft works', 'microsoft picture it',
        'microsoft digital image', 'microsoft photo story', 'microsoft movie maker',
        'microsoft streets', 'microsoft auto route', 'microsoft encarta',
        'microsoft money', 'microsoft home', 'microsoft plus', 'microsoft reader',
        'microsoft xml core', 'microsoft xml parser', 'microsoft xml notepad',
        'microsoft xml paper specification', 'microsoft xml for analysis'
    ]
    
    # 明确的软件发布商（非游戏）
    SOFTWARE_PUBLISHERS = [
        'microsoft corporation', 'microsoft', 'adobe systems', 'oracle',
        'google llc', 'mozilla', 'apple inc', 'autodesk', 'symantec',
        'mcafee', 'kaspersky', 'norton', 'avg', 'avast'
    ]
    
    def __init__(self, existing_games: List[Dict] = None):
        """初始化扫描器"""
        self.existing_games = existing_games or []
        self.scanned_games: List[Dict] = []
        self.scan_callback = None
        self.progress_callback = None
        self.is_scanning = False
        self.custom_directories: List[str] = []
        
    def set_scan_callback(self, callback):
        """设置扫描回调函数"""
        self.scan_callback = callback
        
    def set_progress_callback(self, callback):
        """设置进度回调函数"""
        self.progress_callback = callback
    
    def set_custom_directories(self, directories: List[str]):
        """设置自定义扫描目录"""
        self.custom_directories = directories
        
    def scan_registry(self) -> List[Dict]:
        """扫描Windows注册表中的游戏"""
        games = []
        registry_paths = [
            (winreg.HKEY_LOCAL_MACHINE, r'SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall'),
            (winreg.HKEY_LOCAL_MACHINE, r'SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall'),
            (winreg.HKEY_CURRENT_USER, r'SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall'),
        ]
        
        total_keys = 0
        current_key = 0
        
        # 计算总键数
        for root_key, sub_key in registry_paths:
            try:
                key = winreg.OpenKey(root_key, sub_key)
                total_keys += winreg.QueryInfoKey(key)[0]
                winreg.CloseKey(key)
            except:
                pass
        
        # 扫描注册表
        for root_key, sub_key in registry_paths:
            try:
                key = winreg.OpenKey(root_key, sub_key)
                for i in range(winreg.QueryInfoKey(key)[0]):
                    try:
                        sub_key_name = winreg.EnumKey(key, i)
                        sub_key_path = fr'{sub_key}\{sub_key_name}'
                        
                        if self.progress_callback:
                            current_key += 1
                            progress = int((current_key / total_keys) * 100)
                            self.progress_callback(progress, f'扫描注册表: {sub_key_name}')
                        
                        app_key = winreg.OpenKey(root_key, sub_key_path)
                        
                        try:
                            display_name = winreg.QueryValueEx(app_key, 'DisplayName')[0]
                            publisher = None
                            install_location = None
                            
                            try:
                                publisher = winreg.QueryValueEx(app_key, 'Publisher')[0]
                            except:
                                pass
                            
                            try:
                                install_location = winreg.QueryValueEx(app_key, 'InstallLocation')[0]
                            except:
                                try:
                                    install_location = winreg.QueryValueEx(app_key, 'InstallPath')[0]
                                except:
                                    pass
                            
                            # 检查是否是游戏
                            if self._is_game(display_name, install_location, publisher):
                                game_info = {
                                    'name': display_name,
                                    'platform': self._detect_platform(display_name, install_location),
                                    'executable': self._find_executable(install_location),
                                    'directory': install_location,
                                    'size': self._calculate_size(install_location) if install_location else '未知'
                                }
                                
                                if not self._is_duplicate(game_info):
                                    games.append(game_info)
                                    if self.scan_callback:
                                        self.scan_callback(game_info)
                        
                        finally:
                            winreg.CloseKey(app_key)
                            
                    except Exception as e:
                        continue
                        
                winreg.CloseKey(key)
            except Exception as e:
                continue
                
        return games
    
    def scan_custom_directories(self) -> List[Dict]:
        """扫描自定义目录"""
        games = []
        
        for directory in self.custom_directories:
            if not os.path.exists(directory):
                continue
            
            if self.progress_callback:
                self.progress_callback(50, f'扫描目录: {directory}')
            
            # 扫描目录中的exe文件
            for root, dirs, files in os.walk(directory):
                for file in files:
                    if file.endswith('.exe'):
                        filepath = os.path.join(root, file)
                        
                        # 排除卸载程序和安装程序
                        if 'unins' in file.lower() or 'setup' in file.lower() or 'install' in file.lower():
                            continue
                        
                        # 检查是否是游戏
                        if self._is_game(file, os.path.dirname(filepath), None):
                            game_name = os.path.splitext(file)[0]
                            game_info = {
                                'name': game_name,
                                'platform': self._detect_platform(game_name, os.path.dirname(filepath)),
                                'executable': filepath,
                                'directory': os.path.dirname(filepath),
                                'size': self._calculate_size(os.path.dirname(filepath))
                            }
                            
                            if not self._is_duplicate(game_info):
                                games.append(game_info)
                                if self.scan_callback:
                                    self.scan_callback(game_info)
        
        return games
    
    def _is_game(self, name: str, install_location: str, publisher: str = None) -> bool:
        """判断是否是游戏"""
        if not name:
            return False
            
        name_lower = name.lower()
        
        # 检查发布商
        if publisher:
            publisher_lower = publisher.lower()
            for pub in self.SOFTWARE_PUBLISHERS:
                if pub in publisher_lower:
                    return False
        
        # 检查排除关键词
        for exclude in self.EXCLUDE_KEYWORDS:
            if exclude in name_lower:
                return False
        
        # 检查游戏关键词
        for keyword in self.GAME_KEYWORDS:
            if keyword in name_lower:
                return True
        
        # 检查路径中是否包含常见游戏目录
        if install_location:
            path_lower = install_location.lower()
            if 'game' in path_lower or 'steamapps' in path_lower or 'wegameapps' in path_lower:
                return True
        
        return False
    
    def _detect_platform(self, name: str, install_location: str) -> str:
        """检测游戏平台"""
        name_lower = name.lower()
        location_lower = install_location.lower() if install_location else ''
        
        if 'steam' in name_lower or 'steamapps' in location_lower:
            return 'Steam'
        elif 'epic' in name_lower or 'epicgames' in location_lower:
            return 'Epic Games'
        elif 'wegame' in name_lower or 'wegameapps' in location_lower:
            return 'WeGame'
        elif 'origin' in name_lower:
            return 'Origin'
        elif 'uplay' in name_lower or 'ubisoft' in location_lower:
            return 'Uplay'
        else:
            return '独立游戏'
    
    def _find_executable(self, install_location: str) -> Optional[str]:
        """查找游戏的可执行文件"""
        if not install_location or not os.path.exists(install_location):
            return None
        
        for root, dirs, files in os.walk(install_location):
            for file in files:
                if file.endswith('.exe') and not file.lower().startswith('unins'):
                    if 'unins' not in file.lower() and 'setup' not in file.lower():
                        return os.path.join(root, file)
        
        return None
    
    def _calculate_size(self, directory: str) -> str:
        """计算目录大小"""
        if not directory or not os.path.exists(directory):
            return '未知'
        
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
                return f'{total_size / 1073741824:.2f} GB'
            elif total_size >= 1048576:
                return f'{total_size / 1048576:.2f} MB'
            elif total_size >= 1024:
                return f'{total_size / 1024:.2f} KB'
            else:
                return f'{total_size} Bytes'
        except:
            return '未知'
    
    def _is_duplicate(self, game_info: Dict) -> bool:
        """检查游戏是否已存在"""
        for existing in self.existing_games:
            if existing['name'] == game_info['name']:
                return True
            if game_info['executable'] and existing['executable'] == game_info['executable']:
                return True
        return False
    
    def start_scan(self, scan_custom_dirs: bool = False):
        """开始扫描（在后台线程中）"""
        if self.is_scanning:
            return
        
        self.is_scanning = True
        self.scanned_games = []
        
        def scan_thread():
            try:
                # 先扫描注册表
                games = self.scan_registry()
                
                # 如果启用，再扫描自定义目录
                if scan_custom_dirs and self.custom_directories:
                    custom_games = self.scan_custom_directories()
                    games.extend(custom_games)
                
                self.scanned_games = games
                if self.progress_callback:
                    self.progress_callback(100, '扫描完成')
            finally:
                self.is_scanning = False
        
        thread = threading.Thread(target=scan_thread)
        thread.daemon = True
        thread.start()
    
    def get_scanned_games(self) -> List[Dict]:
        """获取扫描到的游戏"""
        return self.scanned_games