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
    
    def add_turn_left(self, degrees=90):
        """添加左转指令"""
        self.blocks.append({
            'type': 'turn_left',
            'degrees': degrees
        })
    
    def add_turn_right(self, degrees=90):
        """添加右转指令"""
        self.blocks.append({
            'type': 'turn_right', 
            'degrees': degrees
        })
    
    def add_beep(self, frequency=440, duration=500):
        self.blocks.append({
            'type': 'beep',
            'frequency': frequency,
            'duration': duration
        })
    
    def generate_c_code(self):
        c_lines = []
        for block in self.blocks:
            if block['type'] == 'move':
                if block['direction'] == 'forward':
                    c_lines.append(f"forward({block['speed']}, {block['distance']});")
                else:
                    c_lines.append(f"back({block['speed']}, {block['distance']});")
            elif block['type'] == 'turn_left':
                c_lines.append(f"turn_left({block['degrees']});")
            elif block['type'] == 'turn_right':
                c_lines.append(f"turn_right({block['degrees']});")
            elif block['type'] == 'beep':
                c_lines.append(f"beep({block['frequency']}, {block['duration']});")
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
