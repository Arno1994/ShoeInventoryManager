from tabulate import tabulate

class Shoes:
    """Class for the shoes will use the country name, product name, cost of the shoe and quantity in stock
    in the constructor where 3 class methods are defined. The get_cost method will take the cost of the
    object and convert it to a float and eturn the cost. The get_quantity method will get the quantity of
    the object and convert it to a integer. The __str__ method will return a defined string when the method
    is called for the object."""
    def __init__(self, country, code, product, cost, quantity):
        self.country = country
        self.code = code
        self.product = product
        self.cost = cost
        self.quantity = quantity

    def get_cost(self):
        shoe_cost = float(self.cost)
        return shoe_cost

    def get_quantity(self):
        shoe_quantity = int(self.quantity)
        return shoe_quantity

    def __str__(self):
        return f'{self.country}, {self.code}, {self.product}, {self.cost}, {self.quantity}'

def read_shoes_data():
    """ The read_shoes_data function will open the inventory.txt file and for every line strip the spaces
    and create a new list (line_list) from the split function. The new list s used in 2 places:
    Firstly it saves each line_list for every line to a list called shoe_table_list and secondly every index
    of each line_list is used to make a Shoe object from the Shoes Class. Some error handling is used to
    inform the user if the file is missing. Lastly the headings from the txt file are removed from the list
    that contains the shoes objects."""
    try:
        with open('inventory.txt', 'r') as shoes:
            for line in shoes:
                line_strip = line.strip()
                line_list = line_strip.split(",")
                shoe_table_list.append(line_list)
                shoes_list.append(Shoes(line_list[0], line_list[1], line_list[2],\
                                     line_list[3], line_list[4]))
    except FileNotFoundError:
        print("The inventory.txt file could not be found")
    except IndexError:
        print("Faulty data in file")

    shoes_list.pop(0)

def capture_shoes():
    """In this function user validation is used to ensure the user does not add a new shoe by accident.
    Boolean variables are defined to use in while loops for user valdation for the entry off every detail
    of the new shoes to be registered. The new shoes details are put into the Shoes class to create a new
    object and added to the shoes_list. Additonally the shoe_table_list is also appended with the new shoe
    details. List are appended to enssure they are updated if users want to use the view_all function."""
    # Boolean varables to be used for user validation
    country_check =  False
    code_check = False
    product_check = False
    cost_check = False
    quantity_check = False
    user_exit_check = False
    # Ask user for inputs and validate
    while user_exit_check == False:
        user_exit = input("You have chosen to capture a new shoe item to the system.\n"\
                          + "Do you want to continue? Y = Yes, N = No:")
        if user_exit.upper() == "Y":
            user_exit_check = True
        elif user_exit.upper() == "N":
            break
        else:
            print("Invalid input. Please try again.")
    while country_check == False:
        shoe_country = input("Please provide the country for the shoes:")
        if len(shoe_country) == 0:
            print("No country provided. Please try again.\n")
        else:
            country_check = True
    while code_check == False:
        shoe_code = input("What is the product code of the shoe you want to capture?:")
        # Make sure the code is 8 characters long
        if len(shoe_code) != 8:
            print("Incorrect code was provided. Please try again.\n")
        else:
            code_check = True
    while product_check == False:
        shoe_product = input("Please provide the product name:")
        if len(shoe_product) == 0:
            print("No name was provided. please try again.\n")
        else:
            product_check = True
    while cost_check == False:
        try:
            shoe_cost = int(input("What is the price of the shoes?:"))
            cost_check = True
        except ValueError:
            print("Invalid input. Please provide only the price.\n")
    while quantity_check == False:
        try:
            shoe_quantity = int(input("Please provide quantity of shoes:"))
            quantity_check = True
        except ValueError:
            print("Invalid input. Please provide only the quantity.\n")

    shoe_details = Shoes(shoe_country, shoe_code, shoe_product, shoe_cost, shoe_quantity)
    shoes_list.append(shoe_details)
    shoe_table_list.append([shoe_country, shoe_code, shoe_product, shoe_cost, shoe_quantity])
    # New string to add new shoe details to the inventory.txt file
    shoe_detail_string = shoe_country + "," + shoe_code + "," + shoe_product + "," +\
                        str(shoe_cost) + "," + str(shoe_quantity) + "\n"
    # Append inventory.txt for new shoe 
    with open('inventory.txt', 'a') as shoes:
        shoes.write(shoe_detail_string)
    print("New shoe has been registered.\n")

def view_all():
    # Take the shoe_table_list and create a table using tabulate
    print(tabulate(shoe_table_list, headers = 'firstrow', tablefmt = 'fancy_grid'))

