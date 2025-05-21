import pygame
import sys
from visual_generator import VisualProgramGenerator

# 初始化
pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("机器人可视化编程")
clock = pygame.time.Clock()
generator = VisualProgramGenerator()

# 颜色定义
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GRAY = (200, 200, 200)

# 积木块定义 - 完全匹配robot.py的功能
BLOCKS = {
    'forward': {'rect': pygame.Rect(50, 100, 200, 50), 'text': "前进", 'params': [
        {'name': "速度", 'default': 4, 'range': (1, 8)},
        {'name': "距离", 'default': 1, 'range': (1, 10)}
    ]},
    'back': {'rect': pygame.Rect(50, 180, 200, 50), 'text': "后退", 'params': [
        {'name': "速度", 'default': 4, 'range': (1, 8)},
        {'name': "距离", 'default': 1, 'range': (1, 10)}
    ]},
    'left': {'rect': pygame.Rect(50, 260, 200, 50), 'text': "左转", 'params': [
        {'name': "角度", 'default': 90, 'range': (1, 360)}
    ]},
    'right': {'rect': pygame.Rect(50, 340, 200, 50), 'text': "右转", 'params': [
        {'name': "角度", 'default': 90, 'range': (1, 360)}
    ]},
    'beep': {'rect': pygame.Rect(50, 420, 200, 50), 'text': "蜂鸣", 'params': [
        {'name': "频率", 'default': 440, 'range': (20, 2000)},
        {'name': "时长", 'default': 500, 'range': (100, 3000)}
    ]},
    'say': {'rect': pygame.Rect(50, 500, 200, 50), 'text': "说话", 'params': [
        {'name': "模式", 'default': 1, 'range': (0, 1)},
        {'name': "文本", 'default': "你好", 'range': None}
    ]},
    'execute': {'rect': pygame.Rect(300, 520, 200, 50), 'text': "执行"}
}

class ParamInput:
    def __init__(self, x, y, width, height, default_value, param_type=int):
        self.rect = pygame.Rect(x, y, width, height)
        self.value = str(default_value)
        self.active = False
        self.param_type = param_type
        
    def draw(self, screen):
        color = BLUE if self.active else GRAY
        pygame.draw.rect(screen, color, self.rect, 2)
        font = pygame.font.SysFont('simhei', 24)
        text = font.render(self.value, True, BLACK)
        screen.blit(text, (self.rect.x + 5, self.rect.y + 5))
        
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.active = self.rect.collidepoint(event.pos)
        elif event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_RETURN:
                self.active = False
            elif event.key == pygame.K_BACKSPACE:
                self.value = self.value[:-1]
            elif self.param_type == int and event.unicode.isdigit():
                self.value += event.unicode
            elif self.param_type == str:
                self.value += event.unicode

def draw_button(screen, rect, text, color=BLUE):
    pygame.draw.rect(screen, color, rect)
    font = pygame.font.SysFont('simhei', 30)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect(center=rect.center)
    screen.blit(text_surface, text_rect)

def main():
    running = True
    current_block = None
    param_inputs = []
    text_input_active = False
    
    while running:
        screen.fill(WHITE)
        
        # 绘制积木块按钮
        for name, block in BLOCKS.items():
            draw_button(screen, block['rect'], block['text'])
        
        # 绘制参数输入框
        for input_box in param_inputs:
            input_box.draw(screen)
        
        # 显示生成的代码
        code_text = generator.generate_c_code()
        font = pygame.font.SysFont('simhei', 20)
        y_pos = 100
        for line in code_text.split('\n'):
            text = font.render(line, True, BLACK)
            screen.blit(text, (300, y_pos))
            y_pos += 25
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # 检查是否点击了积木块
                for name, block in BLOCKS.items():
                    if block['rect'].collidepoint(event.pos):
                        if name == 'execute':
                            result = generator.execute_on_robot()
                            print("执行结果:", result)
                        else:
                            current_block = name
                            param_inputs = []
                            y_offset = block['rect'].y + block['rect'].height + 10
                            for param in block['params']:
                                param_type = str if param['name'] == "文本" else int
                                param_inputs.append(ParamInput(
                                    300, y_offset, 200, 30, 
                                    param['default'], param_type))
                                y_offset += 40
            
            elif event.type == pygame.KEYDOWN and current_block:
                for input_box in param_inputs:
                    input_box.handle_event(event)
                
                # 回车确认参数
                if event.key == pygame.K_RETURN and param_inputs:
                    params = []
                    for input_box in param_inputs:
                        if input_box.param_type == int:
                            params.append(int(input_box.value))
                        else:
                            params.append(input_box.value)
                    
                    # 调用对应的生成器方法
                    if current_block == 'forward':
                        generator.add_move_forward(*params)
                    elif current_block == 'back':
                        generator.add_move_back(*params)
                    elif current_block == 'left':
                        generator.add_turn_left(*params)
                    elif current_block == 'right':
                        generator.add_turn_right(*params)
                    elif current_block == 'beep':
                        generator.add_beep(*params)
                    elif current_block == 'say':
                        generator.add_say(*params)
                    
                    current_block = None
                    param_inputs = []
        
        pygame.display.flip()
        clock.tick(60)
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
