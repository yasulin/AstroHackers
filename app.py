from flask import Flask, jsonify, render_template
import openai
import os
import random

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
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": "You are the smartest astrophysicist and the most intelligent aerospace engineer in the world."
                },
                {
                    "role": "user",
                    "content":
                        "Generate a random space quiz question related to solar system, galaxy, astrophysics, rockets, satellites and four possible answers."\

                        f"RandomSeed: {seed}"\
                        "The format of the response must be as follows and do not include titles:"\
                        """
                        <question>\nA) <answer 1>\nB) <answer 2>\nC) <answer 3>\nD) <answer 4>\n<correct answer>\n<description>
                        """
                        "The <description> must be within 200 words that is conclusive in one paragraph ."\
                }
            ],
            max_tokens=300,
            temperature=0.9,
            top_p=0.95
        )
        quiz_text = response.choices[0].message['content'].strip()
        quiz = parse_quiz(quiz_text)
        return jsonify({"quiz": quiz, "seed": seed})
    except Exception as e:
        return f"Error generating quiz: {e}"

def parse_quiz(text):
    lines = text.split('\n')
    question = lines[0].rstrip()
    answers = [s.rstrip() for s in lines[1:5]]
    correct_answer = lines[5].split(')')[0].rstrip()
    description = lines[-1]
    return {
        "question": question,
        "answers": answers,
        "correct_answer": correct_answer,
        "description": description,
        "whole_text": text
    }

@app.route('/debug/')
def debug():
    return f"OpenAI API Key: {os.getenv('OPENAI_API_KEY')}"

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
