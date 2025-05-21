"""
机器人遥控器
通过HTTP发送C语言命令控制机器人
"""

import requests
import json
import base64
import cmd
import sys

class RobotRemoteControl(cmd.Cmd):
    """机器人遥控器命令行界面"""
    
    prompt = 'robot> '
    intro = '机器人遥控器 (输入help查看命令)'
    
    def __init__(self, host='localhost', port=8080):
        super().__init__()
        self.base_url = f"http://{host}:{port}"
        self.robot_id = 0  # 默认控制第一个机器人
    
    def do_forward(self, arg):
        """前进命令: forward <速度> <距离>"""
        args = arg.split()
        if len(args) != 2:
            print("用法: forward <速度(1-8)> <距离>")
            return
        speed, distance = args
        c_code = f'forward({speed}, {distance});'
        self._send_c_command(c_code)
    
    def do_back(self, arg):
        """后退命令: back <速度> <距离>"""
        args = arg.split()
        if len(args) != 2:
            print("用法: back <速度(1-8)> <距离>")
            return
        speed, distance = args
        c_code = f'back({speed}, {distance});'
        self._send_c_command(c_code)
    
    def do_left(self, arg):
        """左转命令: left <角度>"""
        if not arg:
            print("用法: left <角度>")
            return
        c_code = f'turn_left({arg});'
        self._send_c_command(c_code)
    
    def do_right(self, arg):
        """右转命令: right <角度>"""
        if not arg:
            print("用法: right <角度>")
            return
        c_code = f'turn_right({arg});'
        self._send_c_command(c_code)
    
    def do_say(self, arg):
        """说话命令: say <文本>"""
        if not arg:
            print("用法: say <文本>")
            return
        c_code = f'gpp_say(1, "{arg}");'
        self._send_c_command(c_code)
    
    def do_beep(self, arg):
        """蜂鸣命令: beep <频率> <时长(ms)>"""
        args = arg.split()
        if len(args) != 2:
            print("用法: beep <频率> <时长(ms)>")
            return
        freq, duration = args
        c_code = f'beep({freq}, {duration});'
        self._send_c_command(c_code)
    
    def do_id(self, arg):
        """切换机器人ID: id <机器人编号>"""
        if not arg.isdigit():
            print("用法: id <机器人编号>")
            return
        self.robot_id = int(arg)
        print(f"已切换到机器人 {self.robot_id}")
    
    def do_exec(self, arg):
        """执行C代码: exec <C代码>"""
        if not arg:
            print("用法: exec <C代码>")
            return
        self._send_c_command(arg)
    
    def do_quit(self, arg):
        """退出遥控器"""
        print("再见!")
        return True
    
    def _send_c_command(self, c_code):
        """发送C命令到机器人服务器"""
        try:
            url = f"{self.base_url}/execute_c_program"
            data = {
                "robot_id": self.robot_id,
                "program": c_code
            }
            response = requests.post(url, json=data)
            if response.status_code == 200:
                print("命令执行成功")
            else:
                print(f"命令执行失败: {response.text}")
        except requests.exceptions.RequestException as e:
            print(f"连接服务器失败: {e}")

def main():
    # 解析命令行参数
    host = 'localhost'
    port = 8080
    
    if len(sys.argv) > 1:
        host = sys.argv[1]
        if ':' in host:
            host, port = host.split(':')
            port = int(port)
    
    # 启动遥控器
    remote = RobotRemoteControl(host, port)
    remote.cmdloop()

if __name__ == "__main__":
    main()
