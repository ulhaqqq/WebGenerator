#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Python Web框架生成工具 (PyQt5版本)

这个工具用于生成企业级Python Web应用框架，支持多种Web框架和数据库。
使用PyQt5作为GUI库，提供现代的用户界面和良好的跨平台兼容性。
"""

import os
import sys
import json
import shutil
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                             QLabel, QRadioButton, QCheckBox, QLineEdit, QPushButton,
                             QFileDialog, QMessageBox, QButtonGroup, QSpacerItem, QSizePolicy,
                             QProgressBar, QDialog, QTextEdit)
from PyQt5.QtGui import QFont, QColor, QPalette
from PyQt5.QtCore import Qt

# 导入项目生成器模块
from generators.flask_generator import FlaskGenerator
from generators.fastapi_generator import FastAPIGenerator
from utils.config_manager import ConfigManager
from utils.logger import setup_logger

# 设置日志
logger = setup_logger()

# 应用主题颜色 - 现代化配色方案
COLORS = {
    "primary": "#4CAF50",      # 绿色 - 主要按钮
    "secondary": "#2196F3",    # 蓝色 - 次要按钮
    "accent": "#FF9800",       # 橙色 - 强调色
    "purple": "#9C27B0",      # 紫色 - PostgreSQL
    "gray": "#607D8B",        # 灰色 - SQLite
    "background": "#FFFFFF",   # 白色背景
    "card_bg": "#F8F9FA",     # 卡片背景
    "text": "#333333",        # 深灰色文字
    "text_light": "#666666",  # 浅灰色文字
    "border": "#E0E0E0",      # 边框颜色
    "success": "#4CAF50",     # 成功色
    "warning": "#FF9800",     # 警告色
    "error": "#F44336"        # 错误色
}


class CustomConfirmDialog(QDialog):
    """自定义确认对话框"""
    
    def __init__(self, parent=None, title="确认", message="", icon="❓"):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.setFixedSize(380, 160)
        self.setModal(True)
        self.result_value = False
        
        # 设置窗口样式
        self.setStyleSheet(f"""
            QDialog {{
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, 
                    stop:0 #fafafa, stop:1 #f0f0f0);
                border: 1px solid {COLORS['border']};
                border-radius: 12px;
            }}
        """)
        
        # 创建布局
        layout = QVBoxLayout(self)
        layout.setContentsMargins(25, 20, 25, 20)
        layout.setSpacing(15)
        
        # 图标和消息容器
        message_container = QWidget()
        message_layout = QHBoxLayout(message_container)
        message_layout.setContentsMargins(0, 0, 0, 0)
        message_layout.setSpacing(15)
        
        # 图标
        icon_label = QLabel(icon)
        icon_label.setStyleSheet(f"""
            font-size: 32px;
            color: {COLORS['warning']};
            min-width: 40px;
            max-width: 40px;
        """)
        icon_label.setAlignment(Qt.AlignCenter)
        
        # 消息文本
        message_label = QLabel(message)
        message_label.setStyleSheet(f"""
            color: {COLORS['text']};
            font-size: 14px;
            line-height: 1.5;
        """)
        message_label.setWordWrap(True)
        
        message_layout.addWidget(icon_label)
        message_layout.addWidget(message_label, 1)
        layout.addWidget(message_container)
        
        # 按钮容器
        button_container = QWidget()
        button_layout = QHBoxLayout(button_container)
        button_layout.setContentsMargins(0, 0, 0, 0)
        button_layout.setSpacing(10)
        
        # 取消按钮
        cancel_button = QPushButton("取消")
        cancel_button.setStyleSheet(f"""
            QPushButton {{
                background-color: {COLORS['card_bg']};
                color: {COLORS['text']};
                border: 1px solid {COLORS['border']};
                border-radius: 6px;
                padding: 8px 20px;
                font-size: 12px;
                font-weight: 500;
                min-width: 70px;
            }}
            QPushButton:hover {{
                background-color: {COLORS['border']};
                border-color: {COLORS['text_light']};
            }}
            QPushButton:pressed {{
                background-color: #d0d0d0;
            }}
        """)
        cancel_button.clicked.connect(self.reject)
        
        # 确认按钮
        confirm_button = QPushButton("确认")
        confirm_button.setStyleSheet(f"""
            QPushButton {{
                background-color: {COLORS['warning']};
                color: white;
                border: none;
                border-radius: 6px;
                padding: 8px 20px;
                font-size: 12px;
                font-weight: 500;
                min-width: 70px;
            }}
            QPushButton:hover {{
                background-color: #e68900;
            }}
            QPushButton:pressed {{
                background-color: #cc7a00;
            }}
        """)
        confirm_button.clicked.connect(self.accept)
        
        button_layout.addStretch()
        button_layout.addWidget(cancel_button)
        button_layout.addWidget(confirm_button)
        layout.addWidget(button_container)
        
        # 设置默认焦点
        cancel_button.setFocus()
    
    def accept(self):
        self.result_value = True
        super().accept()
    
    def reject(self):
        self.result_value = False
        super().reject()
    
    @staticmethod
    def question(parent, title, message):
        dialog = CustomConfirmDialog(parent, title, message, "⚠️")
        dialog.exec_()
        return dialog.result_value


class ProgressDialog(QDialog):
    """项目生成进度对话框"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("项目生成进度")
        self.setFixedSize(800, 600)
        self.setModal(True)
        
        # 设置窗口样式
        self.setStyleSheet(f"""
            QDialog {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, 
                    stop:0 #11998e, stop:1 #38ef7d);
                border-radius: 10px;
            }}
        """)
        
        # 创建主布局
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(20)
        
        # 创建内容容器
        content_widget = QWidget()
        content_widget.setStyleSheet(f"""
            QWidget {{
                background-color: white;
                border-radius: 12px;
            }}
        """)
        content_layout = QVBoxLayout(content_widget)
        content_layout.setContentsMargins(30, 30, 30, 30)
        content_layout.setSpacing(25)
        
        # 标题
        self.title_label = QLabel("正在生成 FastAPI + PostgreSQL 项目...")
        self.title_label.setStyleSheet(f"""
            color: {COLORS['text']};
            font-size: 20px;
            font-weight: bold;
            text-align: center;
        """)
        self.title_label.setAlignment(Qt.AlignCenter)
        content_layout.addWidget(self.title_label)
        
        # 进度条容器
        progress_container = QWidget()
        progress_layout = QVBoxLayout(progress_container)
        progress_layout.setContentsMargins(0, 0, 0, 0)
        progress_layout.setSpacing(10)
        
        # 进度条
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)
        self.progress_bar.setFixedHeight(25)
        self.progress_bar.setStyleSheet(f"""
            QProgressBar {{
                border: none;
                border-radius: 12px;
                background-color: #e0e0e0;
                text-align: center;
                font-weight: bold;
                color: white;
                font-size: 12px;
            }}
            QProgressBar::chunk {{
                background-color: {COLORS['primary']};
                border-radius: 12px;
            }}
        """)
        progress_layout.addWidget(self.progress_bar)
        content_layout.addWidget(progress_container)
        
        # 主要内容区域
        main_content = QHBoxLayout()
        main_content.setSpacing(30)
        
        # 左侧：生成步骤
        steps_widget = QWidget()
        steps_layout = QVBoxLayout(steps_widget)
        steps_layout.setContentsMargins(0, 0, 0, 0)
        steps_layout.setSpacing(15)
        
        steps_title = QLabel("生成步骤:")
        steps_title.setStyleSheet(f"""
            color: {COLORS['text']};
            font-size: 16px;
            font-weight: bold;
        """)
        steps_layout.addWidget(steps_title)
        
        # 步骤列表（初始为空，将由配置决定）
        self.steps = []
        
        self.step_labels = []
        self.steps_layout = steps_layout  # 保存布局引用以便后续动态添加步骤
        # 步骤将在set_project_info中动态创建
        
        steps_layout.addStretch()
        main_content.addWidget(steps_widget, 1)  # 左侧步骤区域
        
        # 右侧：项目生成结果
        result_widget = QWidget()
        result_widget.setStyleSheet(f"""
            QWidget {{
                background-color: #f8f9fa;
                border-radius: 8px;
                padding: 5px;
            }}
        """)
        result_layout = QVBoxLayout(result_widget)
        result_layout.setContentsMargins(20, 20, 20, 20)
        result_layout.setSpacing(15)
        
        result_title = QLabel("🎉 项目生成结果")
        result_title.setStyleSheet(f"""
            color: {COLORS['text']};
            font-size: 16px;
            font-weight: bold;
        """)
        result_layout.addWidget(result_title)
        
        # 项目信息（包含运行命令）- 占据整个卡片空间
        self.project_info_label = QTextEdit()
        self.project_info_label.setStyleSheet(f"""
            QTextEdit {{
                color: {COLORS['text']};
                font-size: 13px;
                line-height: 1.8;
                background-color: white;
                padding: 20px;
                border-radius: 8px;
                border: none;
            }}
            QTextEdit QScrollBar:vertical {{
                width: 0px;
                background: transparent;
            }}
            QTextEdit QScrollBar:horizontal {{
                height: 0px;
                background: transparent;
            }}
        """)
        self.project_info_label.setReadOnly(True)
        self.project_info_label.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.project_info_label.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        result_layout.addWidget(self.project_info_label, 1)  # 设置拉伸因子为1，占据剩余空间
        
        main_content.addWidget(result_widget, 2)  # 右侧内容区域，拉伸因子为2，比左侧更大
        content_layout.addLayout(main_content)
        
        # 状态栏
        self.status_bar = QLabel("🎯 项目生成完成！正在完成最终操作...")
        self.status_bar.setStyleSheet(f"""
            background-color: #e8f5e8;
            color: #2e7d32;
            padding: 12px 16px;
            border-radius: 6px;
            font-size: 13px;
            font-weight: 500;
        """)
        content_layout.addWidget(self.status_bar)
        
        main_layout.addWidget(content_widget)
        
        # 初始化为空白等待状态
        self._show_waiting_state()
        
        # 详细信息标签（保持兼容性）
        self.detail_label = QLabel("")
        self.status_label = QLabel("准备生成项目...")
    
    def _show_waiting_state(self):
        """显示等待状态"""
        info_text = """⏳ 等待项目生成完成...

正在为您准备:
• 现代化的Web应用框架
• 完整的项目结构
• 开发环境配置
• 运行说明

请耐心等待生成完成"""
        self.project_info_label.setPlainText(info_text)
    
    def _update_step_status(self, step_index, status):
        """更新步骤状态
        Args:
            step_index: 步骤索引
            status: 'pending', 'current', 'completed'
        """
        if 0 <= step_index < len(self.step_labels):
            icon_label, text_label = self.step_labels[step_index]
            
            if status == 'completed':
                icon_label.setText("✓")
                icon_label.setStyleSheet(f"""
                    background-color: {COLORS['primary']};
                    color: white;
                    font-size: 12px;
                    font-weight: bold;
                    border-radius: 10px;
                    text-align: center;
                """)
                text_label.setStyleSheet(f"""
                    color: {COLORS['text']};
                    font-size: 14px;
                """)
            elif status == 'current':
                icon_label.setText("●")
                icon_label.setStyleSheet(f"""
                    background-color: {COLORS['warning']};
                    color: white;
                    font-size: 12px;
                    font-weight: bold;
                    border-radius: 10px;
                    text-align: center;
                """)
                text_label.setStyleSheet(f"""
                    color: {COLORS['text']};
                    font-size: 14px;
                    font-weight: bold;
                """)
            else:  # pending
                icon_label.setText("○")
                icon_label.setStyleSheet(f"""
                    color: #e0e0e0;
                    font-size: 16px;
                    font-weight: bold;
                    border-radius: 10px;
                    text-align: center;
                """)
                text_label.setStyleSheet(f"""
                    color: #999;
                    font-size: 14px;
                """)
    
    def update_progress(self, value, message, sub_step=None, total_sub_steps=None):
        """更新进度条和状态信息
        
        Args:
            value: 主进度值（0-100）
            message: 进度消息
            sub_step: 当前子步骤（可选）
            total_sub_steps: 总子步骤数（可选）
        """
        # 直接使用传入的进度值，因为在 BaseGenerator 中已经计算好了进度百分比
        self.progress_bar.setValue(value)
        
        # 记录当前进度值，用于调试
        import logging
        logging.getLogger('web_generator').debug(f"进度更新: {value}%, 消息: {message}, 子步骤: {sub_step}/{total_sub_steps}")
        
        # 根据进度更新步骤状态
        current_step = int(value / 100 * len(self.steps))
        for i in range(len(self.steps)):
            if i < current_step:
                self._update_step_status(i, 'completed')
            elif i == current_step and value < 100:
                self._update_step_status(i, 'current')
            else:
                self._update_step_status(i, 'pending')
        
        # 更新状态栏
        if value >= 100:
            self.status_bar.setText("🎯 项目生成完成！正在完成最终操作...")
            self.status_bar.setStyleSheet(f"""
                background-color: #fff3cd;
                color: #856404;
                padding: 12px 16px;
                border-radius: 6px;
                font-size: 13px;
                font-weight: 500;
            """)
        else:
            remaining_time = max(1, int((100 - value) * 0.5))  # 估算剩余时间
            self.status_bar.setText(f"正在生成... 预计剩余时间: {remaining_time}秒")
        
        # 保持兼容性
        self.status_label.setText(f"正在生成项目... {int(value)}%")
        self.detail_label.setText(message)
        
        # 确保UI更新
        QApplication.processEvents()
    
    def set_project_info(self, config):
        """设置项目信息，更新标题和项目信息"""
        framework = config["framework"]
        database = config["database"]
        project_name = config["project_name"]
        project_path = config.get("project_path")
        
        framework_name = "Flask" if framework == "flask" else "FastAPI"
        db_name = {
            "mysql": "MySQL",
            "postgresql": "PostgreSQL", 
            "sqlite": "SQLite"
        }.get(database, "PostgreSQL")
        
        # 保存项目信息以便后续使用
        self.project_name = project_name
        self.project_config = config  # 保存完整配置信息
        self.title_label.setText(f"正在生成 {project_name} 项目...")
        
        # 根据框架和配置动态生成步骤列表
        self.steps = [
            "创建项目目录结构",
            f"生成{framework_name}应用文件",
            f"配置{db_name}数据库连接",
            "生成路由和模型" if framework == "flask" else "生成API路由和模型"
        ]
        
        # 根据配置添加可选步骤
        if config.get("tests", False) or config.get("docker", False):
            optional_items = []
            if config.get("tests", False):
                optional_items.append("测试文件")
            if config.get("docker", False):
                optional_items.append("Docker配置")
            self.steps.append(f"创建{' 和 '.join(optional_items)}")
        
        self.steps.append("生成项目文档")
        
        # 清除现有的步骤标签
        for icon_label, text_label in self.step_labels:
            icon_label.deleteLater()
            text_label.deleteLater()
        self.step_labels.clear()
        
        # 动态创建步骤标签
        for i, step in enumerate(self.steps):
            step_container = QWidget()
            step_layout = QHBoxLayout(step_container)
            step_layout.setContentsMargins(0, 0, 0, 0)
            step_layout.setSpacing(10)
            
            # 步骤图标
            icon_label = QLabel("○")
            icon_label.setFixedSize(20, 20)
            icon_label.setStyleSheet(f"""
                color: #e0e0e0;
                font-size: 16px;
                font-weight: bold;
                border-radius: 10px;
                text-align: center;
            """)
            icon_label.setAlignment(Qt.AlignCenter)
            
            # 步骤文本
            text_label = QLabel(step)
            text_label.setStyleSheet(f"""
                color: #999;
                font-size: 14px;
            """)
            
            step_layout.addWidget(icon_label)
            step_layout.addWidget(text_label)
            step_layout.addStretch()
            
            # 在addStretch()之前插入步骤容器
            self.steps_layout.insertWidget(self.steps_layout.count() - 1, step_container)
            self.step_labels.append((icon_label, text_label))
            
            # 设置初始状态
            self._update_step_status(i, 'pending')
        
        # 显示等待状态而不是立即设置项目路径
        self._show_waiting_state()
    
    def update_completion_status(self):
        """更新完成状态的标题"""
        if hasattr(self, 'project_name'):
            self.title_label.setText(f"已生成 {self.project_name} 项目")
        else:
            self.title_label.setText("项目生成完成")
    
    def set_project_path(self, project_path):
        """设置项目路径并更新运行命令"""
        # 更新状态栏为最终完成状态，同时更新标题
        self.status_bar.setText("✅ 项目生成完成！")
        self.status_bar.setStyleSheet(f"""
            background-color: #e8f5e8;
            color: #2e7d32;
            padding: 12px 16px;
            border-radius: 6px;
            font-size: 13px;
            font-weight: 500;
        """)
        
        # 同步更新标题为完成状态
        self.update_completion_status()
        
        # 获取项目配置信息
        config_info = []
        if hasattr(self, 'project_config'):
            config = self.project_config
            framework_name = "Flask" if config["framework"] == "flask" else "FastAPI"
            db_name = {
                "mysql": "MySQL",
                "postgresql": "PostgreSQL", 
                "sqlite": "SQLite"
            }.get(config["database"], "PostgreSQL")
            
            config_info.append(f"框架: {framework_name}")
            config_info.append(f"数据库: {db_name}")
            
            # 添加可选配置
            optional_features = []
            if config.get("redis", False):
                optional_features.append("Redis")
            if config.get("docker", False):
                optional_features.append("Docker")
            if config.get("tests", False):
                optional_features.append("测试框架")
            if config.get("api_docs", False):
                optional_features.append("API文档")
            
            if optional_features:
                config_info.append(f"附加功能: {', '.join(optional_features)}")
        
        # 简化的项目信息显示
        info_text = f"""🎉 项目已成功生成！

📁 项目路径: {project_path}

📋 项目配置:
{chr(10).join(config_info) if config_info else '配置信息已保存'}

🚀 运行命令:
cd {project_path}
pip install -r requirements.txt
python run.py"""
        self.project_info_label.setPlainText(info_text)


