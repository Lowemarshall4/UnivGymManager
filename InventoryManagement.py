#Marhall Lowe
#Cmpsci 132
#Inventory Management Project

import pickle   #Used in the storing and accessing of object structures as binary in text files
import os       #Used in assertion statements to check if filepaths exist 

'''
Patch Notes:
    Deliverable 2:
        * Changed the freeweight class to just be the weight class and created a dumbbell class that inherits from the weight class and the bar class
        * The View inventory function was changed to a filter inventory function that is similar but just returns location of object with the id 
    Deliverable 3:
        * Changed functions that used to take a univ's inventory as a parameter to making them just accept the univ and then accessing their inv from inside function
        * Updated displayInv function to now display a sorted representation of the items based on their name
        * Condensed the removeFromCart and the removeFromInventory Function into one function to handle both tasks
        * Changed displayInv to displayDict and made it multifunctional enough to display the inventory or the cart
    Deliverable 4:
        * Updated all instances of user input to check validity of entered values and to request that the values be re-entered if they were invalid
        * Added a filepath attibute to my brand class to house the filepath to each college inventory (Used absolute path so it will need changed)
        * Implemted the os library to test if filepaths exist in assert statements
        * Implemented the pickle library to store and retrieve data in files. Pickle is a built in library.
        * Added unit tests
'''

class Brand():
    """Brand class is used to set the colors and logo to equipment of a specific 
        university. It is also used to store the inventory of each
        universities gym equipment"""

    __univs = {"PSU":["Blue and White", "Nittany Lion"], "SHIP":["Blue and Red", "Big Red"], "OSU":["Scarlet and Grey", "Brutus Buckeye"], "PITT": ["Blue and Gold", "Roc the Panther"]}
    def __init__(self, univ):
        self.name = univ
        self.colors = self.__univs[str(univ).upper()][0]
        self.logo = self.__univs[str(univ).upper()][1]
        self.inventory = {}
        self.filePath = 'C:\\Users\\Marshall Lowe\\Desktop\\Cmpsci132\\InvManagement\\{}.txt'.format(self.name)

    def __str__(self):
        return self.name

class Weight(Brand):
    '''Weight class is used to represent any type of freeweight however by default it is for weight plates.
       it takes a mass, material, university, and name attribute and based on mass, its price is calculated using an
       external price_calculator function. it inherits colors and a logo from the Brand class based on univ chosen '''

    def __init__(self, mass, material, univ, name ="Plate"):
        Brand.__init__(self, univ)
        self.name = name
        self.mass = mass
        self.material = material
        self.price = price_calculator(self)
    
    def __str__(self):
        return "\nItem: {}\n\tColor(s): {}\n\tLogo: {}\n\tMaterial: {}\n\tMass: {}\n\tPrice: {}".format(self.name,self.colors,self.logo,self.material,self.mass,self.price)

    def __radd__(self, o):
        return self.price + o

class Bar():
    '''Bar class represents any type of bar and has attributes of mass, length, name and its price is calculated
        through an external price_calculator function '''

    def __init__(self, length, bMass, name):  
        self.bMass = bMass
        self.length = length
        self.name = name
        self.price = price_calculator(self)

    def __str__(self):
        return "\nItem: {}\n\tMass: {}\n\tLength: {}\n\tPrice: {}".format(self.name,self.bMass,self.length, self.price)

    def __radd__(self, o):
        return self.price + o

class Dumbbell(Weight, Bar):
    '''The dummbell class has parameters of mass, material and university. It has a defaulted bar mass, length, and name 
        due to its specificity. Its price is calculated through an external price_calculator function. '''
    def __init__(self, mass, material, univ, length=12, bMass=0, name="Dumbbell"):
        Weight.__init__(self, mass, material, univ)
        Bar.__init__(self, length, bMass, name)
        self.price = price_calculator(self)

    def __str__(self):
        return "\nItem: {}\n\tColor(s): {}\n\tLogo: {}\n\tMaterial: {}\n\tMass: {}\n\tLength: {}\n\tPrice: {}".format(self.name,self.colors,self.logo,self.material,self.mass,self.length,self.price)

    def __radd__(self, o):
        return self.price + o

