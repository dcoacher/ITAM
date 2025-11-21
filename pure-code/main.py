### This is a Main file which will contain Welcome Screen and Main Menu features. 
import functions # Importing functions module from functions.py file
import demo # Importing Dummy Data (preloaded Users and Items with different status)


functions.welcome_screen() # Welcome Screen (will be displayed once and not included to the menu loop)
# functions.login_screen()    # Adding Login Screen feature using admin username and password credentials (Temporarily Disabled)

while True: # Start of Loop Menu
    functions.main_menu_handler()   # Calling Main Menu from Functions file
    main_menu_user_choise = input("✨ Please choose menu option (q for exit)✨: ")   # Prompt the user for main menu option choosing

    match main_menu_user_choise:  # Start of Menu Options, based on match cases
        case "1":
            functions.main_menu_add_new_item() # Calling Main Menu "Add New Item" Function

        case "2":
            functions.main_menu_delete_item()   # Calling Main Menu "Delete Item" Function

        case "3":
            functions.main_menu_modify_item()   # Calling Main Menu "Modify Item" Function

        case "4":
            functions.main_menu_assign_item()   # Calling Main Menu "Assign Item" Function

        case "5":
            functions.main_menu_add_new_user()  # Calling Main Menu "Add New User" Function

        case "6":
            functions.main_menu_show_all_users()    # Calling Main Menu "Show All Users" Function

        case "7":
            functions.main_menu_show_all_items_by_the_user()    # Calling Main Menu "Show All Items by the User" Function

        case "8":
            functions.main_menu_show_all_stock_items()  # Calling Main Menu "Show All Stock Items" Function

        case "9":
            functions.main_menu_calculate_stock_by_categories() # Calculate Stock by Categories" Function
        
        case "q":   # Exit
            print("👋 Thank you for using our service. See you later!\n")   # Print goodbye message to the user before quit the loop
            break   # Breaking the loop

        case _:
            print("❌ Error: Incorrect menu option has been chosen. Please try again.") # In case the user's chosen option does not exist
    # End of Menu Options, based on match cases

#    input("Press Enter key in order to return to the Main Menu.") # Prompt the input message as a part of the loop for returning to the Main Menu (Temporarily Disabled)
# End of Loop Menu