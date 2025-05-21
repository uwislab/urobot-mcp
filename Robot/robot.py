"""
机器人仿真系统主模块
包含:
- 机器人仿真逻辑
- HTTP服务器
- 命令行接口
- 图形界面
"""

import pygame
import math
import http.server
import socketserver
import threading
import base64
import ctypes
import argparse
import json

# 初始化pygame图形库
pygame.init()

# 屏幕尺寸和墙壁
WIDTH, HEIGHT = 800, 600
WALL_THICKNESS = 20
PLAY_AREA = pygame.Rect(WALL_THICKNESS, WALL_THICKNESS, 
                       WIDTH - 2*WALL_THICKNESS, HEIGHT - 2*WALL_THICKNESS)
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("机器人仿真")

# 颜色定义
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

class Robot:
    """机器人仿真类
    
    属性:
        x, y: 当前位置坐标
        id: 机器人唯一标识
        active: 是否活动状态
        width, height: 机器人尺寸
        speed: 移动速度
        direction: 移动方向向量
        angle: 当前朝向角度
        command_queue: 待执行命令队列
        executing: 是否正在执行命令
        keys_pressed: 键盘按键状态
        
    方法:
        实现机器人移动、转向、发声等基本功能
    """
    def __init__(self, x, y, robot_id):
        self.x = x
        self.y = y
        self.id = robot_id
        self.active = True
        self.width = 40
        self.height = 60
        self.speed = 4
        self.direction = [0, 0]  # 运动方向 [x, y]
        self.angle = 0  # 当前角度
        self.command_queue = []
        self.executing = False
        self.keys_pressed = {
            'up': False,
            'down': False,
            'left': False,
            'right': False
        }
        
    def draw(self, screen):
        # 绘制墙壁
        pygame.draw.rect(screen, BLACK, (0, 0, WIDTH, WALL_THICKNESS))  # 上墙
        pygame.draw.rect(screen, BLACK, (0, 0, WALL_THICKNESS, HEIGHT))  # 左墙
        pygame.draw.rect(screen, BLACK, (WIDTH - WALL_THICKNESS, 0, WALL_THICKNESS, HEIGHT))  # 右墙
        pygame.draw.rect(screen, BLACK, (0, HEIGHT - WALL_THICKNESS, WIDTH, WALL_THICKNESS))  # 下墙
        
        # 在底部显示信息
        font = pygame.font.SysFont('simhei', 20)
        # 显示服务器信息
        info_text = f"服务器: localhost:8080"
        text_surface = font.render(info_text, True, BLACK)
        text_rect = text_surface.get_rect(center=(WIDTH//2, HEIGHT - 50))
        screen.blit(text_surface, text_rect)
        
        # 显示当前选中的机器人
        select_text = f"当前控制: 机器人 {self.id+1} (按1-9切换)"
        select_surface = font.render(select_text, True, RED if self.id == robot_manager.selected_robot else BLACK)
        select_rect = select_surface.get_rect(center=(WIDTH//2, HEIGHT - 30))
        screen.blit(select_surface, select_rect)
        
        # 显示最后接收到的命令
        if hasattr(self, 'last_command'):
            cmd_text = f"最后命令: {self.last_command}"
            cmd_surface = font.render(cmd_text, True, BLACK)
            cmd_rect = cmd_surface.get_rect(center=(WIDTH//2, HEIGHT - 10))
            screen.blit(cmd_surface, cmd_rect)
        
        # 创建旋转后的表面
        robot_surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        
        # 绘制车身
        pygame.draw.rect(robot_surface, (0, 128, 255), (10, 0, 20, 40))  # 浅蓝色主体
        pygame.draw.rect(robot_surface, BLACK, (10, 0, 20, 40), 2)  # 黑色边框
        
        # 绘制轮子
        pygame.draw.circle(robot_surface, BLACK, (15, 50), 8)
        pygame.draw.circle(robot_surface, BLACK, (25, 50), 8)
        
        # 绘制前灯
        pygame.draw.circle(robot_surface, YELLOW, (20, 5), 3)
        
        # 旋转表面
        rotated_surface = pygame.transform.rotate(robot_surface, self.angle)
        new_rect = rotated_surface.get_rect(center=(self.x + self.width/2, self.y + self.height/2))
        
        # 绘制到屏幕上
        screen.blit(rotated_surface, new_rect.topleft)
        
    def move_up(self):
        self.direction = [0, -1]
        self.angle = 0
        self._move()
        
    def move_down(self):
        self.direction = [0, 1]
        self.angle = 180
        self._move()
        
    def move_left(self):
        self.direction = [-1, 0]
        self.angle = 90
        self._move()
        
    def move_right(self):
        self.direction = [1, 0]
        self.angle = 270
        self._move()
        
    def _move(self):
        if not self.active:
            return
            
        # 计算新位置 - 考虑所有按下的方向键
        move_x = 0
        move_y = 0
        
        if self.keys_pressed['up']:
            move_y -= self.speed
            self.angle = 0
        if self.keys_pressed['down']:
            move_y += self.speed
            self.angle = 180
        if self.keys_pressed['left']:
            move_x -= self.speed
            self.angle = 90
        if self.keys_pressed['right']:
            move_x += self.speed
            self.angle = 270
            
        # 对角线移动时保持45度角
        if move_x != 0 and move_y != 0:
            if move_y < 0:  # 向上
                self.angle = 315 if move_x > 0 else 45
            else:  # 向下
                self.angle = 225 if move_x < 0 else 135
                
        # 计算新位置
        new_x = self.x + move_x
        new_y = self.y + move_y

        # 检查是否碰撞墙壁
        if new_x < WALL_THICKNESS:
            self.direction[0] *= -1
            self.angle = 270 if self.angle == 90 else 90
            new_x = WALL_THICKNESS
        elif new_x + self.width > WIDTH - WALL_THICKNESS:
            self.direction[0] *= -1
            self.angle = 270 if self.angle == 90 else 90
            new_x = WIDTH - WALL_THICKNESS - self.width
            
        if new_y < WALL_THICKNESS:
            self.direction[1] *= -1
            self.angle = 0 if self.angle == 180 else 180
            new_y = WALL_THICKNESS
        elif new_y + self.height > HEIGHT - WALL_THICKNESS:
            self.direction[1] *= -1
            self.angle = 0 if self.angle == 180 else 180
            new_y = HEIGHT - WALL_THICKNESS - self.height
            
        self.x = new_x
        self.y = new_y

    def forward(self, speed, distance):
        self.speed = min(8, max(1, speed)) / 2
        steps = distance * 10
        for _ in range(steps):
            self._move()
            pygame.time.wait(50)

    def back(self, speed, distance):
        self.speed = min(8, max(1, speed)) / 2
        steps = distance * 10
        for _ in range(steps):
            self.x -= self.direction[0] * self.speed
            self.y -= self.direction[1] * self.speed
            pygame.time.wait(50)

    def turn_left(self, degrees):
        self.angle = (self.angle + degrees) % 360
        pygame.time.wait(degrees * 10)

    def turn_right(self, degrees):
        self.angle = (self.angle - degrees) % 360
        pygame.time.wait(degrees * 10)

    def gpp_say(self, mode, text):
        if mode == 0:
            # Interrupt current speech
            print(f"[SPEECH INTERRUPT] {text}")
        else:
            # Queue speech
            print(f"[SPEECH] {text}")

    def beep(self, frequency, duration):
        print(f"[BEEP] {frequency}Hz for {duration}ms")

class RobotManager:
    """机器人管理器
    
    功能:
    - 管理所有机器人实例
    - 处理机器人碰撞检测
    - 提供机器人选择功能
    """
    def __init__(self):
        self.robots = []
        self.lock = threading.Lock()
        self.selected_robot = 0  # 默认选中第一个机器人
        
    def add_robot(self, x, y):
        robot_id = len(self.robots)
        robot = Robot(x, y, robot_id)
        self.robots.append(robot)
        return robot_id
        
    def get_robot(self, robot_id):
        return self.robots[robot_id]
        
    def check_collisions(self):
        with self.lock:
            for i in range(len(self.robots)):
                r1 = self.robots[i]
                if not r1.active:
                    continue
                    
                # Check wall collisions
                if (r1.x < WALL_THICKNESS or 
                    r1.x + r1.width > WIDTH - WALL_THICKNESS or
                    r1.y < WALL_THICKNESS or 
                    r1.y + r1.height > HEIGHT - WALL_THICKNESS):
                    r1.active = False
                    continue
                    
                # Check robot collisions
                for j in range(i+1, len(self.robots)):
                    r2 = self.robots[j]
                    if not r2.active:
                        continue
                        
                    if (abs(r1.x - r2.x) < (r1.width + r2.width)/2 and 
                        abs(r1.y - r2.y) < (r1.height + r2.height)/2):
                        r1.active = False
                        r2.active = False

class HTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    """自定义HTTP请求处理器
    
    处理来自客户端的HTTP请求并转换为机器人控制命令
    支持:
    - 基本移动命令
    - C代码执行
    - 状态查询
    """
    def __init__(self, *args, **kwargs):
        self.robot_manager = kwargs.pop('robot_manager')
        self.last_command = ""
        super().__init__(*args, **kwargs)
    def do_POST(self):
        if self.path == '/execute_c_program':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            
            try:
                data = json.loads(post_data.decode())
                robot_id = data.get('robot_id', 0)
                c_program = data['program']
                
                robot = self.robot_manager.get_robot(robot_id)
                robot.last_command = c_program
                self.execute_c_code(robot_id, c_program)
                
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({'status': 'success'}).encode())
            except Exception as e:
                self.send_response(500)
                self.end_headers()
                self.wfile.write(json.dumps({'error': str(e)}).encode())

    def do_GET(self):
        if self.path.startswith('/robot.html'):
            params = self.path.split('?')[1].split('&')
            cmd = None
            robot_id = 0  # Default to first robot
            for param in params:
                if param.startswith('cmd='):
                    cmd = param[4:]
                elif param.startswith('id='):
                    robot_id = int(param[3:])
            
            # Handle simple movement commands
            if cmd in ['forward', 'back', 'left', 'right', 'stop']:
                try:
                    robot = self.robot_manager.get_robot(robot_id)
                    if cmd == 'forward':
                        robot.forward(4, 1)  # speed 4, distance 1
                    elif cmd == 'back':
                        robot.back(4, 1)
                    elif cmd == 'left':
                        robot.turn_left(90)
                    elif cmd == 'right':
                        robot.turn_right(90)
                    elif cmd == 'stop':
                        robot.speed = 0
                    
                    self.send_response(200)
                    self.end_headers()
                    return
                except Exception as e:
                    self.send_response(500)
                    self.end_headers()
                    return
            
            if cmd and robot_id is not None:
                try:
                    # Decode base64 and execute C code
                    c_code = base64.b64decode(cmd).decode('utf-8')
                    self.execute_c_code(robot_id, c_code)
                    self.send_response(200)
                except Exception as e:
                    self.send_response(500)
                    print(f"Error executing command: {e}")
                finally:
                    self.end_headers()
        else:
            self.send_response(404)
            self.end_headers()
            
    def execute_c_code(self, robot_id, c_code):
        robot = self.robot_manager.get_robot(robot_id)
        robot.command_queue = []  # 清空之前的命令
        
        for line in c_code.split('\n'):
            line = line.strip()
            if not line or line.startswith(('//', '/*', '*/', '*')):
                continue
            
            # 解析标准C函数调用
            if line.startswith(('forward(', 'back(', 'turn_left(', 'turn_right(', 'beep(', 'gpp_say(')):
                func_name = line.split('(')[0]
                params = line[line.find('(')+1:line.rfind(')')].split(',')
                
                # 处理字符串参数
                params = [p.strip().strip('"') for p in params]
                
                if func_name == 'forward':
                    robot.command_queue.append(('forward', (int(params[0]), int(params[1]))))
                elif func_name == 'back':
                    robot.command_queue.append(('back', (int(params[0]), int(params[1]))))
                elif func_name == 'turn_left':
                    robot.command_queue.append(('turn_left', (int(params[0]),)))
                elif func_name == 'turn_right':
                    robot.command_queue.append(('turn_right', (int(params[0]),)))
                elif func_name == 'beep':
                    robot.command_queue.append(('beep', (int(params[0]), int(params[1]))))
                elif func_name == 'gpp_say':
                    robot.command_queue.append(('gpp_say', (int(params[0]), params[1])))
            
            # Handle variable declarations
            elif line.startswith('int ') or line.startswith('float '):
                # Skip variable declarations
                continue
                
            # Handle loops
            elif 'for ' in line:
                # Simple for loop support
                parts = line.split(';')
                init = parts[0][4:].strip()
                condition = parts[1].strip()
                increment = parts[2][:-1].strip()
                
                # Execute initialization
                if '=' in init:
                    var, val = init.split('=')
                    locals()[var.strip()] = int(val.strip())
                    
                # Execute loop
                while eval(condition):
                    # Execute loop body
                    pass
                    
                    # Execute increment
                    exec(increment)
        
def start_http_server(robot_manager):
    PORT = 8080  # 改用8080端口
    handler = lambda *args, **kwargs: HTTPRequestHandler(*args, robot_manager=robot_manager, **kwargs)
    with socketserver.TCPServer(("", PORT), handler) as httpd:
        print(f"Serving at port {PORT}")
        httpd.serve_forever()

# 主循环
def execute_terminal_command(robot_manager, command):
    """执行终端命令控制机器人"""
    if not command:
        return
        
    parts = command.split()
    cmd = parts[0].lower()
    robot_id = 0  # 默认控制第一个机器人
    
    if len(parts) > 1 and parts[1].isdigit():
        robot_id = int(parts[1])
        if robot_id >= len(robot_manager.robots):
            print(f"错误: 机器人ID {robot_id} 不存在")
            return
    
    robot = robot_manager.get_robot(robot_id)
    
    try:
        if cmd == "forward":
            if len(parts) >= 3:
                speed = int(parts[-2])
                distance = int(parts[-1])
                robot.forward(speed, distance)
            else:
                print("格式错误: forward 需要速度和距离参数")
        elif cmd == "back":
            if len(parts) >= 3:
                speed = int(parts[-2])
                distance = int(parts[-1])
                robot.back(speed, distance)
            else:
                print("格式错误: back 需要速度和距离参数")
        elif cmd == "left":
            if len(parts) >= 2:
                degrees = int(parts[-1])
                robot.turn_left(degrees)
            else:
                print("格式错误: left 需要角度参数")
        elif cmd == "right":
            if len(parts) >= 2:
                degrees = int(parts[-1])
                robot.turn_right(degrees)
            else:
                print("格式错误: right 需要角度参数")
        elif cmd == "beep":
            if len(parts) >= 3:
                freq = int(parts[-2])
                duration = int(parts[-1])
                robot.beep(freq, duration)
            else:
                print("格式错误: beep 需要频率和时长参数")
        elif cmd == "say":
            if len(parts) >= 3:
                text = " ".join(parts[2:])
                robot.gpp_say(1, text)
            else:
                print("格式错误: say 需要文本参数")
        elif cmd == "stop":
            robot.speed = 0
        elif cmd == "speed":
            if len(parts) >= 2:
                speed = int(parts[-1])
                robot.speed = min(8, max(1, speed))
            else:
                print("格式错误: speed 需要速度参数")
        else:
            print(f"未知命令: {cmd}")
    except (IndexError, ValueError) as e:
        print(f"命令格式错误: {e}")

def main():
    # 解析命令行参数
    parser = argparse.ArgumentParser(description='机器人仿真控制')
    parser.add_argument('--command', '-c', type=str, help='直接执行控制命令')
    args = parser.parse_args()

    clock = pygame.time.Clock()
    robot_manager = RobotManager()
    
    # Add initial robots
    robot_id = robot_manager.add_robot(WIDTH//2 - 100, HEIGHT//2)
    robot_manager.add_robot(WIDTH//2 + 100, HEIGHT//2)
    
    # 示例命令 - 可以删除或保留作为演示
    robot = robot_manager.get_robot(robot_id)
    robot.command_queue.extend([
        ('forward', (4, 10)),
        ('turn_left', (90,)),
        ('forward', (4, 10))
    ])
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                
        # 检查碰撞
        robot_manager.check_collisions()
        
        # 处理键盘控制
        keys = pygame.key.get_pressed()
        if len(robot_manager.robots) > 0:
            # 处理机器人选择
            for i in range(1, 10):
                if keys[getattr(pygame, f'K_{i}')]:
                    if i-1 < len(robot_manager.robots):
                        robot_manager.selected_robot = i-1
            
            # 获取当前选中的机器人
            robot = robot_manager.robots[robot_manager.selected_robot]
            robot.keys_pressed['up'] = keys[pygame.K_UP]
            robot.keys_pressed['down'] = keys[pygame.K_DOWN]
            robot.keys_pressed['left'] = keys[pygame.K_LEFT]
            robot.keys_pressed['right'] = keys[pygame.K_RIGHT]
            
            # 处理移动
            if robot.keys_pressed['up']:
                robot.move_up()
            elif robot.keys_pressed['down']:
                robot.move_down()
            if robot.keys_pressed['left']:
                robot.move_left()
            elif robot.keys_pressed['right']:
                robot.move_right()
        
        # 执行队列中的命令
        for robot in robot_manager.robots:
            if robot.command_queue and not robot.executing:
                cmd, args = robot.command_queue.pop(0)
                robot.executing = True
                try:
                    getattr(robot, cmd)(*args)
                except Exception as e:
                    print(f"执行命令{cmd}出错:", e)
                finally:
                    robot.executing = False
            
        # 绘制场景
        screen.fill(WHITE)
        for robot in robot_manager.robots:
            robot.draw(screen)
        pygame.display.flip()
        
        clock.tick(60)
        
    pygame.quit()

def run_server():
    # Create robot manager
    robot_manager = RobotManager()
    
    # 添加初始机器人
    robot_manager.add_robot(WIDTH//2 - 100, HEIGHT//2)
    robot_manager.add_robot(WIDTH//2 + 100, HEIGHT//2)
    
    # Start HTTP server in separate thread
    http_thread = threading.Thread(target=start_http_server, args=(robot_manager,))
    http_thread.daemon = True
    http_thread.start()
    return robot_manager

if __name__ == "__main__":
    robot_manager = run_server()
    
    # 如果有命令行参数，执行命令后退出
    import sys
    if len(sys.argv) > 1 and sys.argv[1] in ['-c', '--command']:
        execute_terminal_command(robot_manager, " ".join(sys.argv[2:]))
        sys.exit(0)
    
    # 否则进入主循环
    main()
