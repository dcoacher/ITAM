### This is a Functions file which will contain functions for reusable logic of the Main file.
import getpass  # Importing Getpass module for password input data masking

items_db = {}   # Creation of items database empty list
users_db = {}   # Creation of users database empty list

user_id_counter = 7 # Creation of User ID Counter value (will start from 7 because of dummy data)
item_id_counter = 7 # Creation of Item ID Counter value (will start from 7 because of dummy data)

def welcome_screen():   # Welcome Screen function
    welcome_screen_total_users = len(users_db)  # Calculating Starting Total Users Existing in the Users Database (Including Dummy Data preloaded)
    welcome_screen_total_items = len(items_db)  # Calculating Starting Total Items Existing in the Items Database (Including Dummy Data preloaded)
    welcome_screen_items_in_stock = 0   # Set Items with status "In Stock" with zero value before calculation
    welcome_screen_items_assigned = 0   # Set Items with status "Assigned" with zero value before calculation
    welcome_screen_items_categories = {"Assets": 0, "Accessories": 0, "Licenses": 0}    # Set Items Categories Types with zero value before calculation
    # Start Items Status and Category Calculation
    for item in items_db.values():  # Loop for identify item status, category and calculate them
        status = item.get("status", "")
        category = item.get("main_category", "")

        if status == "In Stock":    # In case Item Status equal "In Stock"
            welcome_screen_items_in_stock += 1  # Update "In Stock" counter by counting +1
        elif status == "Assigned":  # In case Item Status equal "Assigned"
            welcome_screen_items_assigned += 1  # Update "Assigned" counter by counting +1
        if category in welcome_screen_items_categories: # In case Item Category equal Assets/Accessories/Licenses
            welcome_screen_items_categories[category] += 1  # Update the relevant category counter by counting +1
    # End Items Status and Category Calculation

    # Start Printing Data
    print("\n👋 Welcome to IT Asset Management System!")
    print("🙏 Credits to Desmond Coacher and Artiom Krits.\n")
    print(f"ℹ️  Total Users Existing in the Database: {welcome_screen_total_users}")
    print(f"ℹ️  Total Items Existing in the Database: {welcome_screen_total_items}")
    print(f"ℹ️  In Stock Items: {welcome_screen_items_in_stock}, Assigned Items: {welcome_screen_items_assigned}")
    for value, count in welcome_screen_items_categories.items():    # Loop for printing the items quantity by categories
        print(f"ℹ️  {value} Items: {count}")

    # End Printing Data

def login_screen(): # Login Screen function
    while True: # Loop for user input prompt for username and password credentials
        username = input("Enter the username: ")
        password = getpass.getpass("Enter the password: ")
        if username == "root" and password == "123456": # Validation for the entered by the user credentials
            print(f"✅ Success: You has been successfully logged in as `{username}`.")    # Success case - break the loop and login
            break
        else:
            print("❌ Error: Incorrect username/password data has been entered. Please try again.\n")   # Incorrect data provided case, return to the loop start

def main_menu_handler(): # Menu Handler function
    print("\n🔸 Main Menu🔸")
    print("1️⃣  Add New Item")
    print("2️⃣  Delete Item")
    print("3️⃣  Modify Item")
    print("4️⃣  Assign Item")
    print("5️⃣  Add New User")
    print("6️⃣  Show All Users")
    print("7️⃣  Show All Items by the User")
    print("8️⃣  Show All Stock Items")
    print("9️⃣  Calculate Stock by Categories\n")

