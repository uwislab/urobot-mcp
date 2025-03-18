import pygame
import math

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
    def __init__(self, x, y):
        self.x = x
        self.y = y
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

# 主循环
def main():
    clock = pygame.time.Clock()
    robot = Robot(WIDTH//2, HEIGHT//2)
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                
        # 获取按键状态
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            robot.move_up()
        if keys[pygame.K_DOWN]:
            robot.move_down()
        if keys[pygame.K_LEFT]:
            robot.move_left()
        if keys[pygame.K_RIGHT]:
            robot.move_right()
            
        # 绘制场景
        screen.fill(WHITE)
        robot.draw(screen)
        pygame.display.flip()
        
        clock.tick(60)
        
    pygame.quit()

if __name__ == "__main__":
    main()
