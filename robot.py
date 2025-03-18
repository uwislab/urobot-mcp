import pygame
import math
import http.server
import socketserver
import threading
import base64
import ctypes

# 初始化pygame
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

# 机器人类
class Robot:
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
        
    def draw(self, screen):
        # 绘制墙壁
        pygame.draw.rect(screen, BLACK, (0, 0, WIDTH, WALL_THICKNESS))  # 上墙
        pygame.draw.rect(screen, BLACK, (0, 0, WALL_THICKNESS, HEIGHT))  # 左墙
        pygame.draw.rect(screen, BLACK, (WIDTH - WALL_THICKNESS, 0, WALL_THICKNESS, HEIGHT))  # 右墙
        pygame.draw.rect(screen, BLACK, (0, HEIGHT - WALL_THICKNESS, WIDTH, WALL_THICKNESS))  # 下墙
        
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
            
        # 计算新位置
        new_x = self.x + self.direction[0] * self.speed
        new_y = self.y + self.direction[1] * self.speed

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
    def __init__(self):
        self.robots = []
        self.lock = threading.Lock()
        
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
    def __init__(self, *args, **kwargs):
        self.robot_manager = kwargs.pop('robot_manager')
        super().__init__(*args, **kwargs)
    def do_GET(self):
        if self.path.startswith('/robot.html'):
            params = self.path.split('?')[1].split('&')
            cmd = None
            robot_id = None
            for param in params:
                if param.startswith('cmd='):
                    cmd = param[4:]
                elif param.startswith('id='):
                    robot_id = int(param[3:])
            
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
        
        # Simple C-like interpreter
        lines = c_code.split('\n')
        for line in lines:
            line = line.strip()
            
            # Handle function calls
            if line.startswith('forward('):
                params = line[8:-1].split(',')
                robot.forward(int(params[0]), int(params[1]))
            elif line.startswith('back('):
                params = line[5:-1].split(',')
                robot.back(int(params[0]), int(params[1]))
            elif line.startswith('turn_left('):
                robot.turn_left(int(line[10:-1]))
            elif line.startswith('turn_right('):
                robot.turn_right(int(line[11:-1]))
            elif line.startswith('gpp_say('):
                params = line[8:-1].split(',')
                mode = int(params[0])
                text = params[1].strip().strip('"')
                robot.gpp_say(mode, text)
            elif line.startswith('beep('):
                params = line[5:-1].split(',')
                robot.beep(int(params[0]), int(params[1]))
            elif line.startswith('stop('):
                robot.speed = 0
            elif line.startswith('set_speed('):
                speed = int(line[10:-1])
                robot.speed = min(8, max(1, speed))
            elif line.startswith('get_position()'):
                x = int(robot.x)
                y = int(robot.y)
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(f'{{"x":{x},"y":{y}}}'.encode())
                return
            
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
def main():
    clock = pygame.time.Clock()
    robot_manager = RobotManager()
    
    # Add initial robots
    robot = robot_manager.add_robot(WIDTH//2 - 100, HEIGHT//2)
    robot_manager.add_robot(WIDTH//2 + 100, HEIGHT//2)
    
    # 添加测试动作
    robot.forward(4, 10)
    robot.turn_right(90)
    robot.forward(4, 10)
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                
        # 检查碰撞
        robot_manager.check_collisions()
            
        # 绘制场景
        screen.fill(WHITE)
        for robot in robot_manager.robots:
            robot.draw(screen)
        pygame.display.flip()
        
        clock.tick(60)
        
    pygame.quit()

if __name__ == "__main__":
    # Create robot manager
    robot_manager = RobotManager()
    
    # Start HTTP server in separate thread
    http_thread = threading.Thread(target=start_http_server, args=(robot_manager,))
    http_thread.daemon = True
    http_thread.start()
    
    # Start main loop
    main()
