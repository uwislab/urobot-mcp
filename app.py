from flask import Flask, request, jsonify, render_template
import ollama
import subprocess

# 初始化Flask应用
app = Flask(__name__)

# 首页路由
@app.route('/')
def index():
    """
    处理根路径请求，返回首页模板
    Returns:
        HTML: 渲染后的index.html模板
    """
    return render_template('index.html')

@app.route('/call_ollama', methods=['POST'])
def call_ollama():
    """
    处理Ollama API调用请求
    Returns:
        JSON: 包含AI响应结果或错误信息
    """
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
        return jsonify({"result": response["message"]["content"]})
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
    return render_template('new_page.html')

@app.route('/run_script3', methods=['POST'])
def run_script3():
    """
    处理C代码生成请求
    Returns:
        JSON: 包含生成结果或错误信息
    """
    try:
        # 动态导入script3模块
        from script3 import generate_c_code
        # 调用生成函数
        output = generate_c_code()
        return jsonify({
            'message': output,
            'error': ''
        })
    except Exception as e:
        # 处理异常情况
        return jsonify({
            'error': str(e),
            'message': ''
        }), 500

@app.route('/run_script4', methods=['POST'])
def run_script4():
    """
      处理PlantUML代码生成请求
       Returns:JSON: 包含生成结果或错误信息
    """
    try:
        # 动态导入script4模块
        from script4 import generate_plantuml
        # 调用生成函数
        output = generate_plantuml()
        return jsonify({
            'message': output,
            'error': ''
        })
    except Exception as e:
        # 处理异常情况
        return jsonify({
            'error': str(e),
            'message': ''
        }), 500

# 主程序入口
if __name__ == '__main__':
    # 启动Flask开发服务器
    app.run(debug=True)
