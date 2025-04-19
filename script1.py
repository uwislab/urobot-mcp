import os

def generate_c_code():
    """
    生成C语言代码的主函数
    通过Ollama生成朴素贝叶斯算法的C语言实现代码
    并将生成的代码保存到本地文件
    
    Returns:
        str: 生成结果信息，包含保存路径和生成的代码内容
    """
    from interpreter import interpreter

    interpreter.offline = True
    interpreter.llm.model = "ollama/llama3:8b"
    interpreter.llm.api_base = "http://localhost:11434"

    try:
        # 调用Ollama生成代码
        response = interpreter.chat(
            "定位：一个能生成 C 语言程序的智能助手。"
            "能力：可以根据用户提供的需求准确生成相应的 C 语言代码，并以文本格式保存。"
            "知识储备：熟练掌握 C 语言的各种语法、数据结构、算法及标准库函数。"
            "请根据以下需求生成 C 语言代码："
            "实现一个朴素贝叶斯算法,使用python调用os包将生成的C语言代码作为文本保存到本地"
            "保存位置C:\PlantUML\plantuml_graphviz_word2019_template_win64\sort.c"
        )
        
        # 获取生成的代码
        code = response[-1]['content'] if response else ""

        # 保存生成的代码到文件
        save_path = r"C:\PlantUML\plantuml_graphviz_word2019_template_win64\sort.c"
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        
        with open(save_path, 'w', encoding='utf-8') as f:
            f.write(code)
        
        return f"代码已成功生成并保存到 {save_path}\n\n生成的代码内容：\n{code}"
        
    except Exception as e:
        return f"生成代码时出错: {str(e)}"

if __name__ == "__main__":
    result = generate_c_code()
    print(result)