class WebGeneratorApp(QMainWindow):
    """Python Web框架生成工具的主应用类 (PyQt5版本)"""
    
    def __init__(self):
        """初始化应用"""
        super().__init__()
        
        self.config_manager = ConfigManager()
        self.config = self.config_manager.get_config()
        
        print("正在初始化PyQt5应用...")
        self.setWindowTitle("Python Web Framework Generator")
        self.setFixedSize(580, 750)
        self.setMinimumSize(550, 700)
        self.setMaximumSize(620, 800)
        
        # 设置窗口在屏幕中央显示
        self.center_window()
        
        # 设置主窗口样式 - 渐变背景
        self.setStyleSheet(f"""
            QMainWindow {{
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #667eea, stop:1 #764ba2);
            }}
        """)
        
        # 创建中央widget
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        
        # 设置中央widget样式
        self.central_widget.setStyleSheet(f"""
            QWidget {{
                background-color: {COLORS['background']};
                border-radius: 12px;
                margin: 15px;
            }}
        """)
        
        # 创建主布局
        self.main_layout = QVBoxLayout(self.central_widget)
        self.main_layout.setContentsMargins(20, 20, 20, 20)
        self.main_layout.setSpacing(12)
        
        # 创建UI
        self._create_ui()
        
        print("PyQt5应用初始化完成")
    
    def center_window(self):
        """将窗口居中显示在屏幕上"""
        from PyQt5.QtWidgets import QDesktopWidget
        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move(
            (screen.width() - size.width()) // 2,
            (screen.height() - size.height()) // 2
        )
    
    def _create_ui(self):
        """创建用户界面"""
        # 标题区域
        title_label = QLabel("🚀 Python Web Framework Generator")
        title_label.setStyleSheet(f"""
            color: {COLORS['text']};
            font-size: 20px;
            font-weight: bold;
            margin: 8px 0;
        """)
        title_label.setAlignment(Qt.AlignCenter)
        self.main_layout.addWidget(title_label)
        
        subtitle_label = QLabel("一键生成企业级Python Web应用框架")
        subtitle_label.setStyleSheet(f"""
            color: {COLORS['text_light']};
            font-size: 13px;
            margin: 0 0 10px 0;
        """)
        subtitle_label.setAlignment(Qt.AlignCenter)
        self.main_layout.addWidget(subtitle_label)
        
        # 添加分隔线
        separator_line = QLabel()
        separator_line.setStyleSheet(f"""
            background-color: {COLORS['border']};
            max-height: 1px;
            margin: 8px 0;
        """)
        self.main_layout.addWidget(separator_line)
        
        # 框架选择
        framework_label = QLabel("🌐 选择Web框架")
        framework_label.setStyleSheet(f"""
            color: {COLORS['text']};
            font-weight: bold;
            font-size: 15px;
            margin: 3px 0;
        """)
        self.main_layout.addWidget(framework_label)
        
        framework_layout = QHBoxLayout()
        framework_layout.setContentsMargins(20, 0, 0, 0)  # 添加左边距创建层级效果
        self.framework_group = QButtonGroup(self)
        
        # Flask 按钮
        self.flask_radio = QRadioButton("🌶️ Flask")
        self.flask_radio.setStyleSheet(f"""
            QRadioButton {{
                color: {COLORS['text']};
                font-size: 12px;
                font-weight: bold;
                spacing: 6px;
                margin: 2px 0;
            }}
            QRadioButton::indicator {{
                width: 14px;
                height: 14px;
                border: 1px solid {COLORS['border']};
                border-radius: 7px;
                background-color: white;
            }}
            QRadioButton::indicator:checked {{
                background-color: {COLORS['primary']};
                border-color: {COLORS['primary']};
            }}
        """)
        
        # FastAPI 按钮
        self.fastapi_radio = QRadioButton("⚡ FastAPI")
        self.fastapi_radio.setStyleSheet(f"""
            QRadioButton {{
                color: {COLORS['text']};
                font-size: 12px;
                font-weight: bold;
                spacing: 6px;
                margin: 2px 0;
            }}
            QRadioButton::indicator {{
                width: 14px;
                height: 14px;
                border: 1px solid {COLORS['border']};
                border-radius: 7px;
                background-color: white;
            }}
            QRadioButton::indicator:checked {{
                background-color: {COLORS['secondary']};
                border-color: {COLORS['secondary']};
            }}
        """)
        
        if self.config["framework"] == "flask":
            self.flask_radio.setChecked(True)
        else:
            self.fastapi_radio.setChecked(True)
        
        self.framework_group.addButton(self.flask_radio)
        self.framework_group.addButton(self.fastapi_radio)
        
        framework_layout.addWidget(self.flask_radio)
        framework_layout.addWidget(self.fastapi_radio)
        framework_layout.addStretch()
        
        self.main_layout.addLayout(framework_layout)
        self.main_layout.addSpacing(6)
        
        # 数据库选择
        db_label = QLabel("🗄️ 选择数据库")
        db_label.setStyleSheet(f"""
            color: {COLORS['text']};
            font-weight: bold;
            font-size: 15px;
            margin: 3px 0;
        """)
        self.main_layout.addWidget(db_label)
        
        db_layout = QHBoxLayout()
        db_layout.setContentsMargins(20, 0, 0, 0)  # 添加左边距创建层级效果
        self.db_group = QButtonGroup(self)
        
        # MySQL 按钮
        self.mysql_radio = QRadioButton("🐬 MySQL")
        self.mysql_radio.setStyleSheet(f"""
            QRadioButton {{
                color: {COLORS['text']};
                font-size: 12px;
                font-weight: bold;
                spacing: 6px;
                margin: 2px 0;
            }}
            QRadioButton::indicator {{
                width: 14px;
                height: 14px;
                border: 1px solid {COLORS['border']};
                border-radius: 7px;
                background-color: white;
            }}
            QRadioButton::indicator:checked {{
                background-color: {COLORS['accent']};
                border-color: {COLORS['accent']};
            }}
        """)
        
        # PostgreSQL 按钮
        self.postgres_radio = QRadioButton("🐘 PostgreSQL")
        self.postgres_radio.setStyleSheet(f"""
            QRadioButton {{
                color: {COLORS['text']};
                font-size: 12px;
                font-weight: bold;
                spacing: 6px;
                margin: 2px 0;
            }}
            QRadioButton::indicator {{
                width: 14px;
                height: 14px;
                border: 1px solid {COLORS['border']};
                border-radius: 7px;
                background-color: white;
            }}
            QRadioButton::indicator:checked {{
                background-color: {COLORS['purple']};
                border-color: {COLORS['purple']};
            }}
        """)
        
        # SQLite 按钮
        self.sqlite_radio = QRadioButton("💾 SQLite")
        self.sqlite_radio.setStyleSheet(f"""
            QRadioButton {{
                color: {COLORS['text']};
                font-size: 12px;
                font-weight: bold;
                spacing: 6px;
                margin: 2px 0;
            }}
            QRadioButton::indicator {{
                width: 14px;
                height: 14px;
                border: 1px solid {COLORS['border']};
                border-radius: 7px;
                background-color: white;
            }}
            QRadioButton::indicator:checked {{
                background-color: {COLORS['gray']};
                border-color: {COLORS['gray']};
            }}
        """)
        
        if self.config["database"] == "mysql":
            self.mysql_radio.setChecked(True)
        elif self.config["database"] == "sqlite":
            self.sqlite_radio.setChecked(True)
        else:
            self.postgres_radio.setChecked(True)
        
        self.db_group.addButton(self.mysql_radio)
        self.db_group.addButton(self.postgres_radio)
        self.db_group.addButton(self.sqlite_radio)
        
        db_layout.addWidget(self.mysql_radio)
        db_layout.addWidget(self.postgres_radio)
        db_layout.addWidget(self.sqlite_radio)
        db_layout.addStretch()
        
        self.main_layout.addLayout(db_layout)
        self.main_layout.addSpacing(6)
        
        # Redis选项
        redis_layout = QHBoxLayout()
        redis_layout.setContentsMargins(20, 0, 0, 0)  # 添加左边距创建层级效果
        
        self.redis_checkbox = QCheckBox("⚡ 启用Redis缓存")
        self.redis_checkbox.setChecked(self.config["redis"])
        self.redis_checkbox.setStyleSheet(f"""
            QCheckBox {{
                color: {COLORS['text']};
                font-size: 12px;
                font-weight: bold;
                spacing: 6px;
                margin: 2px 0;
            }}
            QCheckBox::indicator {{
                width: 14px;
                height: 14px;
                border: 1px solid {COLORS['border']};
                border-radius: 3px;
                background-color: white;
            }}
            QCheckBox::indicator:checked {{
                background-color: {COLORS['error']};
                border-color: {COLORS['error']};
            }}
        """)
        
        redis_layout.addWidget(self.redis_checkbox)
        redis_layout.addStretch()
        self.main_layout.addLayout(redis_layout)
        self.main_layout.addSpacing(8)
        
        # 创建项目标题
        create_title = QLabel("🚀 创建项目")
        create_title.setStyleSheet(f"""
            color: {COLORS['text']};
            font-weight: bold;
            font-size: 15px;
            margin: 3px 0;
        """)
        self.main_layout.addWidget(create_title)
        self.main_layout.addSpacing(3)
        
        # 项目配置区域 - 简洁设计
        config_widget = QWidget()
        config_widget.setStyleSheet(f"""
            QWidget {{
                background-color: transparent;
                border: none;
                margin: 0px;
            }}
        """)
        config_layout = QVBoxLayout(config_widget)
        config_layout.setContentsMargins(20, 15, 20, 15)
        config_layout.setSpacing(12)
        
        # 项目名称行
        name_container = QWidget()
        name_container_layout = QVBoxLayout(name_container)
        name_container_layout.setContentsMargins(0, 0, 0, 0)
        name_container_layout.setSpacing(6)
        
        name_label = QLabel("项目名称")
        name_label.setStyleSheet(f"""
            color: {COLORS['text']};
            font-size: 13px;
            font-weight: 600;
            margin-bottom: 2px;
        """)
        
        self.project_name_input = QLineEdit()
        self.project_name_input.setText(self.config["project_name"])
        self.project_name_input.setPlaceholderText("输入项目名称")
        self.project_name_input.setStyleSheet(f"""
            QLineEdit {{
                padding: 12px 8px;
                border: none;
                border-bottom: 1px solid {COLORS['border']};
                border-radius: 0px;
                background-color: transparent;
                color: {COLORS['text']};
                font-size: 13px;
                min-height: 16px;
            }}
            QLineEdit:focus {{
                border-bottom: 2px solid {COLORS['primary']};
                background-color: transparent;
            }}
            QLineEdit:hover {{
                border-bottom: 1px solid {COLORS['text_light']};
            }}
        """)
        
        name_container_layout.addWidget(name_label)
        name_container_layout.addWidget(self.project_name_input)
        config_layout.addWidget(name_container)
        
        # 项目路径行
        path_container = QWidget()
        path_container_layout = QVBoxLayout(path_container)
        path_container_layout.setContentsMargins(0, 0, 0, 0)
        path_container_layout.setSpacing(6)
        
        path_label = QLabel("项目路径")
        path_label.setStyleSheet(f"""
            color: {COLORS['text']};
            font-size: 13px;
            font-weight: 600;
            margin-bottom: 2px;
        """)
        
        # 项目路径输入框和浏览按钮容器
        path_input_container = QWidget()
        path_input_layout = QHBoxLayout(path_input_container)
        path_input_layout.setContentsMargins(0, 0, 0, 0)
        path_input_layout.setSpacing(8)
        
        self.project_path_input = QLineEdit()
        self.project_path_input.setText(self.config["project_path"])
        self.project_path_input.setPlaceholderText("选择项目保存路径")
        self.project_path_input.setStyleSheet(f"""
            QLineEdit {{
                padding: 12px 8px;
                border: none;
                border-bottom: 1px solid {COLORS['border']};
                border-radius: 0px;
                background-color: transparent;
                color: {COLORS['text']};
                font-size: 13px;
                min-height: 16px;
            }}
            QLineEdit:focus {{
                border-bottom: 2px solid {COLORS['primary']};
                background-color: transparent;
            }}
            QLineEdit:hover {{
                border-bottom: 1px solid {COLORS['text_light']};
            }}
        """)
        
        browse_button = QPushButton("📁 浏览")
        browse_button.clicked.connect(self._browse_path)
        browse_button.setStyleSheet(f"""
            QPushButton {{
                background-color: transparent;
                color: {COLORS['secondary']};
                border: 1px solid {COLORS['secondary']};
                padding: 10px 16px;
                border-radius: 4px;
                font-weight: 500;
                font-size: 12px;
                min-width: 80px;
            }}
            QPushButton:hover {{
                background-color: {COLORS['secondary']};
                color: white;
            }}
            QPushButton:pressed {{
                background-color: #1565C0;
                color: white;
            }}
        """)
        
        path_input_layout.addWidget(self.project_path_input, 1)
        path_input_layout.addWidget(browse_button, 0)
        
        path_container_layout.addWidget(path_label)
        path_container_layout.addWidget(path_input_container)
        config_layout.addWidget(path_container)
        
        # 将配置区域添加到主布局
        self.main_layout.addWidget(config_widget)
        self.main_layout.addSpacing(10)
        
        # 高级选项
        advanced_label = QLabel("🔧 高级选项")
        advanced_label.setStyleSheet(f"""
            color: {COLORS['text']};
            font-weight: bold;
            font-size: 15px;
            margin: 5px 0;
        """)
        self.main_layout.addWidget(advanced_label)
        
        # 高级选项水平布局
        advanced_layout = QHBoxLayout()
        advanced_layout.setContentsMargins(20, 0, 0, 0)  # 添加左边距创建层级效果
        advanced_layout.setSpacing(20)
        
        # Docker支持
        self.docker_checkbox = QCheckBox("🐳 Docker支持")
        self.docker_checkbox.setChecked(self.config["docker"])
        self.docker_checkbox.setStyleSheet(f"""
            QCheckBox {{
                color: {COLORS['text']};
                font-size: 12px;
                font-weight: bold;
                spacing: 6px;
                margin: 2px 0;
            }}
            QCheckBox::indicator {{
                width: 14px;
                height: 14px;
                border: 1px solid {COLORS['border']};
                border-radius: 3px;
                background-color: white;
            }}
            QCheckBox::indicator:checked {{
                background-color: {COLORS['secondary']};
                border-color: {COLORS['secondary']};
            }}
        """)
        
        # 测试文件
        self.testing_checkbox = QCheckBox("🧪 测试框架")
        self.testing_checkbox.setChecked(self.config["testing"])
        self.testing_checkbox.setStyleSheet(f"""
            QCheckBox {{
                color: {COLORS['text']};
                font-size: 12px;
                font-weight: bold;
                spacing: 6px;
                margin: 2px 0;
            }}
            QCheckBox::indicator {{
                width: 14px;
                height: 14px;
                border: 1px solid {COLORS['border']};
                border-radius: 3px;
                background-color: white;
            }}
            QCheckBox::indicator:checked {{
                background-color: {COLORS['accent']};
                border-color: {COLORS['accent']};
            }}
        """)
        
        # API文档
        self.api_docs_checkbox = QCheckBox("📚 API文档")
        self.api_docs_checkbox.setChecked(self.config["api_docs"])
        self.api_docs_checkbox.setStyleSheet(f"""
            QCheckBox {{
                color: {COLORS['text']};
                font-size: 12px;
                font-weight: bold;
                spacing: 6px;
                margin: 2px 0;
            }}
            QCheckBox::indicator {{
                width: 14px;
                height: 14px;
                border: 1px solid {COLORS['border']};
                border-radius: 3px;
                background-color: white;
            }}
            QCheckBox::indicator:checked {{
                background-color: {COLORS['purple']};
                border-color: {COLORS['purple']};
            }}
        """)
        
        advanced_layout.addWidget(self.docker_checkbox)
        advanced_layout.addWidget(self.testing_checkbox)
        advanced_layout.addWidget(self.api_docs_checkbox)
        advanced_layout.addStretch()
        
        self.main_layout.addLayout(advanced_layout)
        self.main_layout.addSpacing(20)
        
        # 按钮
        buttons_layout = QHBoxLayout()
        
        generate_button = QPushButton("🚀 生成项目")
        generate_button.setMinimumSize(120, 32)
        generate_button.setStyleSheet(f"""
            QPushButton {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 {COLORS['primary']}, stop:1 {COLORS['secondary']});
                color: white;
                border: none;
                padding: 6px 12px;
                border-radius: 6px;
                font-weight: bold;
                font-size: 12px;
                margin: 2px;
                max-height: 32px;
            }}
            QPushButton:hover {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 {COLORS['secondary']}, stop:1 {COLORS['primary']});
            }}
            QPushButton:pressed {{
                background: {COLORS['primary']};
            }}
        """)
        generate_button.clicked.connect(self._generate_project)
        
        exit_button = QPushButton("退出")
        exit_button.setMinimumSize(120, 32)
        exit_button.setStyleSheet(f"""
            QPushButton {{
                background-color: #E0E0E0;
                color: {COLORS['text']};
                border: none;
                padding: 6px 12px;
                border-radius: 6px;
                font-weight: bold;
                font-size: 12px;
                margin: 2px;
                max-height: 32px;
            }}
            QPushButton:hover {{
                background-color: #D0D0D0;
            }}
        """)
        exit_button.clicked.connect(self.close)
        
        buttons_layout.addStretch()
        buttons_layout.addWidget(generate_button)
        buttons_layout.addSpacing(10)
        buttons_layout.addWidget(exit_button)
        
        self.main_layout.addLayout(buttons_layout)
        
        # 版权信息
        copyright_label = QLabel("© 2025 Python Web框架生成器 - 由zlynn制作")
        copyright_label.setStyleSheet(f"""
            color: {COLORS['text_light']};
            font-size: 10px;
            margin: 10px 0 5px 0;
            text-align: center;
        """)
        copyright_label.setAlignment(Qt.AlignCenter)
        self.main_layout.addWidget(copyright_label)
        
        self.main_layout.addStretch()
    
    def _browse_path(self):
        """打开文件对话框选择项目路径"""
        path = QFileDialog.getExistingDirectory(self, "选择项目路径", self.project_path_input.text())
        if path:
            self.project_path_input.setText(path)
    
    def _get_project_config(self):
        """获取项目配置"""
        # 确定数据库类型
        if self.mysql_radio.isChecked():
            database = "mysql"
        elif self.sqlite_radio.isChecked():
            database = "sqlite"
        else:
            database = "postgresql"
        
        return {
            "project_name": self.project_name_input.text(),
            "project_path": self.project_path_input.text(),
            "framework": "flask" if self.flask_radio.isChecked() else "fastapi",
            "database": database,
            "redis": self.redis_checkbox.isChecked(),
            "docker": self.docker_checkbox.isChecked(),
            "tests": self.testing_checkbox.isChecked(),
            "api_docs": self.api_docs_checkbox.isChecked(),
            "auth": False
        }
    
    def _generate_project(self):
        """生成项目"""
        config = self._get_project_config()
        
        # 验证输入
        if not config["project_name"] or not config["project_path"]:
            QMessageBox.critical(self, "错误", "项目名称和路径不能为空")
            return
        
        # 检查项目路径是否存在
        if not os.path.exists(config["project_path"]):
            try:
                os.makedirs(config["project_path"])
            except Exception as e:
                QMessageBox.critical(self, "错误", f"无法创建项目路径: {str(e)}")
                return
        
        # 完整项目路径
        full_path = os.path.join(config["project_path"], config["project_name"])
        
        # 检查项目是否已存在
        if os.path.exists(full_path):
            reply = CustomConfirmDialog.question(self, "警告",
                                                f"项目 {config['project_name']} 已存在于 {config['project_path']} 中。\n是否覆盖?")
            
            if reply:
                try:
                    shutil.rmtree(full_path)
                    self._create_project(config, full_path)
                except Exception as e:
                    QMessageBox.critical(self, "错误", f"无法删除现有项目: {str(e)}")
            return
        
        # 直接生成项目
        self._create_project(config, full_path)
    
    def _create_project(self, config, full_path):
        """创建项目"""
        # 创建进度对话框
        progress_dialog = ProgressDialog(self)
        # 设置项目信息
        progress_dialog.set_project_info(config)
        progress_dialog.show()
        
        try:
            # 打印配置信息以便调试
            print("\n项目配置信息:")
            import json
            print(json.dumps(config, indent=4, ensure_ascii=False))
            print("\n")
            
            # 进度回调函数
            def progress_callback(value, message, sub_step=None, total_sub_steps=None):
                progress_dialog.update_progress(value, message, sub_step, total_sub_steps)
            
            # 选择合适的生成器
            if config["framework"] == "flask":
                generator = FlaskGenerator(config, progress_callback=progress_callback)
            else:  # fastapi
                generator = FastAPIGenerator(config, progress_callback=progress_callback)
            
            # 生成项目
            generator.generate()
            
            # 保存配置以供将来使用
            self.config_manager.save_config(config)
            
            # 添加短暂延迟，确保所有后端操作完成
            import time
            time.sleep(1)
            
            # 更新进度对话框显示项目生成结果（只有在项目真正完成后才调用）
            progress_dialog.set_project_path(full_path)
            
            # 不自动关闭进度对话框，让用户查看结果并手动关闭
            
        except Exception as e:
            # 关闭进度对话框
            progress_dialog.close()
            
            logger.exception("项目生成失败")
            QMessageBox.critical(self, "错误", f"项目生成失败: {str(e)}")


def main():
    """主函数"""
    try:
        print("正在启动Python Web框架生成器 (PyQt5版本)...")
        
        # 创建应用实例
        app = QApplication(sys.argv)
        
        # 设置应用样式
        app.setStyle("Fusion")
        
        # 创建主窗口
        window = WebGeneratorApp()
        window.show()
        
        print("应用初始化完成，开始运行...")
        
        # 运行应用
        sys.exit(app.exec_())
    except Exception as e:
        print(f"应用运行出错: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()