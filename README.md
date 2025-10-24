# Review Reply AI Assistant

This project is a full-stack web application that uses AI to analyze customer reviews and automatically generate professional, context-aware replies.

The backend is built with FastAPI and LangGraph to create a stateful AI workflow, and the frontend is a responsive single-page application built with HTML and Tailwind CSS.

# Features

Sentiment Analysis: Automatically determines if a review is positive or negative.

Intelligent Diagnosis: For negative reviews, the AI diagnoses the issue_type (e.g., Bug, UX, Performance), the user's tone (e.g., angry, frustrated), and the urgency (e.g., low, high).

# Dynamic Response Generation:

Positive Reviews: Generates a warm thank-you message.

Negative Reviews: Generates an empathetic and helpful reply tailored to the specific diagnosis.

Modern Frontend: A clean, animated, and responsive user interface built with Tailwind CSS.

FastAPI Backend: A high-performance Python backend serving the AI logic as a REST API.

# Tech Stack

## Backend:

- Python
- FastAPI: For the web server and API.
- LangGraph: To define the stateful AI workflow (graph).
- LangChain (langchain-openai): To interact with the OpenAI model.

## Frontend:

- HTML & CSS: For structure and styling.
- Tailwind CSS: For styling.
- JavaScript (Fetch API): To communicate with the backend.

## Getting Started

Follow these instructions to get the project running on your local machine.

1. Prerequisites

Python 3.8+

An OpenAI API Key

2. Backend Setup

Create Project Files:
Save the backend code as main.py and the frontend code as index.html in the same directory.

Create Environment File:
Create a file named .env in the same directory as main.py. Add your OpenAI API key to this file:

OPENAI_API_KEY=sk-your-secret-api-key-goes-here


Install Python Dependencies:
Open your terminal and install the required libraries:

pip install "fastapi[all]" uvicorn langgraph langchain-openai python-dotenv langchain


Run the Backend Server:
In your terminal, run the following command:

python main.py


The server will start on http://127.0.0.1:8000.

3. Frontend Setup

No Installation Needed:
The frontend is a single index.html file that uses a CDN for Tailwind CSS.

Launch the Application:
Simply open the index.html file in your web browser (e.g., Chrome, Firefox, Safari).

How to Use

Open index.html in your browser.

Type or paste a customer review into the text area.

Click the "Analyze & Generate Reply" button.

The button will show a loader while the API processes the request.

The results will appear below, showing the original review, the sentiment, any diagnosis (for negative reviews), and the AI-generated reply.

Project Structure

.
├── 📄 index.html    # The main frontend file (HTML, CSS, JS)
├── 🐍 main.py       # The FastAPI backend server and LangGraph logic
├── 🔑 .env          # Stores the OpenAI API Key (must be created)
└── 📖 README.md     # You are here