def main_menu_add_new_item():  # Add New Item Main Menu Function
    while True: # Starting Loop
        global item_id_counter  # Calling ID Counter
        item_id = str(item_id_counter)  # Convert to string in order to store all the user ID's in the same format
        main_category = input("Choose Category (Assets/Accessories/Licenses): ")    # Ask the User to choose Main Category
        if main_category == "Assets":   # In case the User's choise is Assets Main Category
            sub_category = input("Choose Item (PC/Laptop): ")   # Ask the User to choose Sub Category
            if sub_category.lower() not in ["pc", "laptop"]:    # In case the User's choise is not equal the sub category prompt
                print("❌ Error: Error: Invalid Item has been choosen.")  # Error Message Printing
                return  # Exit the function in this phase (return to main menu)

        elif main_category == "Accessories":    # In case the User's choise is Accessories Main Category
            sub_category = input("Choose Item (Mouse/Keyboard/Docking Station/Monitor/Headset): ")  # Ask the User to choose Sub Category
            if sub_category.lower() not in ["mouse", "keyboard", "docking station", "monitor", "headset"]:  # In case the User's choise is not equal the sub category prompt
                print("❌ Error: Error: Invalid Item has been choosen.")  # Error Message Printing
                return  # Exit the function in this phase (return to main menu)

        elif main_category == "Licenses":   # In case the User's choise is Licenses Main Category
            sub_category = input("Choose Item (Serial Number/Subscription): ")  # Ask the User to choose Sub Category
            if sub_category.lower() not in ["serial number", "subscription"]:   # In case the User's choise is not equal the sub category prompt
                print("❌ Error: Error: Invalid Item has been choosen.")  # Error Message Printing
                return  # Exit the function in this phase (return to main menu)

        else:
            print("❌ Error: Invalid Category has been choosen.") # Error Message Printing for Invalid Main Category choose by the User
            return  # Exit the function in this phase (return to main menu)

        manufacturer = input("Enter the Manufacturer: ")    # Prompt the user for input data
        model = input("Enter the Model: ")  # Prompt the user for input data
        price = input("Enter the Price per Unit: ")    # Prompt the user for input data and convert the value to integer
        if not price.isdigit(): # Checking if the user entered numeric value into the input line above
            print("❌ Error: Entered value for the price must be numeric.")   # Printing Error Message
            return  # Exit the function in this phase (return to main menu)

        item = {    # Creating New Item record based on the prompt values
            "id": item_id,
            "main_category": main_category,
            "sub_category": sub_category,
            "manufacturer":manufacturer,
            "model": model,
            "price": int(price),    # Convert the value to integer
            "quantity": 1,  # Quantity is "1" by default
            "status": "In Stock",   # Default value equals "In Stock"
            "assigned_to": None # There are no item assignment by default
        }

        item_id_counter += 1    # Updating Item ID Counter
        items_db[item["id"]] = item # Adding the New Item record to the Items Database
        print(f"✅ Success: The Item `{sub_category} {manufacturer} {model}` with the ID `{item_id}` was successfully added to the database.")  # Printing Success Message to the User
        add_additional_one = input("Do you want to add additional item? (y/n): ")   # Asking the user for additional item adding
        if add_additional_one == "y":   # In case the user's answer is "y" (yes) - Proceed
            True    # Going back to the Loop Start
        else:   # In case the user's answer is "n" (no) - Break
            break   # Breaking Loop

def main_menu_delete_item():    # Delete Item Main Menu Function
    while True: # Starting Loop
        item_id = input("Enther Item ID to delete: ")   # Prompt the user for input data
        if not item_id.isdigit(): # Checking if the user entered numeric value into the input line above
            print("❌ Error: Entered value must be numeric.")   # Printing Error Message
            return  # Exit the function in this phase (return to main menu)
        
        if item_id in items_db: # In case the provided by the User ID exists in the Items Database
            item_sub_category_ram = items_db[item_id]["sub_category"]   # Create temp RAM record for the Success Removal Message Item Sub Category Displaying
            item = items_db[item_id]
            assigned_user_id = item.get("assigned_to")  # Getting the "Assigned to" User's ID in order to remove the assignment record
            if assigned_user_id in users_db:    # In Case the Item's Status is "Assigned" - proceed and remove the Record from the User by the User's ID
                if item_id in users_db[assigned_user_id]["items"]:
                    users_db[assigned_user_id]["items"].remove(item_id)
            
            del items_db[item_id]   # Delete the Item from the Items Database
            print(f"✅ Success: The item `{item_sub_category_ram}` with the ID `{item_id}` has been revomed from the database.")    # Printing Success Message to the User
            add_additional_one = input("Do you want to delete additional item? (y/n): ")   # Asking the user for additional item removal
            if add_additional_one == "y":   # In case the user's answer is "y" (yes) - Proceed
                True    # Going back to the Loop Start
            else:   # In case the user's answer is "n" (no) - Break
                break   # Breaking Loop
        else:
            print(f"❌ Error: There are no item with the ID `{item_id}` existing in the database.") # Printing Error Message to the User in case the provided Item ID is not exist in the Database
            return  # Exit the function in this phase (return to main menu)
              
