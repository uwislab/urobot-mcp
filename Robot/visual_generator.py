import json
import requests

class VisualProgramGenerator:
    def __init__(self):
        self.blocks = []
        
    def add_move_forward(self, speed=4, distance=1):
        self.blocks.append({
            'type': 'move',
            'direction': 'forward',
            'speed': speed,
            'distance': distance
        })
    
    def add_turn(self, direction, degrees):
        self.blocks.append({
            'type': 'turn',
            'direction': direction,
            'degrees': degrees
        })
    
    def generate_c_code(self):
        c_lines = ["void main() {"]
        for block in self.blocks:
            if block['type'] == 'move':
                c_lines.append(f"    forward({block['speed']}, {block['distance']});")
            elif block['type'] == 'turn':
                c_lines.append(f"    turn_{block['direction']}({block['degrees']});")
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
