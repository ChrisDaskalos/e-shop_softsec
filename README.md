# E-Shop Project

This project is an e-commerce experimental platform for the Software Security course.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

Make sure you have the following software installed:

- Python 3.11.2
- PostgreSQL 13+
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


4. **Set up the database:**

    - Ensure PostgreSQL is running and create a database named `eshopdb`.
    - Create a user named `eshopuser` with password `1234` and grant all privileges on the database.

5. **Apply migrations:**

    `python manage.py makemigrations`
    `python manage.py migrate`

6. **Run the SSL server:**

    Before running the SSL server, make sure you have SSL certificates placed in the `ssl` directory of your project.

    `python manage.py runsslserver`


## Available Pages

Below is a list of all the available pages in the e-shop project:

### 1. Login Page

**URL:** `/`

<p align="center">
  <img src="assets/images/image-1.png" alt="Login Page">
</p>

**Description:** This is the landing page where users can log in to their accounts.

### 2. Product Catalogue Page

**URL:** `/products/`

<p align="center">
  <img src="assets/images/image-2.png" alt="Product Catalogue Page">
  <img src="assets/images/image-3.png" alt="Product Catalogue Page">
</p>

**Description:** Displays the product catalogue available to authenticated users. Users can search for products and add them to their cart.

### 3. Add to Cart

**URL:** `/add_to_cart/<product_id>/`

<p align="center">
  <img src="assets/images/image-4.png" alt="Add to Cart">
</p>

**Description:** Adds a selected product to the user's shopping cart.

### 4. Cart and Checkout Page

**URL:** `/checkout/`

<p align="center">
  <img src="assets/images/image-5.png" alt="Cart and Checkout Page">
</p>

**Description:** Shows the items in the user's cart and allows them to enter their shipping information. Users can review their order details and submit the order.

### 5. Order Summary Page

**URL:** `/order_summary/`

<p align="center">
  <img src="assets/images/image-6.png" alt="Order Summary Page">
</p>

**Description:** Provides a summary of the user's order before final submission.

### 6. Order Confirmation Page

**URL:** `/order_confirmation/`

<p align="center">
  <img src="assets/images/image-7.png" alt="Order Confirmation Page">
</p>

**Description:** Displays the confirmation of the user's order once it has been successfully placed.

### 7. Logout

**URL:** `/logout/`

<p align="center">
  <img src="assets/images/image-8.png" alt="Logout">
</p>

**Description:** Logs the user out and redirects them to the login page.


## Security Features

The e-shop project implements several security features:

1. **HTTPS Only:** All content is available only via HTTPS.
2. **Secure Cookies:** Session and CSRF cookies are configured to be secure.
3. **CSRF Protection:** Cross-Site Request Forgery protection is enabled.
4. **Rate Limiting:** Rate limiting is implemented on login attempts.
5. **Content Security Policy (CSP):** The application has a Content Security Policy to mitigate XSS attacks.
6. **HSTS:** HTTP Strict Transport Security is enforced to ensure all communication is over HTTPS.
7. **SQL Injection Prevention Mechanisms:** Django ORM query operations and other integrated security measures prevent SQL injection.
8. **HTML Escaping:** HTML content is escaped to prevent XSS attacks.
9. **SameSite Cookies:** The SameSite attribute is applied to cookies to prevent CSRF attacks.
10. **Django Integrated Security Measures:** Additional security measures provided by Django to tackle various threats.
