### This is a file which contains db pre-created dummy data for project demonstration. 
### Those values will be imported to the project.
### New data added using project functions will be added/modified as well to the existing db with the pre-created and earlier added data from this file.

from functions import items_db, users_db    # Import an empty items and users databases data from functions.py file

# Adding Users Dummy Data without any Items for now
# Source used for random names creation: https://goodbyejohndoe.com/
users_db["1"] = {"name": "Brandon Guidelines", "items": []}
users_db["2"] = {"name": "Carnegie Mondover", "items": []}
users_db["3"] = {"name": "John Doe", "items": []}
users_db["4"] = {"name": "Abraham Pigeon", "items": []}
users_db["5"] = {"name": "Miles Tone", "items": []}
users_db["6"] = {"name": "Claire Voyant", "items": []}

# Adding Items Dummy Data without any assignments
items_db["1"] = {
    "id": "1", "main_category": "Assets", "sub_category": "Laptop", "manufacturer": "Dell", "model": "XPS", "price": 5000, "quantity": 1, "status": "In Stock", "assigned_to": None
}
items_db["2"] = {
    "id": "2", "main_category": "Assets", "sub_category": "Laptop", "manufacturer": "Lenovo", "model": "X1 Carbon", "price": 8300, "quantity": 1, "status": "In Stock", "assigned_to": None
}
items_db["3"] = {
    "id": "3", "main_category": "Assets", "sub_category": "PC", "manufacturer": "Asus", "model": "Desktop Intel Core i9 14900KS", "price": 14900, "quantity": 1, "status": "In Stock", "assigned_to": "1"
}

items_db["4"] = {
    "id": "4", "main_category": "Accessories", "sub_category": "Docking Station", "manufacturer": "Dell", "model": "WD19TB", "price": 700, "quantity": 1, "status": "In Stock", "assigned_to": "1"
}
items_db["5"] = {
    "id": "5", "main_category": "Accessories", "sub_category": "Mouse", "manufacturer": "Logitech", "model": "MX Master 3", "price": 550, "quantity": 1, "status": "In Stock", "assigned_to": "3"
}
items_db["6"] = {
    "id": "6", "main_category": "Licenses", "sub_category": "Subscription", "manufacturer": "OpenAI", "model": "ChatGPT Pro", "price": 800, "quantity": 1, "status": "In Stock", "assigned_to": "5"
}

# Assigning some items to the users
users_db["1"]["items"].append("3")
users_db["1"]["items"].append("4")
users_db["3"]["items"].append("5")
users_db["5"]["items"].append("6")

# Changing item status from "In Stock" to "Assigned"
items_db["3"]["status"] = "Assigned"
items_db["4"]["status"] = "Assigned"
items_db["5"]["status"] = "Assigned"
items_db["6"]["status"] = "Assigned"