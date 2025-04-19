# script2.py
import os

def generate_plantuml():
    """
    生成PlantUML代码的主函数
    通过Ollama生成学生管理系统的PlantUML代码
    并将生成的代码保存到本地文件
    
    Returns:
        str: 生成结果信息，包含保存路径和生成的代码内容
    """
    from interpreter import interpreter

    interpreter.offline = True
    interpreter.llm.model = "ollama/llama3:8B"
    interpreter.llm.api_base = "http://localhost:11434"

    try:
        # 调用Ollama生成代码
        response = interpreter.chat(
            "你是一个能生成 PlantUML 代码的智能助手。"
            "能力：能够根据输入的描述准确生成 PlantUML 代码，并以文本文件形式提供。"
            "知识储备：精通 PlantUML 语法及各类图形绘制规则。"
            "请根据以下描述生成 PlantUML 代码："
            "生成一个包含学生、教师、课程、班级、选课记录、成绩、考勤等七个对象的学生管理系统的PlantUML代码"
            "保存位置C:\PlantUML\plantuml_graphviz_word2019_template_win64\estuml.txt"
            "1.只调用os的python包，2.将PlantUML代码在python代码中作为文本写入txt文件"
        )
        
        # 获取生成的代码
        code = response[-1]['content'] if response else ""

        # 保存生成的代码到文件
        save_path = r"C:\PlantUML\plantuml_graphviz_word2019_template_win64\estuml.txt"
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        
        with open(save_path, 'w', encoding='utf-8') as f:
            f.write(code)
        
        return f"PlantUML代码已成功生成并保存到 {save_path}\n\n生成的代码内容：\n{code}"
        
    except Exception as e:
        return f"生成PlantUML代码时出错: {str(e)}"

if __name__ == "__main__":
    result = generate_plantuml()
    print(result)
