import os
import logging
from typing import Dict, Any, Optional
from interpreter import interpreter

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def generate_c_code(user_prompt: Optional[str] = None) -> str:
    # 参数验证
    if user_prompt is not None and not isinstance(user_prompt, str):
        logger.error(f"无效的用户提示词类型: {type(user_prompt)}")
        raise ValueError("user_prompt必须是字符串或None")
        
    # 记录调试信息
    logger.debug(f"生成C代码请求参数 - 用户提示: {user_prompt}")
    """
    生成C语言代码的主函数
    功能说明:
    - 通过Ollama本地模型生成朴素贝叶斯算法的C语言实现代码
    - 自动将生成的代码保存到指定路径
    - 支持自定义用户提示
    参数:
        user_prompt (str, optional): 自定义生成提示，默认为None
    返回:
        str: 生成结果信息，包含保存路径和生成的代码内容
    异常:
        Exception: 生成或保存过程中出现的任何错误
        
    示例:
        >>> result = generate_c_code("实现一个快速排序算法")
        >>> print(result)
    """
    logger.info("开始生成C语言代码")
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
