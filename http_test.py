import requests
import time

# 测试HTTP API控制
def test_http_commands():
    base_url = "http://localhost:8080/robot.html"
    commands = [
        ("forward", 0),  # 机器人0前进
        ("right", 0),    # 机器人0右转
        ("back", 1),     # 机器人1后退
        ("left", 1),     # 机器人1左转
        ("stop", 0)      # 机器人0停止
    ]
    
    for cmd, robot_id in commands:
        print(f"发送命令: {cmd} 给机器人 {robot_id}")
        try:
            # 使用requests库发送HTTP请求
            response = requests.get(f"{base_url}?cmd={cmd}&id={robot_id}", timeout=5)
            print(f"响应状态码: {response.status_code}")
        except Exception as e:
            print(f"请求失败: {e}")
        time.sleep(1)  # 等待命令执行完成

if __name__ == "__main__":
    test_http_commands()