class Band(Brand):
    '''The band class has parameters of resistance and univ. Its name is defaulted to "Band" and its price is 
        calculated using an external price_calculator function'''
    def __init__(self,resistance,univ,name="Band"):
        super().__init__(univ)
        self.name = name
        self.resistance = resistance
        self.price = price_calculator(self)
    def __str__(self):
        return "\nItem: {}\n\tColor(s): {}\n\tLogo: {}\n\tResistance: {}\n\tPrice: {}".format(self.name, self.colors, self.logo, self.resistance, self.price)

    def __radd__(self, o):
        return self.price + o

class Ball(Brand):
    '''The ball class has parameters of size and university. its name is defaulted to "Ball". Its price is calculated
        using an external price_calculator function'''
    def __init__(self, size, univ, name="Exercise Ball"):
        Brand.__init__(self, univ)
        self.size = size
        self.name = name
        self.price = price_calculator(self)

    def __str__(self):
        return "\nItem: {}\n\tColor(s): {}\n\tLogo: {}\n\tSize: {}\n\tPrice: {}".format(self.name, self.colors, self.logo, self.size, self.price)
    
    def __radd__(self, o):
        return self.price + o


def price_calculator(obj):
    '''edits the price attribute of the given object based on its type'''
    if isinstance(obj, Dumbbell):
        obj.price = obj.mass * 1.5
    elif isinstance(obj, Weight):
        obj.price = obj.mass * 1
    elif isinstance(obj, Bar):
        obj.price = obj.bMass * 2
    elif isinstance(obj, Band):
        if obj.resistance == 'light': obj.price = 2
        elif obj.resistance == 'medium': obj.price = 3
        elif obj.resistance == 'heavy': obj.price = 4
    elif isinstance(obj, Ball):
        if obj.size == 55 : obj.price = 9
        elif obj.size == 65 : obj.price = 10
        elif obj.size == 75 : obj.price = 11
    return obj.price

def addItem(uni, obj):
    '''takes a dict an an object as arguments and adds the object to the dict giving it a key of the next
        number in the sequence of keys already in the dictionary'''
    if len(uni.inventory) > 0:
        iD = max(uni.inventory.keys())+1
        uni.inventory[iD] = obj
    else:
        iD = 1
        uni.inventory[iD] = obj
    print("\n*Adding {} to {} inventory with ID #: {}*\n".format(obj.name, uni, iD ))

def removeItem(dictionary):
    '''Takes a dict and removes the object with the inputed key from the dictionary'''
    if len(dictionary) != 0:
        while True:
            displayDict(dictionary)
            key = input("\nEnter ID of Item to Delete [Enter q to exit item deletion]: ")
            if key.isalpha(): break
            try:
                print(f"\nRemoving {dictionary[int(key)]}....")
                del dictionary[int(key)]
            except:
                print("There Exists no Item with that ID...")
                continue
            else:
                repeat = input("\nWould you like to remove another |Y|N|: ").upper()
                if repeat == 'N': break
    else:
            print("It is Empty!")
        
def displayDict(dictionary):
    '''Takes a dict as a parameter and prints out all of the objects in the dictionary with their associated key'''
    if len(dictionary) != 0:
        for k, v in sorted(dictionary.items(), key=lambda x: x[1].name):
            print(f"\nID: {k}" , v)
    else: print("\nIt is Empty!")
        
def filterInv(uni):
    '''Given a university, it will display a filtered inventory of what the university has based on the name of equipment given'''
    key = input("Enter name of items you'd like to view: ").title()
    filtered = {}
    for k, obj in uni.inventory.items():
        if obj.name == key:
            filtered[k] = obj
    return filtered

