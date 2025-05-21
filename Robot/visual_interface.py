import pygame
from visual_generator import VisualProgramGenerator

# 初始化
pygame.init()
screen = pygame.display.set_mode((800, 600))
generator = VisualProgramGenerator()

# 积木块定义
BLOCKS = {
    'forward': {'rect': pygame.Rect(50, 100, 200, 50), 'text': "前进"},
    'left': {'rect': pygame.Rect(50, 200, 200, 50), 'text': "左转"},
    'right': {'rect': pygame.Rect(50, 300, 200, 50), 'text': "右转"},
    'execute': {'rect': pygame.Rect(300, 500, 200, 50), 'text': "执行"}
}

# 主循环
running = True
while running:
    screen.fill((255, 255, 255))
    
    # 绘制积木块
    for name, block in BLOCKS.items():
        pygame.draw.rect(screen, (0, 0, 255), block['rect'])
        font = pygame.font.SysFont(None, 30)
        text = font.render(block['text'], True, (255, 255, 255))
        screen.blit(text, block['rect'].center)
    
    # 显示生成的代码
    code_text = generator.generate_c_code()
    font = pygame.font.SysFont(None, 24)
    y_pos = 100
    for line in code_text.split('\n'):
        text = font.render(line, True, (0, 0, 0))
        screen.blit(text, (300, y_pos))
        y_pos += 30
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            for name, block in BLOCKS.items():
                if block['rect'].collidepoint(event.pos):
                    if name == 'forward':
                        generator.add_move_forward()
                    elif name == 'left':
                        generator.add_turn('left', 90)
                    elif name == 'right':
                        generator.add_turn('right', 90)
                    elif name == 'execute':
                        result = generator.execute_on_robot()
                        print("执行结果:", result)
    
    pygame.display.flip()

pygame.quit()
