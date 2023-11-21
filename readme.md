# Cinema Reservation System

## Overview

This project implements a comprehensive cinema reservation system, integrating a Tkinter graphical interface with a Flask API. Users can interactively select movies, visualize seat layouts, and make real-time reservations. The system includes a virtual assistant, supports user account creation, and login for booking functionality.

## Features

- **Tkinter GUI:** User-friendly interface for movie selection, seat layout visualization, and reservation creation.
- **Flask API:** Manages backend operations, including movie data, seat availability, reservations, and user authentication.
- **Real-time Updates:** Provides dynamic updates on seat availability as reservations are made.
- **Virtual Assistant:** Assists users during the reservation process, providing movie information and answering frequently asked questions.
- **User Authentication:** Supports user account creation and login for secure reservation processes.

## Technical Details

- **Frontend:** Developed using Tkinter (Python's standard GUI package).
- **Backend:** Powered by Flask, handling API endpoints for movie data, reservations, and user management.
- **Authentication:** Utilizes Flask-Login for secure user login and session management.
- **Communication:** JSON format for seamless data exchange between Tkinter and Flask.
- **Security:** Implements session-based authentication for user login and reservations.

## Getting Started

1. Clone the repository:
   ```bash
   git clone https://github.com/EuricoSantos-936/cine-reservation-API-Flask-Tkinter

2. Install dependencies:
   ```bash
    pip install -r requirements.txt
    
3. Run the Flask API:
    ```bash
    cd api
    flask run
4. Launch the Tkinter interface:
    ```bash
    cd gui
    python main.py

## Contributing

Contributions are welcome! If you find any issues or have suggestions, please open an issue or submit a pull request.



