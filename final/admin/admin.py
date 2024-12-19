from flask import Flask, request, jsonify, render_template
import json
import os

app = Flask(__name__)

# Load the initial dataset (use a file for persistence if needed)
data_file = os.path.join(os.path.dirname(__file__), '../backend/fineTune/data.json')
try:
    with open(data_file, 'r') as file:
        dataset = json.load(file)
except FileNotFoundError:
    dataset = []

# Home route to display the form
@app.route('/')
def home():
    return render_template('index.html')

# API endpoint to add new data
@app.route('/add', methods=['POST'])
def add_data():
    try:
        prompt = request.form.get('prompt')
        completion = request.form.get('completion')
        tags = request.form.get('tags')

        if not prompt or not completion or not tags:
            return jsonify({'error': 'All fields are required.'}), 400

        # Add the new entry to the dataset
        new_entry = {
            "prompt": prompt,
            "completion": completion,
            "tags": tags
        }
        dataset.append(new_entry)

        # Save the dataset to a file for persistence
        with open(data_file, 'w') as file:
            json.dump(dataset, file, indent=4)

        return jsonify({'message': 'Entry added successfully!', 'entry': new_entry}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# API endpoint to view all data
@app.route('/data', methods=['GET'])
def get_data():
    return jsonify(dataset), 200

if __name__ == '__main__':
    app.run(debug=True)