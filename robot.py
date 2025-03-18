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
        self.speed = 2
        self.angle = 0  # 朝向角度
        
    def draw(self, screen):
        # 绘制机器人主体
        pygame.draw.rect(screen, BLUE, (self.x, self.y, self.width, self.height))
        
        # 绘制方向指示器
        front_x = self.x + self.width/2 + math.cos(math.radians(self.angle)) * 30
        front_y = self.y + self.height/2 + math.sin(math.radians(self.angle)) * 30
        pygame.draw.line(screen, RED, 
                        (self.x + self.width/2, self.y + self.height/2),
                        (front_x, front_y), 3)
        
    def move_forward(self):
        self.x += math.cos(math.radians(self.angle)) * self.speed
        self.y += math.sin(math.radians(self.angle)) * self.speed
        
    def rotate(self, angle):
        self.angle = (self.angle + angle) % 360

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
            robot.move_forward()
        if keys[pygame.K_LEFT]:
            robot.rotate(-2)
        if keys[pygame.K_RIGHT]:
            robot.rotate(2)
            
        # 绘制场景
        screen.fill(WHITE)
        robot.draw(screen)
        pygame.display.flip()
        
        clock.tick(60)
        
    pygame.quit()

if __name__ == "__main__":
    main()
