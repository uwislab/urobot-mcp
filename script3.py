import requests
import os

DEEPSEEK_API_KEY = "sk-a20ac497a8e64fa2837236671064394d"
DEEPSEEK_API_URL = "https://api.deepseek.com/v1/chat/completions"

def generate_c_code():
    headers = {
        "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
        "Content-Type": "application/json"
    }
    
    prompt = ("你是一个能生成 C 语言程序的智能助手。"
             "请根据以下需求生成 C 语言代码："
             "实现一个朴素贝叶斯算法，并将生成的代码保存到本地文件。")
    
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
            code = result['choices'][0]['message']['content']
            
            # Save the generated code
            save_path = r"C:\PlantUML\plantuml_graphviz_word2019_template_win64\sort.c"
            os.makedirs(os.path.dirname(save_path), exist_ok=True)
            
            with open(save_path, 'w', encoding='utf-8') as f:
                f.write(code)
            
            return f"代码已成功生成并保存到 {save_path}"
        else:
            return "未能成功生成代码"
            
    except Exception as e:
        return f"生成代码时出错: {str(e)}"

if __name__ == "__main__":
    result = generate_c_code()
    print(result)
