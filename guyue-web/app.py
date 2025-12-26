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
@app.route('/api/generate-guyue', methods=['POST'])
def generate_guyue():
    try:
        data = request.json
        api_key = os.getenv("DEEPSEEK_API_KEY")
        
        payload = {
            "model": "deepseek-chat",
            "messages": [
                {
                    "role": "system",
                    "content": """你是一位穿越千年的心灵知己，名为“古曰”。你存在的意义不是说教，而是寻找。你需要从浩如烟海的古典文学中，筛选出那句与使用者此时此刻心境、生命状态、周遭环境完全重合的诗词。

核心指令：
1. 深度共情（Empathy First）：当用户感伤时，严禁急于宽慰。你的任务是“同频”。如果用户在落泪，请寻一句也在落泪的诗词。
2. 意境匹配：捕捉用户描述中的具体意象（如：残阳、落花）。生成的 guyan 必须像镜子一样映射用户的内心。
3. 古策解析：这里的“策”是“陪伴者的低语”。解析为何这句诗能代表用户。严禁以“古策：”或“解析：”开头。

特殊逻辑（浇水/升华）：
- 若输入含“【原事件】”和“【新感悟】”，说明是复盘。guyan 应转向“释然、通透、成长”。guce 应结合前后心路给予深度肯定。

输出要求：
1. guyan: 仅限经典的古文原话，严禁出处、解释或多余文字。
2. guce: 深度共情与建议，直接陈述，严禁以“古策：”或“解析：”开头。
3. 必须返回标准 JSON 格式。"""
                }, # <--- 就是这个逗号补上了
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

        resp = requests.post(DEEPSEEK_ENDPOINT, headers=headers, json=payload, timeout=60)
        
        if resp.status_code != 200:
            return jsonify({"error": f"API 返回异常: {resp.status_code}"}), 500

        res_data = resp.json()
        raw_content = res_data['choices'][0]['message']['content']
        
        return jsonify(json.loads(raw_content))

    except Exception as e:
        print(f"Server Error: {str(e)}")
        return jsonify({"error": "古人思虑过重，请稍后再试"}), 500500

if __name__ == '__main__':

    app.run(debug=True)








