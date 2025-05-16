from flask import Flask, request, jsonify

import json
import os

app = Flask(__name__)
DB_FILE = 'quizzes.json'

# Helper to load quizzes from the file
def load_quizzes():
    if not os.path.exists(DB_FILE):
        return {}
    with open(DB_FILE, 'r') as f:
        return json.load(f)
    

# Helper to save quizzes to the file
def save_quizzes(quizzes):
    with open(DB_FILE, 'w') as f:
        json.dump(quizzes, f, indent=4)


# Create a new quiz
@app.route('/quizzes', methods=['POST'])
def create_quiz():
    data = request.get_json()
    quizzes = load_quizzes()

    if 'pin' not in data or 'name' not in data or 'questions' not in data:
        return jsonify({'error': 'Invalid quiz data'}), 400
    
    quizzes[data['pin']] = data
    save_quizzes(quizzes)
    return jsonify({'message': 'Quiz created successfully'}), 201


# Retrieve a quiz by PIN
@app.route('/quizzes/<pin>', methods=['GET'])
def get_quiz(pin):
    quizzes = load_quizzes()
    quiz = quizzes.get(pin)

    if quiz:
        return jsonify(quiz), 200
    return jsonify({'error': 'Quiz not found'}), 404


# Delete a quiz by PIN
@app.route('/quizzes/<pin>', methods=['DELETE'])
def delete_quiz(pin):
    quizzes = load_quizzes()

    if pin in quizzes:
        del quizzes[pin]
        save_quizzes(quizzes)
        return jsonify({'message': 'Quiz deleted successfully'}), 200
    return jsonify({'error': 'Quiz not found'}), 404


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=10000)