def addToCart(uni,cart):
    '''Takes a original dict, a key, and a new dict as parameters and copies the item of the key from the old dict to the new dict'''
    while True:
        displayDict(uni.inventory)
        key = input("\nEnter ID of Item to Add to Cart [Enter q to exit adding items]: ")
        if key.isalpha(): break
        try:
            cart[int(key)] = uni.inventory[int(key)]
        except: 
            print("There Exists no Item with that ID...")
        else:
            repeat = input("Would You Like to Add Another? |Y|N|: ").upper()
            if repeat == "N": break

def getTotal(dictionary):
    '''Returns the total price of all the items in the given dict'''
    return sum(dictionary.values())

def getUniv(univs):
    '''Allows user to select different universities inventories. When switching universities, cart is cleared.'''
    global cart
    cart = {}
    print("Enter Number Of Desired University to Access Their Gym Inventory")
    for i, uni in enumerate(univs):
        print("\t{} : {}".format(i, uni))
    while True: 
        try:
            chosenUni = int(input("> "))
            return univs[chosenUni]
        except:
            print("Please Select a Valid University....")
        else:
            break

def createFreeweight(uni):
    '''Given a university, it goes through prompts to create and return a Weight Object'''
    masses = [5, 10, 25, 35, 45]
    materials = ['Metal', 'Rubber']
    name = input("Enter Name of Freeweight(Plate, Kettleball, etc): [Enter q to exit creating]\n> ").title()
    if name != "Q":
        while True:
            try:
                print("Select a mass:\n\t1: 5\n\t2: 10\n\t3: 25\n\t4: 35\n\t5: 45")
                mass = masses[int(input("> "))-1]
                print("Select a material:\n\t1: Metal\n\t2: Rubber")
                material = materials[int(input("> "))-1]
            except:
                print("Please select an available option...")
                continue
            else:
                break
        return Weight(mass, material, uni, name)
    else: return None

def createBar():
    '''Goes through prompts and returns a bar object'''
    bars = ['Barbell', 'Curl Bar', 'Swiss Bar']
    while True:
        try:
            print("Please select type of bar [Enter q to exit creating]: ")
            print("\t1: Barbell\n\t2: Curl Bar\n\t3: Swiss Bar")
            barType = bars[int(input("> "))-1]
        except IndexError:
            print("Please select an available option...")
            continue
        except ValueError:
            return None
        else:
            if barType == 'Barbell': return Bar(7.2, 45, 'Barbell')
            if barType == 'Curl Bar': return Bar(4, 15, 'Curlbar')
            if barType == 'Swiss Bar': return Bar(7, 35, 'Swiss Bar')

def createDumbell(uni):
    '''Given a university, it goes through prompts to create and return a Dumbbell Object'''
    mass = 0
    materials = ['metal', 'rubber']
    while True:
        try:
            mass = int(input("Enter mass of dumbbell [Enter q to exit creating]:\n> "))
            print("Select a material:\n\t1: Metal\n\t2: Rubber")
            material = materials[int(input("> "))-1]
        except IndexError:
            print("Please select an available option...")
        except ValueError:
            return None
        else:
            break
    return Dumbbell(mass, material, uni)

def createBand(uni):
    '''Given a university, it goes through prompts to create and return a Band Object'''
    resistances = ['light', 'medium', 'heavy']
    while True:
        try:
            print("Choose a resistance [Enter q to exit creating]")
            print("\t1: Light\n\t2: Medium\n\t3: Heavy")
            resistance = resistances[int(input("> "))-1]
        except IndexError:
            print("Please select an available option...")
        except ValueError:
            return None
        else: 
            break
    return Band(resistance, uni)

