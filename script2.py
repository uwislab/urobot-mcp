# script2.py
import os
import logging
from typing import Dict, Any, Optional
from interpreter import interpreter

# 配置日志
log_dir = "logs"
os.makedirs(log_dir, exist_ok=True)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(os.path.join(log_dir, 'script2.log')),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def generate_plantuml(user_prompt: Optional[str] = None) -> str:
    """
    生成PlantUML代码的主函数
    
    详细功能说明:
    - 通过Ollama本地模型生成PlantUML代码
    - 自动将生成的代码保存到指定路径
    - 支持自定义用户提示
    - 提供完整的错误处理和日志记录
    
    参数:
        user_prompt (Optional[str]): 用户自定义的生成提示，默认为None
        
    返回:
        str: 生成结果信息，包含:
            - 保存路径
            - 生成的代码内容
            或错误信息
            
    异常:
        ValueError: 当user_prompt不是字符串或None时
        Exception: 生成或保存过程中出现的其他错误
        
    示例:
        >>> result = generate_plantuml("生成学生管理系统类图")
        >>> print(result)
    """
    # 参数验证
    if user_prompt is not None and not isinstance(user_prompt, str):
        logger.error(f"无效的用户提示词类型: {type(user_prompt)}")
        raise ValueError("user_prompt必须是字符串或None")
        
    logger.info("开始PlantUML代码生成流程")
    logger.debug(f"用户提示词: {user_prompt}")
    from interpreter import interpreter

    interpreter.offline = True
    interpreter.llm.model = "ollama/llama3:8B"
    interpreter.llm.api_base = "http://localhost:11434"

    try:
        # 调用Ollama生成代码
        # 确保没有超时限制的调用  
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
