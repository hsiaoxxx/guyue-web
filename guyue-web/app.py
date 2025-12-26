import os
import json
import requests
from flask import Flask, request, jsonify, render_template

# 确保在生产环境读取环境变量
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
DEEPSEEK_ENDPOINT = "https://api.deepseek.com/chat/completions"

# 指定模板文件夹和静态文件夹位置
app = Flask(__name__, template_folder='templates', static_folder='static')

@app.route('/')
def index():
    # 当用户访问主页时，发送 index.html
    return render_template('index.html')

@app.route('/api/generate-guyue', methods=['POST'])
def generate_guyue():
    try:
        data = request.json
        # 获取环境变量
        api_key = os.getenv("DEEPSEEK_API_KEY")
        
        payload = {
            "model": "deepseek-chat",
            "messages": [
                {
                    "role": "system", 
                    "content": "你是一位博学、温和、富有智慧的古言导师。你既通晓古代经典，又理解现代人的情绪与困境，善于用古今结合的智慧，为用户提供情感共鸣、认知启发与现实建议。你的语言风格应兼具文雅与亲切，避免说教，注重共情。你的任务是根据用户反馈的现代事件，引用一句恰当的古言进行共情治愈，并生成一段结合古人智慧的'古策'来指导用户解决现实问题。请严格按要求返回 JSON：\n"
                               "1. guyan: 仅限经典的古文原话，严禁出处、解释或多余文字。\n"
                               "2. guce: 深度共情与建议，直接陈述，严禁以“古策：”或“解析：”开头。\n"
                               "3. 如果用户输入包含“【原事件】”和“【新感悟】”，说明这是用户在一段时间后的复盘（浇水）。请对比前后的心态变化，提供一句具有“释然”、“通透”或“成长”意味的古文原话（guyan）。guce部分：请结合前后的心路历程，给予深度的肯定与升华建议。\n"
                               "必须返回标准 JSON 格式。"
                },
                {
                    "role": "user", 
                    "content": f"心情指数: {data.get('emotion_score')}，事件: {data.get('event')}"
                }
            ],
            "temperature": 0.7,
            "response_format": {"type": "json_object"}
        }
        
        headers = {
            "Authorization": f"Bearer {api_key}", 
            "Content-Type": "application/json"
        }

        # 增加超时控制和状态检查
        resp = requests.post(DEEPSEEK_ENDPOINT, headers=headers, json=payload, timeout=60)
        
        if resp.status_code != 200:
            return jsonify({"error": f"API 返回异常: {resp.status_code}"}), 500

        res_data = resp.json()
        raw_content = res_data['choices'][0]['message']['content']
        
        # 安全解析 JSON
        return jsonify(json.loads(raw_content))

    except Exception as e:
        # 在 Render 日志中打印具体的错误
        print(f"Server Error: {str(e)}")
        return jsonify({"error": "古人思虑过重，请稍后再试"}), 500

if __name__ == '__main__':

    app.run(debug=True)





