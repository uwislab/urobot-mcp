from flask import Flask, request, jsonify, render_template
import ollama
import subprocess

app = Flask(__name__)

# 定义处理根路径的路由
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/call_ollama', methods=['POST'])
def call_ollama():
    try:
        data = request.get_json()
        prompt = data['prompt']
        model = data.get('model', 'llama3:8b')  # 默认使用llama3模型，可根据需求更改

        # 这里假设ollama.chat函数能正常工作，实际可能需要根据ollama库的正确用法调整
        response = ollama.chat(model=model, messages=[{"role": "user", "content": prompt}])
        return jsonify({"result": response["message"]["content"]})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/new_page')
def new_page():
    return render_template('new_page.html')

@app.route('/run_script', methods=['POST'])
def run_script():
    try:
        # 执行指定的Python脚本
        # Import and run the script directly instead of subprocess
        from script3 import generate_c_code
        output = generate_c_code()
        return jsonify({
            'message': output,
            'error': ''
        })
        return jsonify({
            'message': result.stdout,
            'error': result.stderr
        })
    except subprocess.CalledProcessError as e:
        return jsonify({
            'error': str(e),
            'message': e.stdout,
            'stderr': e.stderr
        }), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
