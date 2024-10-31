# Event Management System

An Event Management System built with Django that allows users to register, browse, and book events, while administrators can manage event listings, bookings, and users.

## Table of Contents
- [Project Overview](#project-overview)
- [Features](#features)
- [Technologies Used](#technologies-used)
- [Getting Started](#getting-started)
- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)

## Project Overview
This Event Management System simplifies the process of organizing and attending events. It provides a web interface for users to sign up, browse upcoming events, and book spots. Administrators have a dedicated dashboard to manage events and bookings, track user activity, and perform CRUD operations on event listings.

## Features
- **User Registration and Authentication**: Users can create accounts, log in, and reset passwords.
- **Event Browsing and Booking**: Users can view a list of upcoming events and book available spots.
- **Admin Dashboard**: Admin users can create, update, and delete events, and view all user bookings.
- **Payment Integration** (optional): Integrate with a payment gateway for event bookings.
- **Responsive Design**: The application is accessible on desktops, tablets, and mobile devices.

## Technologies Used
- **Backend**: Django (Python)
- **Frontend**: HTML, CSS, JavaScript (Bootstrap for responsive design)
- **Database**: SQLite (default; can be configured to use PostgreSQL or MySQL)
- **Authentication**: Django's built-in authentication system

## Getting Started

### Prerequisites
- Python 3.8+
- pip (Python package installer)
- Git

### Installation
1. **Clone the repository**:
```bash
git clone https://github.com/yourusername/event-management-system.git
cd event-management-system
```
2.__Create a virtual environment__:

  ```bash
  python -m venv env
  source env/bin/activate  # On Windows use `env\Scripts\activate`
  ```
3.**Install dependencies**:

```bash
pip install -r requirements.txt
```
4.__Run migrations__:
  ```bash
python manage.py migrate
```
5.__Create a superuser for accessing the admin dashboard__:

```bash
python manage.py createsuperuser
```
6.__Run the development server__:

  ```bash
  python manage.py runserver
```
Visit http://127.0.0.1:8000 in your browser to view the app.

## Usage
Admin Dashboard: After creating a superuser, log in to /admin to manage events and user bookings.
User Interface: Users can sign up, view events, and make bookings.
## Project Structure
event-management-system/
├── events/                     # Main application directory\
│   ├── migrations/             # Database migrations\
│   ├── templates/              # HTML templates\
│   ├── static/                 # Static files (CSS, JavaScript)\
│   ├── views.py                # Application views\
│   ├── models.py               # Application models\
│   └── urls.py                 # Application URLs\
├── event_management/           # Project settings\
├── requirements.txt            # Project dependencies\
├── manage.py                   # Django management script\
└── README.md                   # Project README\

Created by Your TejaNiduram. Feel free to reach out if you have any questions or suggestions!
