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
                    "content": "You are the smartest astrophysicist and the most intelligent aerospace engineer in the world.."
                },
                {
                    "role": "user",
                    "content":
                        "Generate a random space quiz question related to solar system, galaxy, astrophysics, rockets, satellites and four possible answers."\
                        "Please provide the correct answer and the description of the answer in around 200 words."\
                        f"RandomSeed: {seed}"\
                        "The format of the response should be as follows and do not include titles:"\
                        "<question>"\
                        "A) <answer 1>"\
                        "B) <answer 2>"\
                        "C) <answer 3>"\
                        "D) <answer 4>"\
                        "<correct answer>"\
                        "<description>"
                }
            ],

            max_tokens=150,
            temperature=0.9,
            top_p=0.95

        )
        quiz_text = response.choices[0].message['content'].strip()
        quiz = parse_quiz(quiz_text)
        return jsonify({"quiz": quiz, "seed": seed})
    except Exception as e:
        # return jsonify({"error": "Error generating quiz"}), 500
        return f"Error generating quiz: {e}"

def parse_quiz(text):
    # Logic to parse quiz text (sample)
    lines = text.split('\n')
    question = lines[0]
    answers = lines[1:5]
    correct_answer = lines[-2]
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
