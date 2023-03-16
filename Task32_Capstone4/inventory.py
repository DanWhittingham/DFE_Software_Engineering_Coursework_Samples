'''
OOP solution for stock management system
Code a Python program that will read from a text file inventory.txt and
perform various operations according to specifications & template
'''


#========Imports========
# pip install tabulate --user   ## needed for suitable display of product lines
from tabulate import tabulate


#========Shoe class==========
class Shoe:
    '''
    Represents a product line: country, code, product (name), cost, quantity
    '''
    
    def __init__(self, country: str, code: str, product: str, cost: float, quantity: int):
        '''Shoe constructor'''
        self.country = country
        self.code = code
        self.product = product
        self.cost = cost
        self.quantity = quantity

    def get_cost(self):
        '''Returns the cost of the shoe'''
        return(self.cost)

    def get_quantity(self):
        '''Returns the stock quantity of the shoe'''
        return(self.quantity)

    def get_stock_value(self):
        '''Returns value of stock'''
        return(self.cost * self.quantity)

    def add_stock(self, increase):
        '''Add stock'''
        self.quantity = self.quantity + increase

    def make_list(self):
        '''Returns the shoe data to a list, intended for tabulation'''
        return [self.country, self.code, self.product, self.cost, self.quantity]

    def __str__(self):
        '''Returns the shoe data as comma-separated string'''
        return(f"{self.country},{self.code},{self.product},{self.cost:.2f},{self.quantity}")



#==========Menu functions==============
def read_shoes_data():
    '''
    Function to:
    1) read data from inventory.txt
    2) create Shoe object for each line
    3) append to shoe_list
    One line in this file represents data to create one object of shoes. 
    First line assumed to be a header line
    '''
    shoe_list.clear()
    with open("inventory.txt", "r") as shoe_data:
        next(shoe_data)  # Skip header line
        for line in shoe_data:
            this_shoe_as_list = line.strip().split(",")  # convert to list
            try:  # Ensure the description has the anticipated structure (same as header)
                this_shoe_as_list[3] = float(this_shoe_as_list[3])
                this_shoe_as_list[4] = int(this_shoe_as_list[4])
                this_shoe = Shoe(*this_shoe_as_list) # Unpack shoe_list to pass as args
                shoe_list.append(this_shoe)
            except (TypeError, IndexError, ValueError):
                print(f"Warning, unexpected contents on line:\n{line}")
    print("\nData read successfully")


def capture_shoes():
    '''
    Function to obtain and validate shoe description,
    create shoe object, add it to list and update the inventory file.
    '''
    shoe_as_list = ["", "", "", 0, 0]  # Dummy list
    print("\nPlease enter the product country:")
    shoe_as_list[0] = take_valid_string()
    print("\nPlease enter the product code:")
    shoe_as_list[1] = take_valid_string().upper()
    print("\nPlease enter the product name:")
    shoe_as_list[2] = take_valid_string()
    print("\nPlease enter the product cost:")
    shoe_as_list[3] = take_positive_float()
    print("\nPlease enter the product quantity:")
    shoe_as_list[4] = take_non_negative_int()

    new_shoe = Shoe(*shoe_as_list)  # Unpack list to args for object creation
    shoe_list.append(new_shoe)  # Add to in-memory shoe_list

    # Keep the inventory file updated
    with open("inventory.txt", "a") as shoe_data:
        shoe_data.write("\n" + str(new_shoe))

    print("\nNew product added:\n" + str(new_shoe))
    
    ask_if_finished()


def view_all():
    '''
    Output a table displaying information on all product lines
    '''
    print("\nAll product lines:")
    tabulate_shoes(shoe_list)
    
    ask_if_finished()


def re_stock():
    '''
    Dsiplay the shoe objects with the lowest quantity
    Ask the user if they want to re-stock and by how much
    Update the in-memory inventory and the source file
    '''
    min_stock = shoe_list[0].get_quantity()  # set min to 0th shoe
    restock_candidates = [shoe_list[0]]      # put 0th shoe in candidate list
    restocked = False                        # stock hasn't changed yet

    for shoe in shoe_list[1:]: # begin from next shoe
        if shoe.get_quantity() < min_stock:
            # If we find a shoe with lower quantity, replace the restock list
            restock_candidates = [shoe]
            # Set new minimum
            min_stock = shoe.get_quantity()
        elif shoe.get_quantity() == min_stock:
            # If shoe has same quanity as current min, add it to restock list
            restock_candidates.append(shoe)
    
    # Show results
    print("\nThe following lines have low stock:")
    tabulate_shoes(restock_candidates)

    # Decide how to restock
    print("\nRestock all by same amount, or invdividually?")
    while True:
        choice = input("Enter A for all or I for individual restock: ").lower()
        if choice == "a" or choice == "i":
            break
        else:
            print("Unrecognised selection.")

    if choice == "a":
        # Restocking the selected product lines by the same amount
        print("\nEnter a whole number to restock these lines by:")
        increase = take_non_negative_int()
        if increase != 0:
            # Add the quantity to each of the shoes
            for shoe in restock_candidates:
                shoe.add_stock(increase)
            restocked = True  # Record that stock has changed


    if choice == "i":
        # Restock by a chosen amount for each product line
        for shoe in restock_candidates:
            print("\nRestocking this line:\n" + str(shoe))
            print("\nEnter a whole number to restock this line by:")
            increase = take_non_negative_int()
            if increase != 0:
                shoe.add_stock(increase)  # add the chosen quantity for this shoe
                restocked = True  # record that stock has changed

    if restocked:
        # If any of the quantities were changed, update the inventory file
        with open("inventory.txt", "w") as shoe_data:
            shoe_data.write("Country,Code,Product,Cost,Quantity") # Header line
            for shoe in shoe_list:
                shoe_data.write("\n" + str(shoe)) # Put each shoe-string on new line

    # Display outcome
    print("\nStock for these lines now as follows:")
    tabulate_shoes(restock_candidates)
    
    ask_if_finished()
          

