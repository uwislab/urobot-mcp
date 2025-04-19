import requests
import os

# Deepseek API 配置
DEEPSEEK_API_KEY = "sk-a20ac497a8e64fa2837236671064394d"
DEEPSEEK_API_URL = "https://api.deepseek.com/v1/chat/completions"

def gen_c_code(user_prompt=None):
    """
    生成C语言代码的主函数
    通过Deepseek API生成朴素贝叶斯算法的C语言实现代码
    并将生成的代码保存到本地文件
    
    Returns:
        str: 生成结果信息，包含保存路径和生成的代码内容
    """
    # 设置API请求头
    headers = {
        "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
        "Content-Type": "application/json"
    }
    
    # 构造生成C代码的提示词
    prompt = ("你是一个能生成 C 语言程序的智能助手。"
             "请根据以下需求生成 C 语言代码："
             f"{user_prompt if user_prompt else '实现一个朴素贝叶斯算法'}"
             "并将生成的代码保存到本地文件。")
    
    # 构造API请求数据
    data = {
        "model": "deepseek-coder",  # 使用deepseek-coder模型
        "messages": [{
            "role": "user",
            "content": prompt
        }],
        "temperature": 0.7,  # 控制生成结果的随机性
        "max_tokens": 2048  # 限制生成的最大token数
    }
    
    try:
        # 发送API请求
        response = requests.post(DEEPSEEK_API_URL, json=data, headers=headers)
        response.raise_for_status()  # 检查HTTP错误
        result = response.json()  # 解析JSON响应
        
        # 检查并处理API响应
        if 'choices' in result and len(result['choices']) > 0:
            code = result['choices'][0]['message']['content']  # 提取生成的代码
            
            # 保存生成的代码到文件
            save_path = r"C:\PlantUML\plantuml_graphviz_word2019_template_win64\sort.c"
            os.makedirs(os.path.dirname(save_path), exist_ok=True)  # 创建目录（如果不存在）
            
            # 写入文件
            with open(save_path, 'w', encoding='utf-8') as f:
                f.write(code)
            
            # 返回成功信息
            return f"代码已成功生成并保存到 {save_path}\n\n生成的代码内容：\n{code}"
        else:
            return "未能成功生成代码"
            
    except Exception as e:
        # 处理异常情况
        return f"生成代码时出错: {str(e)}"

if __name__ == "__main__":
    result = gen_c_code()
    print(result)
