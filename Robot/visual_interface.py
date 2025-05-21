import pygame
import sys
import requests
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
GREEN = (0, 255, 0)

# 积木块定义
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
    'execute': {'rect': pygame.Rect(300, 500, 200, 50), 'text': "执行"}
}

class ParamInput:
    def __init__(self, x, y, width, height, default_value):
        self.rect = pygame.Rect(x, y, width, height)
        self.value = str(default_value)
        self.active = False
        
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
            elif event.unicode.isdigit():
                self.value += event.unicode

def draw_button(screen, rect, text, color=BLUE):
    pygame.draw.rect(screen, color, rect)
    font = pygame.font.SysFont('simhei', 30)
    text_surface = font.render(text, True, WHITE)
    screen.blit(text_surface, rect)

def execute_on_robot(robot_id=0):
    """执行生成的C代码到指定机器人"""
    c_program = generator.generate_c_code()
    print("正在执行的C代码:\n", c_program)  # 调试输出
    
    try:
        response = requests.post(
            'http://localhost:8080/execute_c_program',
            json={
                'robot_id': robot_id,
                'program': c_program
            },
            timeout=5
        )
        if response.status_code != 200:
            return {'error': f'HTTP错误 {response.status_code}'}
        return response.json()
    except requests.exceptions.ConnectionError:
        return {'error': '无法连接到服务器，请先运行robot.py'}
    except Exception as e:
        return {'error': str(e)}

def main():
    running = True
    current_block = None
    param_inputs = []
    error_message = ""
    error_time = 0
    
    while running:
        screen.fill(WHITE)
        
        # 绘制积木块
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
        
        # 显示错误信息（5秒后消失）
        if error_message and pygame.time.get_ticks() - error_time < 5000:
            error_font = pygame.font.SysFont('simhei', 24)
            error_surface = error_font.render(f"错误: {error_message}", True, RED)
            screen.blit(error_surface, (300, 550))
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for name, block in BLOCKS.items():
                    if block['rect'].collidepoint(event.pos):
                        if name == 'execute':
                            result = execute_on_robot()
                            print("执行结果:", result)
                            if 'error' in result:
                                error_message = result['error']
                                error_time = pygame.time.get_ticks()
                        else:
                            current_block = name
                            param_inputs = []
                            y_offset = block['rect'].y + block['rect'].height + 10
                            for param in block['params']:
                                param_inputs.append(ParamInput(
                                    300, y_offset, 100, 30, param['default']))
                                y_offset += 40
            
            elif event.type == pygame.KEYDOWN and current_block:
                for input_box in param_inputs:
                    input_box.handle_event(event)
                
                # 回车确认参数
                if event.key == pygame.K_RETURN and param_inputs:
                    params = [int(input_box.value) for input_box in param_inputs]
                    if current_block == 'forward':
                        generator.add_move_forward(*params)
                    elif current_block == 'back':
                        generator.add_move_back(*params)
                    elif current_block == 'left':
                        generator.add_turn_left(params[0])  # 只传角度
                    elif current_block == 'right':
                        generator.add_turn_right(params[0])  # 只传角度
                    
                    current_block = None
                    param_inputs = []
        
        pygame.display.flip()
        clock.tick(60)
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
