# E-Shop Project

This project is an e-commerce experimental platform for the SoftwareSecurity course.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

What things you need to install the software:


- Python 3.11.2
- PostgreSQL 13+ (psqlODBC)
- Node.js 12.x+
- pgAdmin 8.6
- Angular CLI


### Installing

#### Setting up the Backend (Django)

1. **Clone the repository:**

   `git clone https://github.com/ChrisDaskalos/e-shop_softsec.git`

   `cd e-shop_softsec`

2. **Set up a virtual environment:**

    `python -m venv venv`
    `source venv/bin/activate`  # On Windows use `venv\Scripts\activate`

3. **Install the required Python packages:**
   
    `pip install -r requirements.txt`

4. **Migrate the database:**

    `python manage.py migrate`

5. **Run the development server:**
   
   `python manage.py runserver`

6. **Run the ssl server:**

    `python manage.py runsslserver`



