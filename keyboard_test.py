import pygame
import time

# 测试键盘控制
def test_keyboard_controls():
    pygame.init()
    screen = pygame.display.set_mode((100, 100))
    pygame.display.set_caption("键盘测试")
    
    print("键盘控制测试开始...")
    print("使用方向键控制机器人，按ESC退出")
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    print("上方向键按下 - 前进")
                elif event.key == pygame.K_DOWN:
                    print("下方向键按下 - 后退")
                elif event.key == pygame.K_LEFT:
                    print("左方向键按下 - 左转")
                elif event.key == pygame.K_RIGHT:
                    print("右方向键按下 - 右转")
                elif event.key == pygame.K_1:
                    print("切换到机器人1")
                elif event.key == pygame.K_2:
                    print("切换到机器人2")
                elif event.key == pygame.K_ESCAPE:
                    running = False
    
    pygame.quit()
    print("键盘测试结束")

if __name__ == "__main__":
    test_keyboard_controls()
