# Real-Time Individual Chat Application

This is a real-time one-to-one chat application built using Django and Django Channels.


# Setup Steps

1. Clone the repository:

   git clone <your-repository-link>
   cd chat_app

2. Create a virtual environment:

   python -m venv env
   env\Scripts\activate


3. Install required packages:

   pip install django channels daphne

4. Apply database migrations:

   python manage.py makemigrations
   python manage.py migrate


# Installation Instructions

Python version 3.9 or above.

Install dependencies:

   pip install django channels daphne


# How to Run the Project

1. Start the development server:

   python manage.py runserver

2. Open browser and go to:

   http://127.0.0.1:8000/

3. Register two users and start chatting.