def main_menu_modify_item():    # Modify Item Main Menu Function
    item_id = input("Enter Item ID to modify: ")    # Prompt the user for input data
    if not item_id.isdigit(): # Checking if the user entered numeric value into the input line above
        print("❌ Error: Entered value must be numeric.")   # Printing Error Message
        return  # Exit the function in this phase (return to main menu)
    
    if item_id in items_db: # In case the provided Item ID by the User exist in the Item Database
        item = items_db[item_id]
        # Start Displaying Current Item's Status (Manufacturer/Model/Price)
        print("")
        print("-" * 50)
        print(f"Item            : {item["sub_category"]}")
        print("-" * 50)
        print(f"Manufacturer    : {item["manufacturer"]}")
        print("-" * 50)
        print(f"Model           : {item["model"]}")
        print("-" * 50)
        print(f"Price per Unit  : {item["price"]} ₪")
        print("-" * 50)
        # End Displaying Current Item's Status (Manufacturer/Model/Price)
        change_type = input("\nWhich data do you want to modify?\nManufacturer (mfg), Model (m), Price per Unit (p)\nFor Exit (q)\nEnther your choise: ")    # Ask the user for the data type to modify
        if change_type.lower() == "mfg":    # In case the User's choise is "mfg"
            current_manufacturer = item["manufacturer"] # Create temp RAM data for the current (old) manufacturer in order to print in Success Message afterward
            changed_manufacturer = input(f"Current Manufacturer is `{item["manufacturer"]}`. Enther new Manufacturer: ")    # Prompt the user to enter the new Manufacturer data
            item["manufacturer"] = changed_manufacturer # Update the new record based on the data entered by the user
            print(f"✅ Success: Manufacturer for the Item `{item["sub_category"]}` with the ID `{item["id"]}` has been changed from `{current_manufacturer}` to `{changed_manufacturer}`.") # Printing Success Message to the User

        elif change_type.lower() == "m":    # In case the User's choise is "m"
            current_model = item["model"]   # Create temp RAM data for the current (old) model in order to print in Success Message afterward
            changed_model = input(f"Current Model is `{item["model"]}`. Enther new Model: ")    # Prompt the user to enter the new Model data
            item["model"] = changed_model   # Update the new record based on the data entered by the user
            print(f"✅ Success: Model for the Item `{item["sub_category"]}` with the ID `{item["id"]}` has been changed from `{current_model}` to `{changed_model}`.")  # Printing Success Message to the User

        elif change_type.lower() == "p":    # In case the User's choise is "p"
            current_price = item["price"]   # Create temp RAM data for the current (old) price in order to print in Success Message afterward
            changed_price = input(f"Current Price is `{item["price"]} ₪`. Enther new Price: ")  # Prompt the user to enter the new Price data
            try:    # Check if entered value by the user is numeric
                item["price"] = int(changed_price)  # Update the new record based on the data entered by the user and convert to integer
                print(f"✅ Success: Price for the Item `{item["sub_category"]}` with the ID `{item["id"]}` has been changed from `{current_price}` to `{changed_price}`.")  # Printing Success Message to the User
            except ValueError:  # In case the entered by the user value is not numeric
                print("❌ Error: Entered value must be numeric.")   # Printing Error Message
        
        elif change_type.lower() == "q":    # In case the User's choise is "q"
            return  # Exit the function in this phase (return to main menu)
        
        else:
           print("❌ Error: Invalid option has been choosen.")  # Printing Error Message in case the user's choise for data modifying wasn't (mfg/m/p)

    else:
        print(f"❌ Error: There are no item with the ID `{item_id}` existing in the database.") # Printing Error Message in case the provided Item ID by the user is not exist in the Item Database

