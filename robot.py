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
                for j in range(i+1, len(self.robots)):
                    r1 = self.robots[i]
                    r2 = self.robots[j]
                    if (abs(r1.x - r2.x) < r1.width and 
                        abs(r1.y - r2.y) < r1.height):
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
        # Create C function from code
        c_func = ctypes.CFUNCTYPE(None)
        c_code = f"void func() {{ {c_code} }}"
        lib = ctypes.CDLL(None)
        libc = ctypes.CDLL("libc.so.6")
        libc.free.argtypes = [ctypes.c_void_p]
        
        # Compile and execute
        src = ctypes.c_char_p(c_code.encode('utf-8'))
        libc.free(src)
        
        # Get robot and execute command
        robot = self.robot_manager.get_robot(robot_id)
        # Here you would map C functions to robot actions
        # For example: move_up() -> robot.move_up()
        
def start_http_server(robot_manager):
    PORT = 8000
    handler = lambda *args, **kwargs: HTTPRequestHandler(*args, robot_manager=robot_manager, **kwargs)
    with socketserver.TCPServer(("", PORT), handler) as httpd:
        print(f"Serving at port {PORT}")
        httpd.serve_forever()

# 主循环
def main():
    clock = pygame.time.Clock()
    robot_manager = RobotManager()
    
    # Add initial robots
    robot_manager.add_robot(WIDTH//2 - 100, HEIGHT//2)
    robot_manager.add_robot(WIDTH//2 + 100, HEIGHT//2)
    
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
