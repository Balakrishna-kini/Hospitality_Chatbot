# Hospitality Chatbot using Gemini API

## Overview

This is an AI-powered **hospitality chatbot** built using **Flask** and **Google Gemini API**. The chatbot acts as a virtual concierge for a hotel, helping guests with bookings, inquiries about hotel services, and providing booking history. It supports session-based chat history and smart intent detection.

## Features

- **Hotel Information Inquiry**: Provides details about amenities, room types, dining options, and more.
- **Booking System**: Allows users to book rooms and retrieve booking history.
- **Chat History**: Maintains user conversation history within the session.
- **Intent Detection**: Detects user intent for booking, inquiries, and chat history retrieval.
- **Google Gemini API Integration**: Uses advanced AI responses for general inquiries.

## Tech Stack

- **Frontend**: HTML, CSS, JavaScript
- **Backend**: Flask (Python)
- **Database**: Session-based (Filesystem)
- **AI Model**: Google Gemini API

## Installation

### Prerequisites

Ensure you have the following installed:

- Python 3.x
- Flask (`pip install flask`)
- Flask-Session (`pip install flask-session`)

### Steps to Run

1. Clone the repository:
   ```sh
   git clone https://github.com/your-username/hospitality-chatbot.git
   cd hospitality-chatbot
   ```
2. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```
3. Set up the **Google Gemini API Key**:
   ```sh
   export GEMINI_API_KEY='your-api-key-here'
   ```
4. Run the application:
   ```sh
   python app.py
   ```
5. Open the chatbot in your browser:
   ```
   http://127.0.0.1:5000/
   ```

## File Structure

```
📂 hospitality-chatbot
│── app.py                 # Main Flask application
│── hotel_info.py          # Hotel details and policies
│── templates/
│   └── index.html         # Frontend chatbot UI
│── static/
│   ├── style.css          # CSS styling (if separate)
│── requirements.txt       # Python dependencies
│── README.md              # Project documentation
```

## Usage

- Open the chatbot in a browser and ask questions about hotel services.
- Type booking details to make a reservation.
- Ask for your booking history or chat history.

## Contributing

Contributions are welcome! Feel free to submit pull requests or open issues.

## License

This project is licensed under the MIT License.


---



