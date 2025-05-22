import requests
import time

"""
HTTP API测试模块
用于测试机器人控制系统的HTTP接口功能
包含各种边界条件和错误情况的测试用例
"""
def test_http_commands():
    """执行HTTP接口测试
    
    测试内容包括:
    - 基本移动命令
    - 边界条件测试
    - 错误处理测试
    - 特殊功能测试
    """
    base_url = "http://localhost:8080/robot.html"  # 服务器基础URL
    commands = [
        # 基本移动命令
        ("forward", 0),  # 机器人0前进
        ("right", 0),    # 机器人0右转
        ("back", 1),     # 机器人1后退
        ("left", 1),     # 机器人1左转
        ("stop", 0),     # 机器人0停止
        
        # 边界条件测试
        ("forward?speed=8&distance=1", 0),  # 测试最大速度
        ("forward?speed=1&distance=100", 0), # 测试长距离
        ("right?degrees=360", 0),           # 测试完整旋转
        ("left?degrees=720", 1),            # 测试多圈旋转
        
        # 错误处理测试
        ("forward", 2),  # 测试不存在的机器人ID
        ("move", 0),     # 测试无效命令
        ("", 0),         # 测试空命令
        ("forward?speed=x", 0),  # 测试无效参数
        
        # 特殊功能测试
        ("beep?freq=440&duration=1000", 0),  # 测试蜂鸣器
        ("say?text=hello", 0)               # 测试语音
    ]
    
    for cmd, robot_id in commands:
        print(f"发送命令: {cmd} 给机器人 {robot_id}")
        try:
            # 使用requests库发送HTTP请求
            # 处理带参数的URL
            if '?' in cmd:
                url = f"{base_url}?{cmd.split('?')[1]}&id={robot_id}"
            else:
                url = f"{base_url}?cmd={cmd}&id={robot_id}"
            
            print(f"请求URL: {url}")
            response = requests.get(url, timeout=5)
            print(f"响应状态码: {response.status_code}")
        except Exception as e:
            print(f"请求失败: {e}")
        time.sleep(1)  # 等待命令执行完成

if __name__ == "__main__":
    test_http_commands()
