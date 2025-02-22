# Fleet Manager - A Vehicle Management System

## Description

Fleet Manager is a web-based application designed to help organizations manage their vehicle assets efficiently. Users can add vehicles, track purchase details, monitor expiry dates for discounts, and receive email reminders. The app ensures streamlined fleet management with an intuitive interface and automated notifications.

## Distinctiveness and Complexity

Fleet Manager is a vehicle management system that builds on the lessons picked up from all earlier course projects and introduces additional complexities. Unlike the earlier CS50W projects, Fleet Manager integrates multiple interconnected features, including a comprehensive asset tracking system, automated task scheduling using Django-Q, and real-time email notifications via SendGrid. The project involves structured data modeling to handle vehicle records, purchase details, and disc expiry tracking while ensuring efficient background task execution. Additionally, Fleet Manager implements intricate user interactions, such as search functionalities by VIN, make, or model, and long-term data persistence beyond typical shopping cart behavior. By incorporating automated workflows and critical notifications, Fleet Manager enhances operational efficiency, making it a more sophisticated and feature-rich application than current CS50W projects or a standard restaurant ordering system such as that covered in the old CS50W Pizza project.

### Project Structure (Key files added)

- fleet_manager/models.py - Defines the database models for vehicles, including fields for purchase details and expiry tracking.
- fleet_manager/views.py - Contains the logic for displaying vehicle details, handling user interactions, and managing search functionality.
- fleet_manager/urls.py - Maps URLs to their corresponding views.
- fleet_manager/tasks.py - Defines scheduled background tasks, such as sending email reminders for discount expiries.
- fleet_manager/templates/ - Contains the HTML templates for rendering the frontend.
- fleet_manager/static/ - Stores static assets like CSS, JavaScript, and asset thumbnail images.
- fleet_manager/admin.py - Registers models with the Django admin panel for easier management.
- fleet_manager/forms.py - Contains Django forms for assets and editing profiles.
- settings.py - The main Django settings file, configured for MySQL, SendGrid email, and Django-Q task scheduling.

## Features

- **User Authentication**: Secure login and user management.
- **Vehicle Management**: Add, update, and delete vehicle assets.
- **Purchase Details Tracking**: Store invoice details, purchase dates, and dealership information.
- **Discount Expiry Alerts**: Automatic email notifications for approaching discount expiry dates.
- **Task Scheduling**: Uses Django-Q for background task execution.
- **Search Functionality**: Easily find vehicles by VIN, make, or model.

## Technologies Used

- **Frontend**: HTML, CSS (Bootstrap), JavaScript
- **Backend**: Django
- **Database**: MySQL
- **Task Scheduling**: Django-Q
- **Email Notifications**: SendGrid

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/simminda/fleet-manager.git
   cd fleet-manager
   ```
2. Create a virtual environment and activate it:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Set up MySQL and configure `settings.py` accordingly:
   ```python
   DATABASES = {
       'default': {
           'ENGINE': 'django.db.backends.mysql',
           'NAME': 'your_database_name',
           'USER': 'your_database_user',
           'PASSWORD': 'your_database_password',
           'HOST': 'localhost',
           'PORT': '3306',
       }
   }
   ```
5. Apply database migrations:
   ```bash
   python manage.py migrate
   ```
6. Create a superuser:
   ```bash
   python manage.py createsuperuser
   ```
7. Start the development server:
   ```bash
   python manage.py runserver
   ```
8. Start Django-Q cluster:
   ```bash
   python manage.py qcluster
   ```
9. Access the app at `http://127.0.0.1:8000/`.

## Usage

- Log in to the system.
- Add vehicle assets and enter their purchase details.
- The system automatically sends email reminders when a discount is nearing expiry.
- Search for vehicles using their VIN, make, or model.
- Monitor and manage fleet assets effectively.

## To-Do

- Implement role-based access control for different user levels.
- Create a better landing page/dashboard for quick analytics on fleet data.
- Improve UI styling for better user experience.
- Implement all features listed in Sidebar.
- Add image property for assets and allow uploading.
- Give more asset and renewal details in the email notification

## License

This project is open-source and available under the [MIT License](LICENSE).

## Author

Developed by Simphiwe Ndaba.

## Acknowledgments

This project was inspired by the need for efficient fleet management solutions and was developed as part of Simphiwe's CS50W journey.
