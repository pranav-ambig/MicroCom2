from flask import Flask, request, jsonify
from flask_cors import CORS

from bson import ObjectId
import bcrypt
from model import user_collection


app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# in '/' path print hi on the screen 
@app.route('/')
def home():
    return "Hi"


@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    user = user_collection.find_one({'email': email})

    if user:
        # Verify password
        if bcrypt.checkpw(password.encode('utf-8'), user['password']):
            return jsonify({'message': 'Login successful :)', 'userID': str(user['_id'])})  # Include user's _id in the response
        else:
            return jsonify({'message': 'Invalid email or password'}), 401
    else:
        return jsonify({'message': 'Invalid email or password'}), 401

@app.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    name = data.get('name')
    age = data.get('age')
    email = data.get('email')
    password = data.get('password')
    ph = data.get('ph')
    address = data.get('address')


    # Hash password
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    # Check if email already exists
    if user_collection.find_one({'email': email}):
        return jsonify({'message': 'Email already exists'}), 400

    # Insert new user
    user_id = user_collection.insert_one({'name': name, 'age' : age ,'email': email, 'password': hashed_password, 'ph.no': ph, 'address': address}).inserted_id

    return jsonify({'message': 'Signup successful', 'user_id': str(user_id)}), 201


if __name__ == '__main__':
    app.run(debug=True, port=9000, host = '0.0.0.0')