def re_stock():
    """ In this function the program will loop through the list containing all the shoes objects
    and convert every quantity variable of each into an integer and save them to the shoe_quantity_list.
    Using the min function on the shoe_quantity_list to find the minmum and save the minimum to a variable.
    The program will loop through the quantity list and check if the quantity of each object matches the minimum
    and the count variable will represent the index value. Every shoe that matches will be shared to the user.
    The user will then be asked if they want to adjust the stock and input is validated."""
    shoe_quantity_list = []
    count = 0
    for shoe in shoes_list:
        shoe_quantity_list.append(int(shoe.quantity))
    min_quantity = min(shoe_quantity_list)
    for item in shoe_quantity_list:
        if item == min_quantity:
            user_check = False
            while user_check == False:
                user_stock = input(f"""============Stock low warning!============
{shoes_list[count].product} with product code: {shoes_list[count].code} is low.
Stock is currently at: {item}
Do you want to update the stock?
(Y/N):""")
                if user_stock.upper() == "Y":
                    input_check = False
                    while input_check == False:
                        # Try/Except used to validte the input and ensure a number is entered
                        try:
                            user_stock_add = int(input("How much stock do you want to add?:"))
                            input_check = True
                        except ValueError:
                            print('Invalid Input. Please try again.')
                    # Replace value at specific index for the shoe object
                    shoes_list[count].quantity = str(int(shoes_list[count].quantity)\
                                                     + user_stock_add)
                    user_check = True
                elif user_stock.upper() == "N":
                    user_check = True
                else:
                    print("Invalid input. Please try again")
        else:
            # Do nothing if it does not match the min
            pass
        count += 1
    # Clear the inventory.txt file and rewrite all information with new stock for the item
    with open('inventory.txt', 'w') as shoes:
        shoes.write("Country,Code,Product,Cost,Quantity\n")
        for item in shoes_list:
            shoes.write(item.country + "," + item.code + "," + item.product + ","\
                        + str(item.cost) + "," + str(item.quantity) + "\n")
def search_shoe():
    """ This function will ask the user for a specific product code where input is validated.
    The function will loop through the shoes_list and will notify and display the found
    product. If product is not found the user is also notiied"""
    found_product = "None"
    search_check = False
    while search_check == False:
        shoe_search_input = input("Please give the code for the shoe you want to find:")
        if len(shoe_search_input) == 8:
            print("Valid product code has been entered.")
            search_check = True
        else:
            print("Code provided is not valid. Please try again")
    for shoe in shoes_list:
        if shoe.code == shoe_search_input:
            print("Product has been found.")
            found_product = shoe
        else:
            pass
    if found_product == "None":
        print("The product could not be found in the inventory list. Please try again.")
    return found_product

def value_per_item():
    """This function will calculate the total cost of each shoe object using the get_cost
    and get_quantity methods. The details of every shoe object and the calculation are saved to
    the item_list and displayed using tabulate"""
    value_list = [["Product", "Code", "Cost (R)", "Quantity", "Total Value (R)"]]
    for shoe in shoes_list:
        product = shoe.product
        code = shoe.code
        cost = shoe.get_cost()
        quantity = shoe.get_quantity()
        value = cost * quantity
        item_list = [product, code, str(cost), str(quantity), str(value)]
        value_list.append(item_list)
    print(tabulate(value_list, headers = 'firstrow', tablefmt = 'fancy_grid'))

def highest_qty():
    """ In this function the program will loop through the list containing all the shoes objects
    and convert every quantity variable of each into an integer and save them to the shoe_quantity_list.
    Using the max function on the shoe_quantity_list to find the maximum and save it to a variable.
    The program will loop through the quantity list and check if the quantity of each object matches the maximum
    and the count variable will represent the index value. Every shoe that matches will be shared to the user
    and declared to be on sale."""
    shoe_quantity_list = []
    count = 0
    for shoe in shoes_list:
        shoe_quantity_list.append(int(shoe.quantity))
    max_quantity = max(shoe_quantity_list)
    for item in shoe_quantity_list:
        if item == max_quantity:
            print(f"""============Shoes on Sale!============
{shoes_list[count].product} with product code: {shoes_list[count].code} is for sale!
Stock is currently at: {item}
""")
        else:
            # Do nothing if it does not match the max
            pass
        count += 1

# Main code section
# Create empty lists to be used by functions
shoes_list = []
shoe_table_list = []
# Run read_shoes_data function to populate the lists
read_shoes_data()
print("Welcome to your inventory managment system.")
# Get and validate user input and run the appropriate function based on user input 
while True:
    # Menu to be showed to user
    user_input = input("""What would you like to do?
1. Add new shoe to the inventory
2. Show inventory
3. Check stock for lowest inventory
4. Search for a shoe using the shoe code
5. Show value of every item in stock
6. Check for product with highest stock to put on sale
7. Exit the program

Please select the number of your choice:""")
    if user_input == "1":
        capture_shoes()
    elif user_input == "2":
        view_all()
    elif user_input == "3":
        re_stock()
    elif user_input == "4":
        # Use the object that is returned and print out the details for the user
        search_result = search_shoe()
        print(f"""The following shoe was found:
Shoe: \t\t{search_result.product}
Country: \t{search_result.country}
Cost: \t\t{search_result.cost}
Quantity: \t{search_result.quantity}
""")
    elif user_input == "5":
        value_per_item()
    elif user_input == "6":
        highest_qty()
    elif user_input == "7":
        exit()
    else:
        print("Invalid input. Please try again.\n")




            
