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
    intro = '''机器人遥控器 (输入help查看命令)
    
示例命令:
  forward 4 5    - 以速度4前进5单位
  left 90        - 左转90度
  say "你好"     - 机器人说话
  beep 440 1000  - 发出440Hz蜂鸣1秒
  exec "square"  - 执行画正方形示例
  exec "circle"  - 执行画圆形示例
  exec "poem"    - 朗诵诗歌
  
输入 quit 退出
'''
    
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
        """执行C代码: exec <C代码>
        示例:
        exec "forward(4, 5); turn_left(90);"
        exec "for(int i=0;i<4;i++){forward(4,2);turn_right(90);}"
        """
        if not arg:
            print("用法: exec <C代码>")
            print("示例命令:")
            print("  square - 画正方形")
            print("  circle - 画圆形路径")
            print("  poem - 朗诵诗歌")
            return
            
        # 预定义示例命令
        if arg == "square":
            c_code = """
            for(int i=0; i<4; i++) {
                forward(4, 3);
                turn_right(90);
            }
            """
        elif arg == "circle":
            c_code = """
            for(int i=0; i<36; i++) {
                forward(2, 1);
                turn_right(10);
            }
            """
        elif arg == "poem":
            c_code = """
            gpp_say(1, "静夜思");
            gpp_say(1, "作者李白");
            gpp_say(1, "床前明月光，疑是地上霜。举头望明月，低头思故乡。");
            """
        else:
            c_code = arg
            
        self._send_c_command(c_code)
    
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
                return True
            else:
                print(f"命令执行失败: {response.text}")
                return False
        except requests.exceptions.RequestException as e:
            print(f"连接服务器失败: {e}")
            return False

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
