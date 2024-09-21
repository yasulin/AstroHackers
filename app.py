from flask import Flask, jsonify, render_template
import openai
import os

app = Flask(__name__)

# OpenAI API key from environment variable
openai.api_key = os.getenv('OPENAI_API_KEY')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get-quiz', methods=['GET'])
def get_quiz():
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": "Generate a space-related quiz question and four possible answers."}
            ],
            max_tokens=150
        )
        quiz_text = response.choices[0].message['content'].strip()
        quiz = parse_quiz(quiz_text)
        return jsonify(quiz)
    except Exception as e:
        print(f"Error generating quiz: {e}")
        # return jsonify({"error": "Error generating quiz"}), 500
        return f"Error generating quiz: {e}"

def parse_quiz(text):
    # Logic to parse quiz text (sample)
    lines = text.split('\n')
    question = lines[0]
    answers = lines[2:]
    return {
        "question": question,
        "answers": answers
    }

@app.route('/debug/')
def debug():
    return f"OpenAI API Key: {os.getenv('OPENAI_API_KEY')}"

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
