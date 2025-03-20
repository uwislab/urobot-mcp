import requests
import os

DEEPSEEK_API_KEY = "sk-a20ac497a8e64fa2837236671064394d"
DEEPSEEK_API_URL = "https://api.deepseek.com/v1/chat/completions"

def generate_plantuml():
    headers = {
        "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
        "Content-Type": "application/json"
    }
    
    prompt = ("你是一个能生成 PlantUML 代码的智能助手。"
             "能力：能够根据输入的描述准确生成 PlantUML 代码，并以文本文件形式提供。"
             "知识储备：精通 PlantUML 语法及各类图形绘制规则。"
             "请根据以下描述生成 PlantUML 代码："
             "生成一个包含学生、教师、课程、班级、选课记录、成绩、考勤等七个对象的学生管理系统的PlantUML代码")
    
    data = {
        "model": "deepseek-coder",
        "messages": [{
            "role": "user",
            "content": prompt
        }],
        "temperature": 0.7,
        "max_tokens": 2048
    }
    
    try:
        response = requests.post(DEEPSEEK_API_URL, json=data, headers=headers)
        response.raise_for_status()
        result = response.json()
        
        if 'choices' in result and len(result['choices']) > 0:
            plantuml_code = result['choices'][0]['message']['content']
            
            # Save the generated code
            save_path = r"C:\PlantUML\plantuml_graphviz_word2019_template_win64\estuml.txt"
            os.makedirs(os.path.dirname(save_path), exist_ok=True)
            
            with open(save_path, 'w', encoding='utf-8') as f:
                f.write(plantuml_code)
            
            return f"PlantUML代码已成功生成并保存到 {save_path}\n\n生成的代码内容：\n{plantuml_code}"
        else:
            return "未能成功生成PlantUML代码"
            
    except Exception as e:
        return f"生成PlantUML代码时出错: {str(e)}"

if __name__ == "__main__":
    result = generate_plantuml()
    print(result)
