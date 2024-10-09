from flask import Flask, request
from flask_cors import CORS
app = Flask(__name__)
CORS(app)  # This enables CORS on all routes

@app.route('/submit', methods=['POST'])
def handle_data():
    user_input = request.form['userInput']
    with open('received_data.txt', 'a') as file:
        file.write(user_input + '\n')
    # this return statement is technically a html file
    return f"<h1> Received and saved: {user_input} </h1>"

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')  