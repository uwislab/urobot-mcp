from markupsafe import escape
from flask import Flask, request, jsonify, render_template
import ollama
import subprocess
import logging
import time
from typing import Dict, Any, Union, Tuple

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# 初始化Flask应用
app = Flask(__name__)

# 定义API响应类型
ApiResponse = Dict[str, Union[str, Dict[str, str]]]

# 首页路由
@app.route('/')
def index():
    """
    处理根路径请求，返回首页模板
    
    功能说明:
    - 渲染并返回前端首页
    - 首页包含基本功能导航
    
    Returns:
        str: 渲染后的index.html模板内容
        
    Raises:
        TemplateNotFound: 如果模板文件不存在
    """
    logger.info("访问首页")
    return render_template('index.html')

@app.route('/call_ollama', methods=['POST'])
def call_ollama():
    """
    处理Ollama API调用请求
    
    详细说明:
    - 接收JSON格式的请求数据
    - 支持自定义模型选择
    - 提供完整的错误处理
    - 记录详细的请求日志
    
    请求参数:
        {
            "prompt": "用户提示词",
            "model": "可选模型名称" 
        }
        
    返回:
        JSON: {
            "result": "AI生成结果",
            "error": "错误信息(如果有)"
        }
    """
    logger.info("收到Ollama API调用请求")
    start_time = time.time()
    try:
        # 获取请求数据
        data = request.get_json()
        prompt = data['prompt']
        # 设置默认模型
        model = data.get('model', 'llama3:8b')
        
        # 调用Ollama API
        response = ollama.chat(
            model=model,
            messages=[{"role": "user", "content": prompt}]
        )
        
        # 返回AI响应内容
        execution_time = time.time() - start_time
        logger.info(f"Ollama请求处理完成，耗时: {execution_time:.2f}秒")
        return jsonify({
            "result": response["message"]["content"],
            "execution_time": execution_time
        })
    except Exception as e:
        # 处理异常情况
        return jsonify({"error": str(e)}), 500

@app.route('/new_page')
def new_page():
    """
    处理新页面请求，返回Deepseek功能页面
    Returns:
        HTML: 渲染后的new_page.html模板
    """
    return render_template('deepseek.html')

@app.route('/run_script1', methods=['POST'])
def run_script1():
    """
    处理C代码生成请求(script1)
    Returns:
        JSON: 包含生成结果或错误信息
    """
    try:
        from script1 import generate_c_code
        output = generate_c_code()
        return jsonify({
            'result': output,
            'error': ''
        })
    except Exception as e:
        return jsonify({
            'error': str(e),
            'result': ''
        }), 500

@app.route('/run_script2', methods=['POST'])
def run_script2():
    """
    处理PlantUML生成请求(script2)
    Returns:
        JSON: 包含生成结果或错误信息
    """
    try:
        from script2 import generate_plantuml
        output = generate_plantuml()
        return jsonify({
            'result': output,
            'error': ''
        })
    except Exception as e:
        return jsonify({
            'error': str(e),
            'result': ''
        }), 500

@app.route('/run_script3', methods=['POST'])
def run_script3():
    """
    处理C代码生成请求
    Returns:
        JSON: 包含生成结果或错误信息
    """
    try:
        # 获取用户输入
        data = request.get_json()
        user_prompt = data.get('prompt', '')
        
        # 动态导入script3模块
        from script3 import gen_c_code
        # 调用生成函数并传入用户提示
        output = gen_c_code(user_prompt)
        return jsonify({
            'result': output,  # 改为result以保持与前端一致
            'error': ''
        })
    except Exception as e:
        # 处理异常情况
        return jsonify({
            'error': str(e),
            'result': ''
        }), 500

@app.route('/run_script4', methods=['POST'])
def run_script4():
    """
    处理PlantUML生成请求
    Returns:
        JSON: 包含生成结果或错误信息
    """
    try:
        # 获取用户输入
        data = request.get_json()
        user_prompt = data.get('prompt', '')
        
        # 动态导入script4模块
        from script4 import gen_plantuml
        # 调用生成函数并传入用户提示
        output = gen_plantuml(user_prompt)
        return jsonify({
            'result': output,  # 改为result以保持与前端一致
            'error': ''
        })
    except Exception as e:
        # 处理异常情况
        return jsonify({
            'error': str(e),
            'result': ''
        }), 500
# 主程序入口
if __name__ == '__main__':
    # 开发环境配置，仅本地访问
    app.run(debug=True, host='127.0.0.1', port=5000)
