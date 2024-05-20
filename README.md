# E-Shop Project

This project is an e-commerce experimental platform for the SoftwareSecurity course.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

What things you need to install the software:


- Python 3.11.2
- PostgreSQL 13+ (psqlODBC)
- pgAdmin 8.6


### Installing

#### Setting up the Backend (Django)

1. **Clone the repository:**

   `git clone https://github.com/ChrisDaskalos/e-shop_softsec.git`

   `cd e-shop_softsec`

2. **Set up a virtual environment:**

    `python -m venv venv`
    `source venv/bin/activate`  
     
    **On Windows use:**
    `venv\Scripts\activate`

3. **Install the required Python packages:**
   
    `pip install -r requirements.txt`

5. **Migrate the database:**

    `python manage.py migrate`


5. **Run the ssl server:**
    Before running the SSL server, make sure you have SSL certificates placed in the ssl directory of your project.

    `python manage.py runsslserver`



