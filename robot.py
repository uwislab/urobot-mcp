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
        
        # 绘制机器人中心点
        center_x = self.x + self.width/2
        center_y = self.y + self.height/2
        pygame.draw.circle(screen, RED, (int(center_x), int(center_y)), 5)
        
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
