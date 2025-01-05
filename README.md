# **Eviden Asset Manager**

A brief description of what the project does and who it's for.

### **Table of Contents**

- [**Installation**](#installation)
- [**Usage**](#usage)
  - [**Authorisation**](#authorisation)
    - [**Register**](#register)
    - [**Log In**](#log-in)
    - [**Sign Out**](#sign-out)
    - [**Delete Account**](#delete-account)
  - [**Asset Features**](#asset-features)
    - [**Adding an Asset**](#adding-an-asset)
    - [**Adding Maintenance**](#adding-maintenance)
    - [**Editing or Deleting Maintenance**](#editing-or-deleting-maintenance)
    - [**Searching for an Asset**](#searching-for-an-asset)
    - [**Editing an Asset**](#editing-an-asset)
    - [**Deleting an Asset**](#deleting-an-asset)
  - [**Customer Features**](#customer-features)
    - [**Adding a Customer**](#adding-a-customer)
    - [**Searching for a Customer**](#searching-for-a-customer)
    - [**Editing a Customer**](#editing-a-customer)
    - [**Deleting a Customer**](#deleting-a-customer)
- [**Wireframes**](#wireframes)
- [**Contributing**](#contributing)
- [**License**](#license)

# **Installation**

Follow these steps to set up the project locally:

```bash
# Clone the repository
git clone https://github.com/Oliver-Lewington/asset-manager.git

# Navigate to the project directory
cd asset-manager

# Create a virtual environment in the root directory (asset-manager)
python -m venv venv

# Activate the virtual environment
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Install application dependencies
pip install -r requirements.txt
```
# Usage
User Manual for Eviden - Asset Manager
This user manual provides a step-by-step guide to perform common actions in the Eviden - Asset Manager. The following sections detail how to register, log in, sign out, and manage assets and customers.

## Authorisation
### Register
1.	Click on the Register link in the Eviden - Asset Manager interface.
   ![image](https://github.com/user-attachments/assets/01a04fd7-7c91-44ea-b09a-fa33403f6166)
2.	Fill in the registration form:
    o	Username: Enter your desired username.
    o	Password: Enter and confirm your password in the respective fields.
    o	(Optional) Check the Register as Administrator box if you want to register as an administrator.
3.	Click the Create Account button to complete the registration process.
4.	After registering, you will be automatically logged in and greeted with a welcome message.
   ![image](https://github.com/user-attachments/assets/4c48ca11-0deb-4932-91d3-bd5d9afd8692)
#### Log In
1.	On the login page, enter your registered username in the Username field.
   ![image](https://github.com/user-attachments/assets/0777b91b-f5b8-46d8-95b8-e6a33c74bb60)
2.	Enter your password in the Password field.
3.	Click the Login button to access your account.
4.	After logging in, you be greeted and greeted with a welcome back message.
   ![image](https://github.com/user-attachments/assets/2c97b623-740d-40f4-9158-cd342ae456dd)
#### Sign Out
1.	Click on the Hello, [username] Admin button (or equivalent) in the top navigation bar. 
2.	From the dropdown menu, select the Sign Out option.
     ![image](https://github.com/user-attachments/assets/c54058ae-5157-440b-beab-a1229cbad250)
3.	You will be logged out and redirected to the login page.
#### Delete Account
1.	Click on the Hello, [username] Admin button (or equivalent) in the top navigation bar. 
2.	In the dropdown menu, locate and click the Delete My Account option.
![image](https://github.com/user-attachments/assets/d9ba30db-4430-4455-a67a-92e39c9fec84)
3.	A confirmation prompt will appear. Click the Yes, Delete My Account button to permanently delete your account.
   ![image](https://github.com/user-attachments/assets/5f3944b1-68b3-45c7-bbf5-417b4a6bcf8d)
Tip: Ensure all information is entered accurately to avoid errors during registration or login. If issues persist, contact your administrator or support team.
## Asset Features
This guide explains how to perform essential tasks related to managing Assets in the application.
#### Steps for Adding an Asset
1.	Navigate to the Assets & Inventory section in the application.
  ![image](https://github.com/user-attachments/assets/f1db0305-8d3f-4fce-b359-3687724b330f)
2.	Click Add Asset.
  ![image](https://github.com/user-attachments/assets/cb1c34e9-8c99-4e2e-a346-81863518410f)
3.	Fill in the required fields:
    o	Asset Name: Enter the asset's name.
    o	Assigned To: Select a user.
    o	(Optional) Warranty Expiry Date: Choose a date.
    o	(Optional) Description: Provide additional details.
    o	Status: Set the current asset status.
4.	Click Create Asset to save.
  ![image](https://github.com/user-attachments/assets/f00e4135-89bb-477f-9283-b87912318ef0)
#### Steps for Adding Maintenance
1.	Navigate to the specific asset and click View. 
2.	Click Add Maintenance. 
   ![image](https://github.com/user-attachments/assets/ff4b230c-3bf5-45af-b250-597a6c5333ee)
3.	Fill in the required fields:
    o	Performed By: Select the technician.
    o	(Optional) Description: Provide maintenance details.
4.	Click Create Maintenance to save.
   ![image](https://github.com/user-attachments/assets/061a6547-4669-43e2-919d-ea06eabca983)
#### Steps for Editing or Deleting Maintenance
1.	Navigate to the specific asset and click View.
2.	Find the maintenance entry you want to edit or delete.  
  ![image](https://github.com/user-attachments/assets/e7fe3da3-c72f-4667-82ee-ff953c8e52cb)
3.	To edit, click the pencil icon:
    o	Update the necessary fields as described in the Adding Maintenance section.
  	![image](https://github.com/user-attachments/assets/fd809324-c80e-41e7-a521-9df787702f87)
5.	To delete, click the trash bin icon and confirm the deletion.
#### Steps for Searching for an Asset
1.	Navigate to the Asset section in the application.
2.	Locate the Search Asserts bar at the top of the page.
  ![image](https://github.com/user-attachments/assets/56489521-38ab-46a8-b069-27a129c570a7)
3.	Click into the search bar and type an asset name.
   ![image](https://github.com/user-attachments/assets/09b5e142-0666-4130-bca8-0722b3cd0d95)
4.	Press Enter or click the Search button (indicated by a magnifying glass icon).
5.	Review the filtered results to find the desired asset record.
   ![image](https://github.com/user-attachments/assets/f6142dc0-0dc0-465b-924d-25ac4242800f)
##### Additional Details:
o	The search bar automatically narrows down results based on your input.
#### Steps for Editing an Asset
1.	Navigate to the asset list and locate the asset.  
  ![image](https://github.com/user-attachments/assets/9c75d1d0-dbc5-44dd-baf6-752db84015c9)
2.	Click Edit Asset.
  ![image](https://github.com/user-attachments/assets/74c17b6b-3691-4c0a-b515-6ae93130ed3f)
3.	Update the necessary fields (e.g., name, assigned user, warranty date, etc.).  
  ![image](https://github.com/user-attachments/assets/c383b4a4-05d0-40c8-8ba0-d04c1c8f40e7)
4.	Click Save Changes to update the asset.
#### Steps for Deleting an Asset
1.	Navigate to the asset list and locate the asset.  
  ![image](https://github.com/user-attachments/assets/b76b8218-8a6a-479f-8197-2139364d0962)
2.	Click Delete Asset.  
  ![image](https://github.com/user-attachments/assets/1ec33e4d-b464-4d6c-87e6-18d2eb0f0fae)
3.	Confirm the deletion when prompted.
   ![image](https://github.com/user-attachments/assets/52c37c19-bd52-4619-87ab-19025645438e)
## Customer Features
This guide explains how to perform essential tasks related to managing customers in the application.
#### Steps for Adding a Customer
1.	Navigate to the Customers section in the application.  
  ![image](https://github.com/user-attachments/assets/02dd1681-84b2-4b42-b936-c6c928226714)
2.	Click on the Add Customer button.
3.	Fill in the required fields:
    o	Customer Name: Enter the customer's name.
    o	Contact Details: Provide an email address or phone number.
    o	(Optional) Address: Enter the customer's physical or mailing address.
    o	Status: Indicate the customer's current status (e.g., Active, Inactive). 
  ![image](https://github.com/user-attachments/assets/fd5bc8bb-dc02-458c-b579-28c9d533ad96)
4.	Click on the Create Customer button to save the customer record.
#### Steps for Searching for a Customer
1.	Navigate to the Customers section in the application. 
2.	Locate the Search Customers bar at the top of the page.  
  ![image](https://github.com/user-attachments/assets/e371ded6-b55c-4307-9ae8-f95ebad68e90)
3.	Click into the search bar and type the name, email, or other identifying detail of the customer.  
  ![image](https://github.com/user-attachments/assets/d2c350d3-1b7a-4735-a461-46da0dbfe50d)
4.	Press Enter or click the Search button (indicated by a magnifying glass icon).
5.	Review the filtered results to find the desired customer record. 
  ![image](https://github.com/user-attachments/assets/4efb7c5b-4acc-465c-b544-603cb406e67a)
##### Additional Details:
o  The search bar automatically narrows down results based on your input.
#### Steps for Editing a Customer
1.	Navigate to the Customers section and locate the customer you want to update. 
  ![image](https://github.com/user-attachments/assets/5d904cbc-1fad-4fdc-b8c9-945eee1145a0)
2.	Click on the Edit Customer button. 
   ![image](https://github.com/user-attachments/assets/2ffaca64-3264-4686-b9b9-c41a3046c52f)
3.	Update the necessary fields (e.g., name, contact details, status).  
  ![image](https://github.com/user-attachments/assets/d366f590-d0ff-4e38-a83b-0ba0d535764f)
4.	Click on the Save Changes button to apply the updates.
#### Steps for Deleting a Customer
1.	Navigate to the Customers section and locate the customer you want to remove.  
2.	Click on the Delete Customer button.  
3.	Confirm the deletion when prompted to permanently remove the customer record.  
# Wireframes

