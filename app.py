from flask import Flask, request, jsonify,render_template
import re
from collections import Counter
import numpy as np

app = Flask(__name__)

# Define intents and responses
intents = {
    'greeting': {
        'patterns': ['hello', 'hi', 'hey'],
        'response': "Hello! How can I assist you?"
    },
    'farewell': {
        'patterns': ['bye', 'goodbye'],
        'response': "Goodbye! Have a great day."
    }
    # Add more intents and responses as needed
}

# Function to find the most similar intent based on user input
def find_most_similar_intent(user_input):
    max_similarity = -1
    most_similar_intent = None

    for intent, data in intents.items():
        for pattern in data['patterns']:
            similarity = compute_similarity(user_input, pattern)
            if similarity > max_similarity:
                max_similarity = similarity
                most_similar_intent = intent

    return most_similar_intent if max_similarity > 0 else None

# Function to compute similarity between two strings using cosine similarity of word counts
def compute_similarity(input_sentence, pattern):
    input_tokens = preprocess_text(input_sentence)
    pattern_tokens = preprocess_text(pattern)

    # Compute cosine similarity of word counts
    input_counts = Counter(input_tokens)
    pattern_counts = Counter(pattern_tokens)

    intersection = set(input_counts.keys()) & set(pattern_counts.keys())
    numerator = sum([input_counts[x] * pattern_counts[x] for x in intersection])

    input_norm = sum([input_counts[x]**2 for x in input_counts.keys()])
    pattern_norm = sum([pattern_counts[x]**2 for x in pattern_counts.keys()])
    denominator = np.sqrt(input_norm) * np.sqrt(pattern_norm)

    if not denominator:
        return 0.0
    else:
        return float(numerator) / denominator

# Function to preprocess text (lowercase and tokenize)
def preprocess_text(text):
    tokens = re.findall(r'\b\w+\b', text.lower())
    return tokens

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json.get('user_input', '').strip().lower()
    if not user_input:
        return jsonify({'response': "Please provide 'user_input' in the request."}), 400

    intent = find_most_similar_intent(user_input)

    if intent:
        response = intents[intent]['response']
    else:
        response = "I'm not sure how to respond to that."

    return jsonify({'response': response})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
