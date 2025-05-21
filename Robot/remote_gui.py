"""
机器人遥控器图形界面
使用PyQt5实现可视化控制
"""

import sys
import argparse
import requests
import json
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                            QHBoxLayout, QPushButton, QLabel, QTextEdit, 
                            QSpinBox, QComboBox, QGroupBox)
from PyQt5.QtCore import Qt, QTimer

class RobotRemoteGUI(QMainWindow):
    def __init__(self, host='localhost', port=8080):
        super().__init__()
        self.base_url = f"http://{host}:{port}"
        self.robot_id = 0
        self.init_ui()
        
    def init_ui(self):
        self.setWindowTitle('机器人遥控器')
        self.setGeometry(100, 100, 600, 500)
        
        # 主控件
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QVBoxLayout()
        main_widget.setLayout(layout)
        
        # 连接状态
        self.status_label = QLabel('状态: 未连接')
        layout.addWidget(self.status_label)
        
        # 机器人选择
        robot_group = QGroupBox('机器人选择')
        robot_layout = QHBoxLayout()
        self.robot_combo = QComboBox()
        self.robot_combo.addItems(['机器人 1', '机器人 2'])
        self.robot_combo.currentIndexChanged.connect(self.change_robot)
        robot_layout.addWidget(QLabel('选择机器人:'))
        robot_layout.addWidget(self.robot_combo)
        robot_group.setLayout(robot_layout)
        layout.addWidget(robot_group)
        
        # 移动控制
        move_group = QGroupBox('移动控制')
        move_layout = QVBoxLayout()
        
        # 速度控制
        speed_layout = QHBoxLayout()
        speed_layout.addWidget(QLabel('速度:'))
        self.speed_spin = QSpinBox()
        self.speed_spin.setRange(1, 8)
        self.speed_spin.setValue(4)
        speed_layout.addWidget(self.speed_spin)
        move_layout.addLayout(speed_layout)
        
        # 方向按钮
        btn_layout = QVBoxLayout()
        
        # 上按钮
        up_layout = QHBoxLayout()
        up_layout.addStretch()
        self.up_btn = QPushButton('↑')
        self.up_btn.setFixedSize(60, 60)
        self.up_btn.clicked.connect(self.move_forward)
        up_layout.addWidget(self.up_btn)
        up_layout.addStretch()
        btn_layout.addLayout(up_layout)
        
        # 左右按钮
        lr_layout = QHBoxLayout()
        self.left_btn = QPushButton('←')
        self.left_btn.setFixedSize(60, 60)
        self.left_btn.clicked.connect(self.turn_left)
        lr_layout.addWidget(self.left_btn)
        
        lr_layout.addStretch()
        
        self.right_btn = QPushButton('→')
        self.right_btn.setFixedSize(60, 60)
        self.right_btn.clicked.connect(self.turn_right)
        lr_layout.addWidget(self.right_btn)
        btn_layout.addLayout(lr_layout)
        
        # 下按钮
        down_layout = QHBoxLayout()
        down_layout.addStretch()
        self.down_btn = QPushButton('↓')
        self.down_btn.setFixedSize(60, 60)
        self.down_btn.clicked.connect(self.move_back)
        down_layout.addWidget(self.down_btn)
        down_layout.addStretch()
        btn_layout.addLayout(down_layout)
        
        move_layout.addLayout(btn_layout)
        move_group.setLayout(move_layout)
        layout.addWidget(move_group)
        
        # 功能控制
        func_group = QGroupBox('功能控制')
        func_layout = QHBoxLayout()
        
        self.beep_btn = QPushButton('蜂鸣')
        self.beep_btn.clicked.connect(self.do_beep)
        func_layout.addWidget(self.beep_btn)
        
        self.say_btn = QPushButton('说话')
        self.say_btn.clicked.connect(self.do_say)
        func_layout.addWidget(self.say_btn)
        
        self.stop_btn = QPushButton('停止')
        self.stop_btn.clicked.connect(self.do_stop)
        func_layout.addWidget(self.stop_btn)
        
        func_group.setLayout(func_layout)
        layout.addWidget(func_group)
        
        # C命令输入
        cmd_group = QGroupBox('C命令输入')
        cmd_layout = QVBoxLayout()
        
        self.cmd_edit = QTextEdit()
        self.cmd_edit.setPlaceholderText('输入C语言命令，例如: forward(4, 10);')
        cmd_layout.addWidget(self.cmd_edit)
        
        exec_layout = QHBoxLayout()
        self.exec_btn = QPushButton('执行')
        self.exec_btn.clicked.connect(self.exec_cmd)
        exec_layout.addWidget(self.exec_btn)
        
        cmd_layout.addLayout(exec_layout)
        cmd_group.setLayout(cmd_layout)
        layout.addWidget(cmd_group)
        
        # 状态更新定时器
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_status)
        self.timer.start(1000)
        
        # 测试连接
        self.update_status()
        
    def change_robot(self, index):
        self.robot_id = index
        
    def _send_c_command(self, c_code):
        """发送C命令到机器人服务器"""
        try:
            url = f"{self.base_url}/execute_c_program"
            data = {
                "robot_id": self.robot_id,
                "program": c_code.strip()
            }
            headers = {
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            }
            
            response = requests.post(
                url,
                json=data,
                headers=headers,
                timeout=3
            )
            
            if response.status_code == 200:
                result = response.json()
                if result.get('status') == 'success':
                    self.status_label.setText('✓ 命令执行成功')
                    self.status_label.setStyleSheet("color: green;")
                else:
                    error_msg = result.get('error', '未知错误')
                    self.status_label.setText(f'✗ 执行失败: {error_msg}')
                    self.status_label.setStyleSheet("color: red;")
            else:
                self.status_label.setText(f'✗ 服务器错误 ({response.status_code})')
                self.status_label.setStyleSheet("color: red;")
                
        except requests.exceptions.RequestException as e:
            self.status_label.setText(f'✗ 连接失败: {str(e)}')
            self.status_label.setStyleSheet("color: red;")
            
    def update_status(self):
        try:
            response = requests.get(f"{self.base_url}/", timeout=1)
            if response.status_code == 200:
                self.status_label.setText('状态: 已连接')
            else:
                self.status_label.setText('状态: 服务器错误')
        except requests.exceptions.RequestException:
            self.status_label.setText('状态: 连接失败')
            
    def move_forward(self):
        speed = self.speed_spin.value()
        c_code = f'forward({speed}, 1);'
        self._send_c_command(c_code)
        
    def move_back(self):
        speed = self.speed_spin.value()
        c_code = f'back({speed}, 1);'
        self._send_c_command(c_code)
        
    def turn_left(self):
        c_code = 'turn_left(90);'
        self._send_c_command(c_code)
        
    def turn_right(self):
        c_code = 'turn_right(90);'
        self._send_c_command(c_code)
        
    def do_beep(self):
        c_code = 'beep(440, 500);'
        self._send_c_command(c_code)
        
    def do_say(self):
        c_code = 'gpp_say(1, "你好，我是机器人");'
        self._send_c_command(c_code)
        
    def do_stop(self):
        c_code = 'forward(0, 0);'
        self._send_c_command(c_code)
        
    def exec_cmd(self):
        cmd = self.cmd_edit.toPlainText()
        if cmd:
            self._send_c_command(cmd)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # 解析命令行参数
    parser = argparse.ArgumentParser(description='机器人遥控器GUI')
    parser.add_argument('address', nargs='?', default='localhost:8080',
                      help='服务器地址，格式: host[:port] (默认: localhost:8080)')
    args = parser.parse_args()

    # 处理地址参数
    if ':' in args.address:
        host, port_str = args.address.split(':')
        try:
            port = int(port_str)
        except ValueError:
            print(f"错误: 端口号必须为整数，使用默认端口8080")
            port = 8080
    else:
        host = args.address
        port = 8080
    
    window = RobotRemoteGUI(host, port)
    window.show()
    sys.exit(app.exec_())
