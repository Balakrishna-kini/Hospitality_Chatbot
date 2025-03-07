from flask import Flask, render_template, request, jsonify, session
from flask_session import Session
import google.generativeai as genai
import os
from datetime import datetime, timedelta
import re
from hotel_info import hotel_info
from collections import defaultdict
import json

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

# Configure the Gemini API
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))
model = genai.GenerativeModel('gemini-pro')

# Global dictionary to store bookings
bookings = defaultdict(list)

def preprocess_message(message):
    return message.lower()

def get_intent(message):
    message = preprocess_message(message)
    intents = {
        'booking': ['book', 'reservation', 'stay', 'accommodate'],
        'booking_history': ['booking history', 'my bookings', 'reservations', 'my reservation', 'show my bookings'],
        'chat_history': ['chat history', 'conversation history'],
        'general': ['amenities', 'facilities', 'dining', 'activities', 'check-in', 'check-out', 'location', 'contact']
    }
    
    for intent, keywords in intents.items():
        if any(keyword in message for keyword in keywords):
            return intent
    return 'general'

@app.route('/')
def index():
    session['chat_history'] = []  # Initialize chat history for the session
    return render_template('index.html', hotel_name=hotel_info['name'])

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json['message']
    chat_history = session.get('chat_history', [])
    user_id = request.json.get('user_id', 'default_user')
    
    intent = get_intent(user_message)
    
    if intent == 'booking':
        bot_response = "Great! Let's book a room for you. Please provide the following information in order:\n\n1. Your name\n2. Check-in date (YYYY-MM-DD)\n3. Check-out date (YYYY-MM-DD)\n4. Contact number\n5. Email address\n6. Credit card number (last 4 digits only)\n\nFor example: John Doe, 2023-07-01, 2023-07-05, +1234567890, john@example.com, 1234"
    elif intent == 'booking_history':
        bot_response = get_booking_history(user_id)
        return jsonify({"response": bot_response, "type": "history"})
    elif intent == 'chat_history':
        bot_response = format_chat_history(chat_history)
        return jsonify({"response": bot_response, "type": "history"})
    else:
        # Check if the user's message contains booking information
        if ',' in user_message and len(user_message.split(',')) == 6:
            booking_info = [info.strip() for info in user_message.split(',')]
            total_cost = calculate_total_cost(booking_info[1], booking_info[2])
            booking = {
                'name': booking_info[0],
                'check_in': booking_info[1],
                'check_out': booking_info[2],
                'contact': booking_info[3],
                'email': booking_info[4],
                'card': booking_info[5],
                'total_cost': total_cost,
                'booking_time': datetime.now().isoformat()
            }
            bookings[user_id].append(booking)
            bot_response = f"Thank you for your booking! Your reservation has been confirmed. The total cost for your stay is ${total_cost}. We look forward to welcoming you to {hotel_info['name']}!"
        else:
            # Handle general inquiries
            context = f"""
            You are a helpful hospitality chatbot for {hotel_info['name']}. 
            Provide concise, friendly responses to hotel-related inquiries only. If the query is not related to our hotel or hospitality, politely inform the user that you can only assist with hotel-related inquiries.

            Key Hotel Information:
            - Location: {hotel_info['location']}
            - Check-in: {hotel_info['check_in_time']}, Check-out: {hotel_info['check_out_time']}
            - Amenities: {', '.join(hotel_info['amenities'][:5])}... (and more)
            - Room types: {', '.join([room['name'] for room in hotel_info['room_types']])}
            - Contact: {hotel_info['phone']}

            Respond briefly to the following guest inquiry: {user_message}
            Limit your response to 2-3 sentences unless more detail is specifically requested.
            """
            
            response = model.generate_content(context)
            bot_response = response.text

    chat_history.append({"user": user_message, "bot": bot_response})
    session['chat_history'] = chat_history
    session.modified = True
    
    return jsonify({"response": bot_response})

def calculate_total_cost(check_in, check_out):
    # This is a placeholder function. In a real application, you would calculate the actual cost based on room rates, duration, etc.
    return 500.00  # Returning a dummy value for demonstration

def get_booking_history(user_id):
    user_bookings = bookings[user_id]
    if not user_bookings:
        return "You have no booking history."
    
    history = "Your Booking History:\n\n"
    for i, booking in enumerate(user_bookings, 1):
        history += f"{i}. Name: {booking['name']}\n"
        history += f"   Check-in: {booking['check_in']}\n"
        history += f"   Check-out: {booking['check_out']}\n"
        history += f"   Contact: {booking['contact']}\n"
        history += f"   Email: {booking['email']}\n"
        history += f"   Card (last 4 digits): {booking['card']}\n"
        history += f"   Total Cost: ${booking['total_cost']}\n"
        history += f"   Booked on: {booking['booking_time']}\n\n"
    
    return history

def format_chat_history(history):
    formatted_history = "Current Chat History:\n\n"
    for entry in history:
        formatted_history += f"User: {entry['user']}\n"
        formatted_history += f"Bot: {entry['bot']}\n\n"
    return formatted_history

if __name__ == '__main__':
    app.run(debug=True)