def createBall(uni):
    '''Given a university, it goes through prompts to create and return a Ball Object'''
    sizes = [55, 65, 75]
    print("Choose a diameter [Enter q to exit creating]")
    while True:
        try:
            print("\t1: 55 cm\n\t2: 65 cm\n\t3: 75 cm")
            size = sizes[int(input("> "))-1]
        except IndexError:
            print("Please select an available option...")
        except ValueError:
            return None
    return Ball(size, uni)

def createItem(uni):
    '''Given a univeristy, it prompts user to select what kind of item to create
        and then passes the user to the appropriate function for the creation of said item
        and then adds the item to the university inventory'''
    while True:
        print("\nWhat kind of item would you like to add to the inventory?")
        print("\t0: Exit Item Adding\n\t1: Dumbbell\n\t2: Freeweight(Plates, Kettleballs, etc)\n\t3: Bar\n\t4: Resistance Band\n\t5: Exercise Ball")
        try:
            choice = int(input("> "))
        except:
            print("Please select an available option...")
        else:
            if choice == 0: break
            elif choice == 1: item = createDumbell(uni)
            elif choice == 2: item = createFreeweight(uni)
            elif choice == 3: item = createBar()
            elif choice == 4: item = createBand(uni)
            elif choice == 5: item = createBall(uni)
            else: continue
            if item != None: addItem(uni, item)
            
def checkout(uni):
    '''Displays the items in the cart and totals their costs. If user completes
        the purchase then the items are removed from the inventory and
         the global cart dictionary is cleared'''
    global cart
    print("Items In Your Cart:")
    displayDict(cart)
    print("\nTotal Cost: {}".format(getTotal(cart)))
    done = input("Would You Like To Complete The Purchase? |Y|N|: ").upper()
    if done == 'Y':
        for iD in cart.keys():
            del uni.inventory[iD]
        cart = {}

def mainMenu():
    '''Displays options for main menu and returns choice as an int'''
    print("0: Exit Program\n1: Select Different University\n2: Inspect Inventory\n3: Filter Inventory\n4: Add Item to Inventory\n5: Remove Item from Inventory\n6: Inspect Cart\n7: Add Item to cart\n8: Remove Item from Cart\n9: Checkout ")
    while True:
        try:
            return int(input("> "))
        except:
            print("Please select an available option...")

def loadInv(invFile):
    '''Loads the binary data of a "pickled" object structure from a file and returns the object structure'''
    with open(invFile, 'rb') as f:
        return pickle.load(f)

def updateInv(invFile, data):
    '''Stores the data of an inventory in a text file as binary. 
        Useful fo direct storage of object structures'''
    with open(invFile, 'wb') as f:
        pickle.dump(data, f)


psu = Brand("PSU")
ship = Brand("SHIP")
osu = Brand("OSU")
pitt = Brand("PITT")

univs = [psu, ship, osu, pitt,]
uni = getUniv(univs)
cart = {} 


try:
    uni.inventory = loadInv(uni.filePath)
except:     #If the file is empty and/or there is no file
    uni.inventory = {}
    updateInv(uni.filePath, {}) #Creates File for inventory


assert len(uni.inventory) == len(loadInv(uni.filePath))
assert len(cart) == 0
assert getTotal(uni.inventory) == getTotal(loadInv(uni.filePath))
assert uni in univs
assert os.path.exists(uni.filePath)


while True:
    print("\nWelcome to {}'s gym inventory management system".format(uni))
    updateInv(uni.filePath, uni.inventory)
    choice = mainMenu()
    if choice == 0: break
    elif choice == 1:
        uni = getUniv(univs)
        try:
            uni.inventory = loadInv(uni.filePath)
        except EOFError:
            uni.inventory = {}
    elif choice == 2: displayDict(uni.inventory)
    elif choice == 3: displayDict(filterInv(uni))
    elif choice == 4: createItem(uni)
    elif choice == 5: removeItem(uni.inventory)
    elif choice == 6: displayDict(cart)
    elif choice == 7: addToCart(uni, cart)
    elif choice == 8: removeItem(cart)
    elif choice == 9: checkout(uni)



