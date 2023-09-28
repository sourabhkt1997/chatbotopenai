from flask import Flask, request, jsonify
import openai
from flask_cors import CORS 
from dotenv import load_dotenv
load_dotenv()
import os
openai.api_key = os.getenv("OPENAI_API_KEY")
mongourl=os.getenv("mongourl")
from mongoengine import connect
# Configure the default database connection
connect(
    db='chatbot',
    host=mongourl,
    alias='default',  # Optional: Give the connection an alias
)

# from db import db
from models.usermodel import User


app = Flask(__name__)
CORS(app)


@app.route("/register",methods=["POST"])
def create_user():
    data = request.get_json()
    if 'username' in data and 'password' in data and 'email' in data:
        username = data['username']
        password = data['password']
        email=data['email']
    
        # Check if a user with the provided email already exists
        existing_user = User.objects(email=email).first()

        if existing_user:
            return jsonify({"message": "User already exists"})
        else:
            # Create a new user
            new_user = User(username=username, password=password, email=email)
            new_user.save()
            return jsonify({"message": "User created successfully"})

    return jsonify({"message": "Invalid request data"})


@app.route('/login',methods=['POST'])
def login():
     data = request.get_json()
     if 'password' in data and 'email' in data:
        password = data['password']
        email=data['email']
        
        # Retrieve the user with the provided email
        user = User.objects(email=email).first()
        print(user)
        if user:
            # Check if the password matches
            if user.password == password:
                return jsonify({"message":"Login successful","username":user["username"]
                })
            else:
                return jsonify({"message": "Incorrect password"})
        else:
            return jsonify({"message": "User not found"})

     return jsonify({"message": "Invalid request data"})





@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    if 'user_input' in data:
        user_input = data['user_input']

    # Define the conversation with user and assistant messages
    conversation = [
        {"role": "user", "content": user_input},
        {"role": "assistant", "content": "hello, how can i help you."},  # You can add a system message if needed
    ]

    # Generate a response from the chatbot
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=conversation,
        temperature=0.7,  # Adjust temperature for desired randomness
        max_tokens=1000,  # Adjust max_tokens for response length
    )

    # Extract the assistant's reply from the response
    assistant_reply = response['choices'][0]['message']['content']

    return jsonify({"response": assistant_reply})

if __name__ == '__main__':
    app.run(debug=True)
