# d_crm
**Django CRM**<br>
Django Customer Order Management System.<br>

**Features**<br>
Registration and logging in of customers and staffs<br>
Confirmation of Availability by items placed on order.

**Usage**<br>
To run the project:<br>
EMAIL CONFIGURATION SETTINGS<br>
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'<br>
EMAIL_HOST = 'smtp.gmail.com'<br>
EMAIL_PORT = 587<br>
EMAIL_USE_TLS = True<br>
EMAIL_HOST_USER = os.environ.get('EMAIL_USER')<br>
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_PASS')<br>

Change EMAIL_USER and EMAIL_PASS to your own set environment variables.<br>

Clone the repository<br>
<sub>Create a virtual environment.
If you already have an existing virtual environment you can skip the creation step. Navigate to where the virtual environment is and activate the environment.<br>
python -m venv name_of_environment<br>
name_of_environment/bin/activate<br>
Install requirements.<br>
pip install -r requirements.txt<br>
Apply migration.<br>
python manage.py migrate<br>
Run the application by starting the server<br>
python manage.py runserver<br></sub>
