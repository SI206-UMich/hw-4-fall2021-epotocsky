#name: Lizzie Potocsky
import unittest

# The Customer class represents a customer who will order from the stalls.   
class Customer: 
    #wallet is a float repping how much money in market payment card 
    # Constructor
    def __init__(self, name, wallet = 100):
        self.name = name
        self.wallet = wallet

    # Reload some deposit into the customer's wallet.
    #adds a passed amount to the customer's wallet 
    def reload_money(self, deposit):
        self.wallet += deposit

    # The customer orders the food and there could be different cases   
    #places an order at that cashier to be delivered to that stall
    def validate_order(self, cashier, stall, item_name, quantity):
        if not(cashier.has_stall(stall)):
            print("Sorry, we don't have that vendor stall. Please try a different one.")
        elif not(stall.has_item(item_name, quantity)):  
            print("Our stall has run out of " + item_name + " :( Please try a different stall!")
        elif self.wallet < stall.compute_cost(quantity): 
            print("Don't have enough money for that :( Please reload more money!")
        else:
            bill = cashier.place_order(stall, item_name, quantity) 
            self.submit_order(cashier, stall, bill) 
    
    # Submit_order takes a cashier, a stall and an amount as parameters, 
    # it deducts the amount from the customer’s wallet and calls the receive_payment method on the cashier object
    def submit_order(self, cashier, stall, amount): 
        self.wallet = self.wallet - amount
        cashier.receive_payment(stall, amount)

    # The __str__ method prints the customer's information.    
    def __str__(self):
        return "Hello! My name is " + self.name + ". I have $" + str(self.wallet) + " in my payment card."


# The Cashier class
# The Cashier class represents a cashier at the market. 
class Cashier:

    # Constructor
    #directory is a list of stalls
    def __init__(self, name, directory =[]):
        self.name = name
        self.directory = directory[:] # make a copy of the directory

    # returns whether the stall is in the cashier's directory
    def has_stall(self, stall):
        return stall in self.directory

    # Adds a stall to the directory of the cashier.
    def add_stall(self, new_stall):
        self.directory.append(new_stall)

    # Receives payment from customer, and adds the money to the stall's earnings.
    def receive_payment(self, stall, money):
        stall.earnings += money

    # Places an order at the stall.
	# The cashier pays the stall the cost.
	# The stall processes the order
	# Function returns cost of the order (quantity times cost), using compute_cost method
    def place_order(self, stall, item, quantity):
        stall.process_order(item, quantity)
        return stall.compute_cost(quantity) 
    
    # string function.
    def __str__(self):

        return "Hello, this is the " + self.name + " cashier. We take preloaded market payment cards only. We have " + str(sum([len(category) for category in self.directory.values()])) + " vendors in the farmers' market."

# Complete the Stall class here following the instructions in HW_4_instructions_rubric
#name is a string that is the name of the stall
#inventory is a dictionary which holds the names of the food as the keys and quantities of food as values
#earnings is a float for amount of money the stall currently has
#cost is the cost to each customer for each food. same cost for all foods in the same stall
class Stall:

    def __init__(self, name, inventory = {}, earnings = 0, cost = 7):
        self.name = name
        self.inventory =  inventory 
        self.cost = cost
        self.earnings = earnings
    
    # method that takes the food name and the quantity. 
    # If the stall has enough food, it will decrease the quantity of that food in the inventory. 
    # Questions for you to think about: should process_order take other actions? If so, add it in your code.
    def process_order(self, name, quantity):
        if self.has_item(name, quantity):
            self.inventory[name] -= quantity
        else:
            return "Sorry. The stall does not haeve enough" + str(self.name) + "to complete this order."

  
  # method that takes the food name and the quantity and returns True if there is enough food left in the inventory and False otherwise.

    def has_item(self, name, quantity):
        if name in self.inventory:
            if self.inventory[name] >= quantity:
                return True
            else:
                return False
        else:
            return False

#method that takes the food name and the quantity. 
# It will add the quantity to the existing quantity if the item exists in the inventory dictionary or create a new item in the inventory dictionary with the item name as the key and the quantity as the value.
    def stock_up(self, name, quantity):
        if name in self.inventory:
            self.inventory[name] += quantity
        else:
            self.inventory[name] = quantity


