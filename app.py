from flask import Flask, jsonify, render_template
import openai
import os
import re
import random
import logging

app = Flask(__name__)

# OpenAI API key from environment variable
openai.api_key = os.getenv('OPENAI_API_KEY')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get-quiz', methods=['GET'])
def get_quiz():
    try:
        seed = random.randint(1000, 9999)
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini-2024-07-18",
            # messages=[
            #     {
            #         "role": "system",
            #         "content": "You are an aerospace engineer who wants to raise awareness about how satellite technologies are used in our daily lives on Earth."
            #     },
            #     {
            #         "role": "user",
            #         "content":
            #             "Generate a random quiz question about how satellite technology is used in various fields of daily life (e.g., time management, communications, observations, weather forecasting, land and ocean monitoring, security, surveillance, navigation, positioning, biological experiments, semiconductor manufacturing, medical production) or regarding issues related to satellites such as space debris. Provide four possible answers. Always provide with the choices with alphabet A, B, C, D."\
            #     }
            # ],
            messages=[
                {
                    "role": "system",
                    "content": "あなたは、衛星技術が地球上の日常生活にどのように使用されているかについて認識を高めたいと考えている航空宇宙技術者です。"
                },
                {
                    "role": "user",
                    "content":
                        "衛星技術が日常生活のさまざまな分野（例：時間管理、通信、観測、天気予報、陸地と海洋のモニタリング、"\
                        "セキュリティ、監視、ナビゲーション、位置測定、生物学的実験、半導体製造、医療生産）でどのように使用されているか、"\
                        "または、宇宙ゴミなどの衛星に関連する問題に関するランダムなクイズを一つだけ生成してください。四つの選択肢を提供してください。"\
                        "回答と正解は必ずアルファベットA, B, C, Dと内容をセットで提供してください。"\
                        "説明文は必ず200文字以内で提供してください。"\
                }
            ],
            max_tokens=500,
            temperature=0.9,
            top_p=0.95,
            response_format={
                "type": "json_schema",
                "json_schema": {
                    "name": "quiz_response",
                    "strict": True,
                    "schema": {
                        "type": "object",
                        "properties": {
                            "question": {"type": "string"},
                            "answers": {
                                "type": "array",
                                "items": {"type": "string"}
                            },
                            "correct_answer": {"type": "string"},
                            "description": {"type": "string"}
                        },
                        "required": ["question", "answers", "correct_answer", "description"],
                        "additionalProperties": False
                    }
                }
            }
        )

        return response.choices[0].message['content']

    except Exception as e:
        return f"Error generating quiz: {e}"

@app.route('/debug/')
def debug():
    return f"OpenAI API Key: {os.getenv('OPENAI_API_KEY')}"

if __name__ == '__main__':
    ### For Development
    # app.run(debug=True, host='0.0.0.0')

    ### For Production
    app.run()