def search_shoe():
    '''
    Take product code from user and show matching product lines
    '''
    print("\nPlease enter the product code to search for (case-sensitive):")
    search_code = take_valid_string()
    matching_shoes = []

    # Scan product lines for matching product code
    for shoe in shoe_list:
        if shoe.code == search_code:
            matching_shoes.append(shoe)
    
    if len(matching_shoes) == 0:
        # No hits
        print("\nNo matching products found.")

    else:
        # Display results
        print("\nFound the following matches:")
        tabulate_shoes(matching_shoes)
    
    ask_if_finished()


def value_per_item():
    '''
    Print stock value for each product line, and total stock value
    '''
    total_stock_value = 0
    for shoe in shoe_list:
        stock_value = shoe.get_stock_value()
        total_stock_value += stock_value  # running total
        print(f"The following product line \n{str(shoe)}\n has stock value: {stock_value:.2f}\n")
    print(f"Total stock value: {total_stock_value:.2f}")
    
    ask_if_finished()


def highest_qty():
    '''
    Find and display the product lines with the highest stock
    '''
    max_stock = shoe_list[0].get_quantity() # set max to 0th shoe
    sale_candidates = [shoe_list[0]]        # put 0th shoe in sale list

    for shoe in shoe_list[1:]:  # start from next shoe
        if shoe.get_quantity() > max_stock:
            # If we find new maximum, replace the sale list
            sale_candidates = [shoe]
            # Set new maximum
            max_stock = shoe.get_quantity()
        elif shoe.get_quantity() == max_stock:
            # If shoe has same quantity as current max, append to sale list
            sale_candidates.append(shoe)
    
    # Display outcome
    print("\nThe following product lines have the highest quantity, put these on sale:")
    tabulate_shoes(sale_candidates)
    
    ask_if_finished()


def finished():
    '''
    Conclude stock management
    '''
    print("\nGoodbye!")
    exit()

#==========Utility functions used within menu functions============
def take_valid_string():
    '''
    Take and validate string for country, code and product
    These must not be empty, must not contain commas
    '''
    while True:
        user_string = input("")
        user_string = user_string.strip()
        if user_string == "":
            print("\nEmpty input, please try again:")
        elif "," in user_string:
            print("\nCommas not allowed, please try again:")
        else:
            return user_string


def take_positive_float():
    '''
    Take and valid suitable input for cost
    These must be positive floats
    '''
    while True:
        user_input = input("")
        try:
            user_float = float(user_input)
            if user_float > 0:  # Ensure positive cost
                return user_float
            else:
                print("\nInput must be positive, please try again:")
        except ValueError:
            print("\nInput must be numerical, please try again:")


def take_non_negative_int():
    '''
    Take and validate suitable input for quantity
    These must be non-negative integers
    '''
    while True:
        user_input = input("")
        try:
            user_int = int(user_input)
            if user_int >= 0:  # Ensure non-negative stock
                return user_int
            else:
                print("\nInput must be non-negative, please try again:")
        except ValueError:
            print("\nInput must be a whole number, please try again:")


def tabulate_shoes(list):
    '''
    Function to display a list of shoe_as_list as readable table
    '''
    table = [["Country", "Code", "Product", "Cost", "Quantity"]]  # Header row
    for shoe in list:
        table.append(shoe.make_list())  # Add shoe rows
    print(tabulate(table))  # Tabulate and display


def ask_if_finished():
    '''
    Called at the end of (most) menu functions so user can exit or return to menu
    '''
    choice = input("\nEnter F to finish, or anything else to return to menu: ")
    if choice.strip().lower() == "f":
        finished()

#==========Main Menu=============

def menu_interaction():
    '''
    Menu function: display options to user, process input and take corresponding action
    '''   

    # dictionary mapping valid user inputs to functions
    main_actions ={
        "r": read_shoes_data,
        "va": view_all,
        "s": search_shoe,
        "v": value_per_item,
        "h": highest_qty,
        "l": re_stock,
        "a": capture_shoes,
        "f": finished
    }

    while True:
        # Present the menu to the user and convert user input to lower case.
        print('''\nThe following options are available:
r  - Re-read inventory file if it has been externally updated
va - View all product lines
s  - Search by product code
v  - Show monetary value of all stock
h  - Identify highest-stock lines to put on sale
l  - Identify and re-stock lines with lowest stock
a  - Record a new product line
f  - Finish''')

        main_choice = input("Please enter your selection: ").strip().lower()

        main_op = main_actions.get(main_choice)

        if main_op == None:
            print("\nUnrecognised selection, please try again")
        else:
            main_op()


#=============Shoe list===========
'''
The list will be used to store a list of objects of shoes.
'''
shoe_list = []

#========= Execute ==========
read_shoes_data()
menu_interaction()
