# script2.py
from interpreter import interpreter
import os

def generate_plantuml():
    interpreter.offline = True
    interpreter.llm.model = "ollama/llama3:8B"
    interpreter.llm.api_base = "http://localhost:11434"
    
    response = interpreter.chat("你是一个能生成 PlantUML 代码的智能助手。"
                             "能力：能够根据输入的描述准确生成 PlantUML 代码，并以文本文件形式提供。"
                             "知识储备：精通 PlantUML 语法及各类图形绘制规则。"
                             "请根据以下描述生成 PlantUML 代码，"
                             "以文本形式输出：(包含学生、教师、课程、班级、选课记录、成绩、考勤等七个对象的学生管理系统)的PlantUML代码，保存位置C:\PlantUML\plantuml_graphviz_word2019_template_win64\estuml.txt"
                             "1.只调用os的python包，2.将PlantUML代码在python代码中作为文本写入txt文件",
                             return_messages=True)
    
    save_path = r"C:\PlantUML\plantuml_graphviz_word2019_template_win64\estuml.txt"
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    
    with open(save_path, 'w', encoding='utf-8') as f:
        f.write(response[-1]['content'])
    
    return f"PlantUML代码已成功生成并保存到 {save_path}\n\n生成的代码内容：\n{response[-1]['content']}"

if __name__ == "__main__":
    result = generate_plantuml()
    print(result)