#method that takes the quantity and returns the total for an order. 
#Since all the foods in one stall have the same cost, you only need to know the quantity of food items that the customer has ordered.
    def compute_cost(self, quantity):
        total = quantity * self.cost
        return total

#a method that returns a string with the information in th instnace variables using
#the below format
#“Hello, we are [NAME]. This is the current menu [INVENTORY KEYS AS LIST]. We charge $[COST] per item. We have $[EARNINGS] in total.”
    def __str__(self):
        return "Hello, we are " + str(self.name) + ". This is the current menu: " + str(list(self.inventory.keys())) + ". We charge $" + str(self.cost) + " per item. We have $" + str(self.earnings) + " in total."
    
        


#do not edit test cases besides the ones below
#test_compute_cost has an error. fix the numbers to make the test pass.
#test_has_item tests the has_item method in the Stall class. there are 3 scenarios to test. refer to starter code
#Complete test_validate_order, which tests the validate_order method in the Customer class. 
# The validate_order method places an order of items from a stall to be carried out by a cashier, but only if several conditions are met: 
# if the customer has enough money in their wallet to pay for the transaction and if the stall has enough items in stock.
#when writing tests for test_validate_order, comment each test case describing the scenarios you test
#ex output
#Don't have enough money for that :( Please reload more money! 
# Our stall has run out of [Food Item] :( Please try a different stall! 
# Sorry, we don't have that vendor stall. Please try a different one!
#Complete test_reload_money that tests if the customer can add money into their wallet
class TestAllMethods(unittest.TestCase):
    
    def setUp(self):
        inventory = {"Burger":40, "Taco":50}
        self.f1 = Customer("Ted")
        self.f2 = Customer("Morgan", 150)
        self.s1 = Stall("The Grill Queen", inventory, cost = 10)
        self.s2 = Stall("Tamale Train", inventory, cost = 9)
        self.s3 = Stall("The Streatery", inventory)
        self.c1 = Cashier("West")
        self.c2 = Cashier("East")
        #the following codes show that the two cashiers have the same directory
        for c in [self.c1, self.c2]:
            for s in [self.s1,self.s2,self.s3]:
                c.add_stall(s)

	## Check to see whether constructors work
    def test_customer_constructor(self):
        self.assertEqual(self.f1.name, "Ted")
        self.assertEqual(self.f2.name, "Morgan")
        self.assertEqual(self.f1.wallet, 100)
        self.assertEqual(self.f2.wallet, 150)

	## Check to see whether constructors work
    def test_cashier_constructor(self):
        self.assertEqual(self.c1.name, "West")
        #cashier holds the directory - within the directory there are three stalls
        self.assertEqual(len(self.c1.directory), 3) 

	## Check to see whether constructors work
    def test_truck_constructor(self):
        self.assertEqual(self.s1.name, "The Grill Queen")
        self.assertEqual(self.s1.inventory, {"Burger":40, "Taco":50})
        self.assertEqual(self.s3.earnings, 0)
        self.assertEqual(self.s2.cost, 9)

	# Check that the stall can stock up properly.
    def test_stocking(self):
        inventory = {"Burger": 10}
        s4 = Stall("Misc Stall", inventory)

		# Testing whether stall can stock up on items
        self.assertEqual(s4.inventory, {"Burger": 10})
        s4.stock_up("Burger", 30)
        self.assertEqual(s4.inventory, {"Burger": 40})
        
    def test_make_payment(self):
		# Check to see how much money there is prior to a payment
        previous_custormer_wallet = self.f2.wallet
        previous_earnings_stall = self.s2.earnings
        
        self.f2.submit_order(self.c1, self.s2, 30)

		# See if money has changed hands
        self.assertEqual(self.f2.wallet, previous_custormer_wallet - 30)
        self.assertEqual(self.s2.earnings, previous_earnings_stall + 30)


	# Check to see that the server can serve from the different stalls
    def test_adding_and_serving_stall(self):
        c3 = Cashier("North", directory = [self.s1, self.s2])
        self.assertTrue(c3.has_stall(self.s1))
        self.assertFalse(c3.has_stall(self.s3)) 
        c3.add_stall(self.s3)
        self.assertTrue(c3.has_stall(self.s3))
        self.assertEqual(len(c3.directory), 3)


	# Test that computed cost works properly.
    def test_compute_cost(self):
        #what's wrong with the following statements?
        #can you correct them?
        self.assertEqual(self.s1.compute_cost(5), 50)
        self.assertEqual(self.s3.compute_cost(6), 42)

	# Check that the stall can properly see when it is empty
    def test_has_item(self):
        # Set up to run test cases

        # Test to see if has_item returns True when a stall has enough items left
        # Please follow the instructions below to create three different kinds of test cases 
        # Test case 1: the stall does not have this food item: 
        self.assertFalse(self.s1.has_item("Chocolate", 10))
        # Test case 2: the stall does not have enough food item: 
        self.assertFalse(self.s1.has_item("Taco", 60))
        # Test case 3: the stall has the food item of the certain quantity: 
        self.assertTrue(self.s1.has_item("Burger", 10))


	# Test validate order
    def test_validate_order(self):
		# case 1: test if a customer doesn't have enough money in their wallet to order
        self.assertFalse(self.f1.validate_order(self.c1, self.s1, "Taco", 30))

		# case 2: test if the stall doesn't have enough food left in stock
        self.assertFalse(self.f1.validate_order(self.c1, self.s1, "Burger", 80))

		# case 3: check if the cashier can order item from that stall
        self.assertEqual(self.f1.validate_order(self.c1, self.s1, "Taco", 10), None)

    # Test if a customer can add money to their wallet
    def test_reload_money(self):
        self.assertEqual(self.f2.reload_money(50), 200)
    