def main_menu_assign_item():    # Assign Item Main Menu Function
    while True:
        item_id = input("Enter Item ID to assign: ")    # Prompt the user for input data
        user_id = input("Enter User ID to assign to: ") # Prompt the user for input data

        if not item_id in items_db and not user_id in users_db: # In case the Item ID or/and User ID are not exists in the Databases
            print(f"❌ Error: There are no item with the ID `{item_id}` or/and user with the ID `{user_id}` existing in the database.") # Printing Error Message
            return  # Exit the function in this phase (return to main menu)
        else:   # In case the Item ID and User ID exists in the Databases (Proceed)
            if items_db[item_id]["status"] == "Assigned":   # Checking if the Item's Status is "Assigned"
                print(f"❌ Error: The item `{items_db[item_id]["sub_category"]} {items_db[item_id]["manufacturer"]} {items_db[item_id]["model"]}` with the ID `{item_id}` is already assigned to another user.")    # Printing Error Message because the item is already assigned to another user
                return  # Exit the function in this phase (return to main menu)
            else:   # In case the Item's Status is "In Stock" (Proceed)
                items_db[item_id]["status"] = "Assigned"    # Change the Item's status from "In Stock" to "Assigned"
                items_db[item_id]["assigned_to"] = user_id  # Update the User's ID for "Assigned to" value
                users_db[user_id]["items"].append(item_id)  # Add the Item ID to the User's record in Users Database based on ID
                print(f"✅ Success: The item `{items_db[item_id]["sub_category"]} {items_db[item_id]["manufacturer"]} {items_db[item_id]["model"]}` with the ID `{item_id}` was successfully assigned to the user `{users_db[user_id]["name"]}`.")    # Printing Success Message to the User
                add_additional_one = input("Do you want to assign additional item? (y/n): ")   # Asking the user for additional item assign
                if add_additional_one == "y":   # In case the user's answer is "y" (yes) - Proceed
                    True    # Going back to the Loop Start
                else:   # In case the user's answer is "n" (no) - Break
                    break   # Breaking Loop

def main_menu_add_new_user():   # Add New User Main Menu Function
    while True: # Starting Loop
        user = input("Enter the Full Name: ")  # Prompt the user for input data
        if not user.replace(" ", "").isalpha():  # Checking if the user entered numeric value into the input line above
            print("❌ Error: Entered value cannot be numeric.")   # Printing Error Message
            break   # Breaking the Loop 
        global user_id_counter  # Calling ID Counter
        user_id = str(user_id_counter)  # Convert to string in order to store all the user ID's in the same format
        users_db[user_id] = {"name": str(user), "items": []} # Adding the User to the Users Database without any assigned items
        print(f"✅ Success: The User `{user}` with the ID `{user_id}` was successfully added to the database.") # Printing Success Message to the User
        user_id_counter += 1    # Updating User ID Counter
        add_additional_one = input("Do you want to add additional user? (y/n): ")   # Asking the user for additional user adding
        if add_additional_one == "y":   # In case the user's answer is "y" (yes) - Proceed
            True    # Going back to the Loop Start
        else:   # In case the user's answer is "n" (no) - Break
            break   # Breaking Loop

def main_menu_show_all_users(): # Show All Users Main Menu Function
    if not users_db:    # In case there are no users exists in the Users Database
        print("❌ Error: There are no users existing in the database.") ## Printing Error Message 
    else:   # In case there are users in the Users Database (Proceed)
        print("\nUsers List:")  # Printing Header
        print("-" * 50) # Printing Header
        for id, name, in users_db.items():  # For each record in the Users Database Loop
            print(f"ℹ️  ID: {id}, Full Name: {name["name"]}")   # Print the record

