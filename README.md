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
# For Windows
venv\Scripts\activate

# For Linux/Mac
source venv/bin/activate

# Install application dependencies
pip install -r requirements.txt

# Navigate to the application root "asset_manager"
cd asset_manager

# Run the Django development server
python manage.py runserver
```

The application will be available at `http://127.0.0.1:8000/` by default.

# License

This project is licensed under the MIT License. See the full license text below:

MIT License

Copyright (c) 2025 Oliver Lewington

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES, OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