### Write main function
def main():
    #Create different objects 
    # Create at least two inventory dictionaries with at least 3 different types of food. 
    inv1 = {"Cheese": 5, "Eggs": 6, "Milk": 4}
    inv2 = { "Apples": 8, "Bananas": 12, "Watermelon": 10}
    # The dictionary keys are the food items and the values are the quantity for each item.
    #Create at least 3 customer objects. 
    customer1 = ("Lizzie", 500)
    customer2 = ("Ellie", 4)
    customer3 = ("Rachel", 150)
    #each should have a unique name and unique amount of money in their wallet
    #create at least 2 stall objects
    stall1 = Stall("Dairy", inv1, 50)
    stall2 = Stall("Fruits", inv2, 10) 
    #each should have a unique name, inventory (use the inventory that you just created), and cost.
    #create at least 2 cashier objects
    #. Each should have a unique name and directory (a list of stalls).

    cashier1 = Cashier("Archie", [stall1, stall2])
    cashier2 = Cashier("Josie", [stall1, stall2])
  

    #Try all cases in the validate_order function
    #Below you need to have *each customer instance* try the four cases
    #case 1: the cashier does not have the stall 
    customer1.validate_order(cashier1, 'Vegetables', 'Carrots', 10)
    customer2.validate_order(cashier1, 'Cheese', 'Mozzarella', 15)
    customer3.validate_order(cashier2, 'Drinks', 'Water', 100)
    
    #case 2: the casher has the stall, but not enough ordered food or the ordered food item
    customer1.validate_order(cashier1, stall1, 'Cheese', 10)
    customer2.validate_order(cashier1, stall2, 'Watermelon', 50)
    customer3.validate_order(cashier1, stall1, 'Milk', 10)
    
    #case 3: the customer does not have enough money to pay for the order: 
    customer1.validate_order(cashier1, stall1, 'Cheese', 5)
    customer2.validate_order(cashier2, stall2, 'Bananas', 1)
    customer3.validate_order(cashier1, stall1, 'Eggs', 3)
    
    #case 4: the customer successfully places an order
    customer1.validate_order(cashier1, stall1, 'Eggs', 1)
    customer2.validate_order(cashier2, stall2, 'Bananas', 2)
    customer3.validate_order(cashier1, stall2, 'Apples', 2)

if __name__ == "__main__":
	main()
	print("\n")
	unittest.main(verbosity = 2)




                  