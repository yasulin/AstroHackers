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
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": "You are the smartest astrophysicist and the most intelligent aerospace engineer in the world.."
                },
                {
                    "role": "user",
                    "content": "Generate a random space quiz question related to solar system, galaxy, astrophysics, rockets or satellites and four possible answers. Please provide the correct answer in the list of answers at the end. The format of the response should be as follows: <question> /n A) <answer 1> /n B) <answer 2> /n C) <answer 3> /n D) <answer 4> /n <correct answer>"
                }
            ],
            max_tokens=150
        )
        quiz_text = response.choices[0].message['content'].strip()
        quiz = parse_quiz(quiz_text)
        return jsonify(quiz)
    except Exception as e:
        # return jsonify({"error": "Error generating quiz"}), 500
        return f"Error generating quiz: {e}"

def parse_quiz(text):
    # Logic to parse quiz text (sample)
    lines = text.split('\n')
    question = lines[0]
    answers = lines[1:5]

    correct_answer = lines[-1].split(':')[-1]
    return {
        "question": question,
        "answers": answers,
        "correct_answer": correct_answer,
        "whole_text": text
    }

@app.route('/debug/')
def debug():
    return f"OpenAI API Key: {os.getenv('OPENAI_API_KEY')}"

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
