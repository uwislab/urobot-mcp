import pygame
import requests
from visual_generator import VisualProgramGenerator

# 初始化
pygame.init()
screen = pygame.display.set_mode((800, 600))
generator = VisualProgramGenerator()

def execute_on_robot(robot_id=0):
    """执行生成的C代码到指定机器人"""
    c_program = generator.generate_c_code()
    try:
        response = requests.post(
            'http://localhost:8080/execute_c_program',
            json={
                'robot_id': robot_id,
                'program': c_program
            },
            timeout=5  # 添加超时
        )
        response.raise_for_status()  # 检查HTTP错误
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"请求失败: {e}")
        return {'error': str(e)}
    except ValueError as e:
        print(f"JSON解析失败: {e}")
        return {'error': 'Invalid server response'}

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
                        generator.add_move_forward(4, 1)  # 速度4，距离1
                    elif name == 'left':
                        generator.add_turn('left', 90)  # 左转90度
                    elif name == 'right':
                        generator.add_turn('right', 90)  # 右转90度
                    elif name == 'execute':
                        result = execute_on_robot()
                        print("执行结果:", result)
                        if 'error' in result:
                            # 显示错误信息
                            font = pygame.font.SysFont(None, 30)
                            error_text = font.render(f"错误: {result['error']}", True, (255, 0, 0))
                            screen.blit(error_text, (300, 550))
    
    pygame.display.flip()

pygame.quit()
"""
机器人可视化编程界面
提供图形化按钮来生成C代码并发送到仿真系统

主要功能:
- 通过图形界面生成机器人控制代码
- 发送代码到仿真服务器执行
- 显示执行结果和错误信息

使用说明:
1. 点击"前进"、"左转"、"右转"按钮添加指令
2. 点击"执行"按钮发送代码到机器人
3. 错误信息会显示在界面底部
"""

import tkinter as tk
from tkinter import messagebox
import requests
import json

class VisualInterface:
    def __init__(self, root):
        self.root = root
        self.root.title("机器人可视化编程")
        self.root.geometry("800x600")
        
        # 程序代码存储
        self.program_lines = []
        
        # 创建界面布局
        self.create_widgets()
        
    def create_widgets(self):
        # 左侧控制面板
        control_frame = tk.Frame(self.root, width=200, bg="#f0f0f0")
        control_frame.pack(side=tk.LEFT, fill=tk.Y, padx=5, pady=5)
        
        # 控制按钮
        tk.Button(control_frame, text="前进", command=self.add_forward, height=2, width=15).pack(pady=5)
        tk.Button(control_frame, text="左转", command=self.add_turn_left, height=2, width=15).pack(pady=5)
        tk.Button(control_frame, text="右转", command=self.add_turn_right, height=2, width=15).pack(pady=5)
        
        # 机器人选择
        tk.Label(control_frame, text="选择机器人:", bg="#f0f0f0").pack(pady=(20,5))
        self.robot_var = tk.IntVar(value=0)
        for i in range(2):  # 默认支持2个机器人
            tk.Radiobutton(control_frame, text=f"机器人 {i}", variable=self.robot_var, 
                          value=i, bg="#f0f0f0").pack(anchor=tk.W)
        
        # 执行按钮
        tk.Button(control_frame, text="执行程序", command=self.execute_program, 
                 height=2, width=15, bg="#4CAF50", fg="white").pack(pady=20)
        
        # 清空按钮
        tk.Button(control_frame, text="清空程序", command=self.clear_program, 
                 height=2, width=15, bg="#f44336", fg="white").pack()
        
        # 右侧代码预览
        code_frame = tk.Frame(self.root)
        code_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        tk.Label(code_frame, text="生成的C代码:").pack(anchor=tk.W)
        self.code_text = tk.Text(code_frame, wrap=tk.WORD, font=("Courier", 12))
        self.code_text.pack(fill=tk.BOTH, expand=True)
        
        # 初始代码
        self.update_code_display()
    
    def add_forward(self):
        self.program_lines.append("    forward(4, 1);")
        self.update_code_display()
    
    def add_turn_left(self):
        self.program_lines.append("    turn_left(90);")
        self.update_code_display()
    
    def add_turn_right(self):
        self.program_lines.append("    turn_right(90);") 
        self.update_code_display()
    
    def clear_program(self):
        self.program_lines = []
        self.update_code_display()
    
    def update_code_display(self):
        self.code_text.delete(1.0, tk.END)
        self.code_text.insert(tk.END, "void main() {\n")
        for line in self.program_lines:
            self.code_text.insert(tk.END, line + "\n")
        self.code_text.insert(tk.END, "}\n")
    
    def execute_program(self):
        if not self.program_lines:
            messagebox.showwarning("警告", "请先添加程序指令!")
            return
            
        full_program = "void main() {\n" + "\n".join(self.program_lines) + "\n}"
        
        try:
            response = requests.post(
                'http://localhost:8080/execute_c_program',
                json={
                    'robot_id': self.robot_var.get(),
                    'program': full_program
                }
            )
            
            if response.status_code == 200:
                messagebox.showinfo("成功", "程序已发送到机器人!")
            else:
                messagebox.showerror("错误", f"执行失败: {response.json().get('error', '未知错误')}")
        except Exception as e:
            messagebox.showerror("错误", f"无法连接到服务器: {str(e)}")

def main():
    root = tk.Tk()
    app = VisualInterface(root)
    root.mainloop()

if __name__ == "__main__":
    main()
