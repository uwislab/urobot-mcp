import json
import requests

class VisualProgramGenerator:
    def __init__(self):
        self.blocks = []
        
    def add_move_forward(self, speed=4, distance=1):
        """添加前进指令"""
        self.blocks.append({
            'type': 'move',
            'direction': 'forward',
            'speed': speed,
            'distance': distance
        })
    
    def add_move_back(self, speed=4, distance=1):
        """添加后退指令"""
        self.blocks.append({
            'type': 'move',
            'direction': 'back',
            'speed': speed,
            'distance': distance
        })
    
    def add_turn(self, direction, degrees=90):
        """添加转向指令
        Args:
            direction: 'left'或'right'
            degrees: 转向角度
        """
        self.blocks.append({
            'type': 'turn',
            'direction': direction,
            'degrees': degrees
        })
    
    def add_beep(self, frequency=440, duration=500):
        self.blocks.append({
            'type': 'beep',
            'frequency': frequency,
            'duration': duration
        })
    
    def generate_c_code(self):
        c_lines = ["void main() {"]
        for block in self.blocks:
            if block['type'] == 'move':
                c_lines.append(f"    {block['direction']}({block['speed']}, {block['distance']});")
            elif block['type'] == 'turn':
                c_lines.append(f"    turn_{block['direction']}({block['degrees']});")
            elif block['type'] == 'beep':
                c_lines.append(f"    beep({block['frequency']}, {block['duration']});")
            elif block['type'] == 'say':
                c_lines.append(f'    gpp_say({block["mode"]}, "{block["text"]}");')
        c_lines.append("}")
        return '\n'.join(c_lines)
    
    def execute_on_robot(self, robot_id=0):
        c_program = self.generate_c_code()
        response = requests.post(
            'http://localhost:8080/execute_c_program',
            json={
                'robot_id': robot_id,
                'program': c_program
            }
        )
        return response.json()
