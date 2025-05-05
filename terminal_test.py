import subprocess
import time

# 测试终端命令控制
def test_terminal_commands():
    commands = [
        # 基本移动命令
        "forward 0 4 5",    # 机器人0前进速度4，距离5
        "right 0 90",       # 机器人0右转90度
        "back 1 3 2",       # 机器人1后退速度3，距离2
        "left 1 45",        # 机器人1左转45度
        "stop 0",           # 机器人0停止
        
        # 边界条件测试
        "forward 0 10 1",    # 测试最大速度
        "forward 0 1 100",   # 测试长距离移动
        "right 0 360",       # 测试完整旋转
        "left 1 720",        # 测试多圈旋转
        
        # 错误处理测试
        "forward 2 4 5",     # 测试不存在的机器人ID
        "move 0",            # 测试无效命令
        "forward 0",         # 测试缺少参数
        "back 0 x y",        # 测试无效参数类型
        
        # 组合命令测试
        "forward 0 4 2; right 0 90; forward 0 4 2",  # 组合命令
        "beep 0 440 1000",   # 测试蜂鸣器
        "say 0 hello"        # 测试语音
    ]
    
    for cmd in commands:
        print(f"执行命令: {cmd}")
        subprocess.run(["python", "robot.py", "-c", cmd])
        time.sleep(1)  # 等待命令执行完成

if __name__ == "__main__":
    test_terminal_commands()
