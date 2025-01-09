# **Eviden Asset Manager**

A streamlined web application designed to assist onsite service (OSS) teams in efficiently managing company assets such as laptops, printers, and desktops. This application enhances inventory tracking and assignment operations while ensuring simplicity and effectiveness.

## **Table of Contents**

- [**Overview**](#overview)
- [**Installation**](#installation)
- [**License**](#license)

## **Overview**

The Eviden Asset Manager is built using Django, following Agile methodologies to ensure robust and iterative development. This application caters to companies needing seamless management of IT assets and tracking their allocation to users.

## **Installation**

Follow these steps to set up the project locally:

```bash
# Clone the repository
git clone https://github.com/Oliver-Lewington/asset-manager.git

# Navigate to the project directory
cd asset-manager

# Create a virtual environment in the root directory (asset-manager)
python -m venv venv

# Activate the virtual environment
venv\Scripts\activate # For Windows
source venv/bin/activate # For Linux/Mac

# Install application dependencies
pip install -r requirements.txt

# Navigate to the application root "asset_manager"
cd asset_manager

# Run the Django development server
python manage.py runserver
```

The application will be available at `http://127.0.0.1:8000/` by default.

# License

This project is licensed under the MIT License. 
