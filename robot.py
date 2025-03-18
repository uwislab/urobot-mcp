import pygame
import math

# 初始化pygame
pygame.init()

# 屏幕尺寸
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("机器人仿真")

# 颜色定义
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# 机器人类
class Robot:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 40
        self.height = 60
        self.speed = 4  # 提高移动速度
        
    def draw(self, screen):
        # 绘制圆形底盘
        center_x = self.x + self.width/2
        center_y = self.y + self.height/2
        pygame.draw.circle(screen, (100, 100, 100), (int(center_x), int(center_y + 10)), 30)  # 灰色底盘
        
        # 绘制主体
        body_rect = pygame.Rect(self.x + 10, self.y, 20, 40)
        pygame.draw.rect(screen, (0, 128, 255), body_rect)  # 浅蓝色主体
        pygame.draw.rect(screen, BLACK, body_rect, 2)  # 黑色边框
        
        # 绘制天线
        pygame.draw.line(screen, RED, 
                        (center_x - 5, self.y),
                        (center_x - 5, self.y - 15), 2)
        pygame.draw.circle(screen, RED, (int(center_x - 5), int(self.y - 15)), 3)
        
        # 绘制轮子
        pygame.draw.circle(screen, BLACK, (int(self.x + 5), int(self.y + 50)), 8)
        pygame.draw.circle(screen, BLACK, (int(self.x + 35), int(self.y + 50)), 8)
        
        # 绘制眼睛
        pygame.draw.circle(screen, WHITE, (int(center_x - 5), int(self.y + 15)), 3)
        pygame.draw.circle(screen, WHITE, (int(center_x + 5), int(self.y + 15)), 3)
        pygame.draw.circle(screen, BLACK, (int(center_x - 5), int(self.y + 15)), 1)
        pygame.draw.circle(screen, BLACK, (int(center_x + 5), int(self.y + 15)), 1)
        
    def move_up(self):
        self.y -= self.speed
        
    def move_down(self):
        self.y += self.speed
        
    def move_left(self):
        self.x -= self.speed
        
    def move_right(self):
        self.x += self.speed

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