def main_menu_show_all_items_by_the_user(): # Show All Items by the User Main Menu Function
    prompt_user_id = input("Enter the User ID: ")   # Prompt the user for input data
    if not prompt_user_id.isdigit():    # Checking if the user entered numeric value into the input line above
        print("❌ Error: Entered value must be numeric.")   # Printing Error Message
        return  # Exit the function in this phase (return to main menu)

    if prompt_user_id in users_db:  # In case the entered by the User User's ID exists in Users Database (Proceed)
        user_id = users_db[prompt_user_id]  # Creating User's ID record basing on the data provided by the user and exists in the Users Database
        items = user_id["items"]    # Creating User's Items Assigned by the User ID

        if not items:   # In case there are no items assigned to the user
            print(f"ℹ️  Info: The User `{user_id["name"]}` has no assigned items.")  # Printing Info Message to the user
        else:   # In case there are items assigned to the user (Proceed)
            # Start Displaying User's Data
            print(f"\nℹ️  ID: {prompt_user_id}, Full Name: {user_id["name"]}\n")
            print("Items List:")    # Printing Header
            print("-" * 50) # Printing Header
            # End Displaying User's Data
            # Start Displaying Item's Data using Loop
            for item_id in items:   # For each item assigned to the user - print based on the format below
                item = items_db.get(item_id)
                if item:
                    print(f"Item ID         : {item["id"]}")
                    print(f"Item            : {item["sub_category"]}")
                    print(f"Category        : {item["main_category"]}")
                    print(f"Manufacturer    : {item["manufacturer"]}")
                    print(f"Model           : {item["model"]}")
                    print(f"Price per Unit  : {item["price"]} ₪")
                    print(f"Quantity        : {item["quantity"]}")
                    print(f"Status          : {item["status"]}")
                    print("-" * 50)
            # End Displaying Item's Data using Loop
    else:   # In case the user's ID provided by the user is not exist in the Users Database
        print(f"❌ Error: There are no user with the ID `{prompt_user_id}` existing in the database.")  # Displaying Error Message

def main_menu_show_all_stock_items():   # Show All Stock Items Main Menu Function
    if not items_db:    # In case there are no items in the Item Database
        print("❌ Error: There are no items existing in the database.") # Displaying Error Message
    else:   # In case there are items in the Item Database (Proceed)
        print("\nAll Stock Items List:")    # Print Header
        print("-" * 50) # Print Header

        # Start Displaying Item's Data using Loop
        for item in items_db.values():  # For each item existing in the Database - print based on the format below
            print(f"Item ID         : {item["id"]}")
            print(f"Item            : {item["sub_category"]}")
            print(f"Category        : {item["main_category"]}")
            print(f"Manufacturer    : {item["manufacturer"]}")
            print(f"Model           : {item["model"]}")
            print(f"Price per Unit  : {item["price"]} ₪")
            print(f"Quantity        : {item["quantity"]}")
            print(f"Status          : {item["status"]}")
            print("-" * 50)   
        # End Displaying Item's Data using Loop

def main_menu_calculate_stock_by_categories():  # Calculate Stock by Categories Main Menu Function
    stock = {"Assets": 0, "Accessories": 0, "Licenses": 0}  # Creating value with starting zero values for each category
    if not items_db:    # In case there are no items in the Item Database
        print("❌ Error: There are no items existing in the database.") # Displaying Error Message
    else:   # In case there are items in the Item Database (Proceed)
        print("\nStock Items Calculation by Categories:")   # Print Header
        print("-" * 50) # Print Header
        for item in items_db.values():  # Loop for calculate stock total values based on items quantity and price per unit
            main_category = item["main_category"]
            stock[main_category] += item["price"] * item["quantity"]
        for category, sum in stock.items(): # Loop for printing calculated values per category
            print(f"ℹ️  Category: {category}, Total Value: {sum} ₪")