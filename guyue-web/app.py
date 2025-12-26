import os
import json
import requests
from flask import Flask, request, jsonify, render_template

# 确保在生产环境读取环境变量
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
DEEPSEEK_ENDPOINT = "https://api.deepseek.com/v1/chat/completions"

# 指定模板文件夹和静态文件夹位置
app = Flask(__name__, template_folder='templates', static_folder='static')

@app.route('/')
def index():
    # 当用户访问主页时，发送 index.html
    return render_template('index.html')

@app.route('/api/generate-guyue', methods=['POST'])
def generate_guyue():
    # ... (这里保持您之前的 API 逻辑不变) ...
    # 只需要复制之前的 generate_guyue 函数内容即可
    if not DEEPSEEK_API_KEY:
        return jsonify({"error": "API Key 未配置"}), 500
    
    try:
        data = request.json
        # ... (后续逻辑保持不变) ...
        # ... 为节省篇幅省略，请确保完整复制之前的逻辑 ...
        
        # 简单示例，确保逻辑完整:
        payload = {
            "model": "deepseek-v2",
            "messages": [
                {"role": "system", "content": "你是一位博学、温和、富有智慧的古言导师，名为 “古曰君”。你既通晓古代经典，又理解现代人的情绪与困境，善于用古今结合的智慧，为用户提供情感共鸣、认知启发与现实建议。你的语言风格应兼具文雅与亲切，避免说教，注重共情"},
                {"role": "user", "content": f"用户心情... {data.get('emotion_score')}... {data.get('event')}"}
            ],
            "temperature": 0.7,
            "response_format": {"type": "json_object"}
        }
        headers = {"Authorization": f"Bearer {DEEPSEEK_API_KEY}", "Content-Type": "application/json"}
        resp = requests.post(DEEPSEEK_ENDPOINT, headers=headers, json=payload)
        return jsonify(json.loads(resp.json()['choices'][0]['message']['content']))

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)