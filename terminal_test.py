import subprocess
import time

# 测试终端命令控制
def test_terminal_commands():
    commands = [
        "forward 4 5",    # 前进速度4，距离5
        "right 90",       # 右转90度
        "forward 2 3",    # 前进速度2，距离3
        "left 45",        # 左转45度
        "stop"            # 停止
    ]
    
    for cmd in commands:
        print(f"执行命令: {cmd}")
        subprocess.run(["python", "robot.py", "-c", cmd])
        time.sleep(1)  # 等待命令执行完成

if __name__ == "__main__":
    test_terminal_commands()
