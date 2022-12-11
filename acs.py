import user
import prod_cart_module

class ACS(object):
    """This class represents terminal-based customer service events."""
    SECRET_CODE = "bye"
    
    ################ Constructor ##################### 
    def __init__(self):
        self.detect = True
        self._customer = None
        self._products={} # list of products available to display to the user
        self._methods = {}          # Jump table for commands
        self._methods["1"] = self._viewProducts
        self._methods["2"] = self._addProduct        
        self._methods["3"] = self._removeProduct
        self._methods["4"] = self._viewCart        
        self._methods["5"] = self._clearCart
        self._methods["6"] = self._updateQuan
        self._methods["7"] = self._quit
        self.__loadProducts()
    
    def __loadProducts(self):
        """ creates a set of 4 products added to _products dictionary. 
        the Product class in the prod_cart_mod module should be defined. 
        """
        p1= prod_cart_module.Product('11QER/31', 'Power painter, 15 psi., 3-nozzle', 120, 8, 20)
        p2= prod_cart_module.Product('13-Q2/P2', '7.25-in. pwr. saw blade', 80, 32)
        p3= prod_cart_module.Product('14-Q1/L3', '9.00-in. pwr. saw blade', 70, 18)
        p4= prod_cart_module.Product('1546-QQ2', 'Hrd. cloth, 1/4-in., 2x50', 100, 15)
        self._products[p1.getCode()]= p1
        self._products[p2.getCode()]= p2
        self._products[p3.getCode()]= p3
        self._products[p4.getCode()]= p4       

    ################ run main menu #####################     
    def run(self):
        """Logs in customers and processes their accounts."""       
        while True:
            if self.detect == False:
                break
            beginning = ACS.choice()
            if beginning == "1":
                cond = ACS.register()
                if cond == -3:
                    break
            elif beginning == "2":
                pass
            userid = input("Enter your user id: ")
            if userid == ACS.SECRET_CODE:
                break
            pwd = input("Enter your PASSWORD: ")
            self._customer = self._authenticateUser(userid, pwd)
            if self._customer == -1:
                break
            if self._customer == -2:
                break
            if self._customer == None:
                print("Error, incorrect userid or password")
            else:
                print(self._customer)
                self._processCustomerAccount()
                
                
   ################ view all products #####################     
    def _viewProducts(self):
        """print the list of all products on the screen. Use the print function """
        for key,value in self._products.items(): # here we just print the codes, which are keys in the dictionary and values which are just objects Product with a defined str method
            print(key,value)
            
    ################ authenticate user in DB  #####################     
    def _authenticateUser(self, userid, pwd):
        """ this method will authenticate the user and returns the customer object. 
        You may consider to read from a text file and search for the given userid and password
        If found, create a new customer object."""
        subFlag1 = False
        subFlag2 = False
        z1 = []
        z2 = []
        q = []
        p = []
        try: # here we just verify the file name
            c = open("list.txt", 'r', encoding = 'utf-8')# we can try to implement "empry_list" which is empty database, or txt file
        except FileNotFoundError:
            print("Wrong database name!")
            return -2

            
        
        try: # the first try block, where we verify that database, or txt, file is not empty. If it is, program stops working.
            for line in c:
                y = line.split()
                q.append(y)
            del q[0]
        except IndexError:
            print("Empty database") # we can try to implement "empry_list" which is empty database
            return -1
        finally:
            print("\nBlock finally is always done")

        try: # the second try block, where we catch ValueError, that indicates that we have more id's than passwords or visa versa, in our database. If such thing happens, we analyse such id or password separetly.
            qq = dict(q)
        except ValueError as v:
            print("\n",v)
            for x in q:
                if len(x)<2: # each list that is less than 2 is separeta Id or password, so we cannot do dict(q). Hence, we need to analyze each list of len 1 separetly.
                    p.append(x)
            for s in p:
                q.remove(s)

            for y in p:
                if userid in y:
                    subFlag1 = True
                if pwd in y:
                    subFlag2 = True
            qq = dict(q) # since we removed list of size 1, we can now do dict(q)

        for key,value in qq.items():
            z1.append(key)
            z2.append(value)
        if userid in z1:
            subFlag1 = True
        if pwd in z2:
            subFlag2 = True

        if subFlag1 == True and subFlag2 == True: # here we are analysing the outcome, basically what should we return or print
            self._customer = user.Customer(userid,pwd)
            return self._customer
        elif subFlag1 == False and subFlag2 == True:
            print("\nWrong ID!\n")
        elif subFlag2 == False and subFlag1 == True:
            print("\nWrong PWD!\n")
        elif subFlag2 == False and subFlag1 == False:
            print("\nWrong ID and password\n")

            

  
    ################ process customer account #####################      
    def _processCustomerAccount(self):
        """A menu-driven command showing the options to view all products, 
        add a product in the cart, remove a product from the cart, view the cart. 
        or quit. Given the user-entered option, the corresponding method should be 
        called from self._methods.
        if the option is not recognized, print a message with the text:' unrecognized number. 
        Refer to the sample execution output for more about functionalities.
        """
        while True: # simple while True loop to display the menu
            print("\nMain menu:\n")
            print("1 to view all products\n")
            print("2 to add the product\n")
            print("3 to remove the product\n")
            print("4 to view your chart\n")
            print("5 to clean your chart\n")
            print("6 to update the quantity of the product\n")
            print("7 to quit\n")
            num = input("Enter the number: ")
            theM = self._methods.get(num, None)
            if theM == None:
                    print("\nWrong Number\n")
            else:
                theM()
                if self._customer == None:
                    break
        
        
        

    ################ add product #####################
    def _addProduct(self):
        """ prompt the user for a product code to add to the cart and the quantity. 
        print a message on the screen, that the product was added to the cart, 
        out of stock or invalid. 
        """
        num = input("Enter the product code: ")
        mun = int(input("Enter the quantity: "))

        if num not in self._products.keys(): # if code is not in the keys of dictionary it is invalid
            print("\nInvalid Product")
        elif mun < 0:
            print("Value is less than 0") # if users enters quenatity less than 0 it is invalid
        else:
            o = self._products[num] # here we just access the properties of product, like quantity 
            if o.qoh < mun:
                print("\nInvalid number") # if we have quantity less than users number
            else:
                o.qoh -= mun # else we are substracting the quantity
                b = self._customer
                b.addProduct(num,mun)
                print("\nProduct added to chart")
            
        
        
    ################ _viewCart #####################
    def _viewCart(self): 
        """ display what is in the cart. 
        """
        total = 0
        b = self._customer
        c = b.viewCart()
        z = user.Customer.getK() # here we are just accessing the list which includes the codes of the products in the cart
        zz = user.Customer.getQ()# here we are just accessing the list which includes the codes of the products in the cart and their quantities
        t = 0 # these are indexes for the processing lists via for loop
        tt = 0
        ttt = 0
        for code in range(len(z)): # within this loop we display info about products and actual sums for the transactions
            if z[t] in self._products.keys():
                o = self._products[z[t]] # product code
                price = o.getPrice() # price
                discount = o.getDiscount() / 100 # dicsount
                quantit = zz[tt] # it is a list in a list, like [[15,11QER]] and quantit is [15,11QER]
                quantity = quantit[ttt] # entered quantity, since the index of a quantity in the list with length 2 is 0 and ttt is 0
                tot = str((price - (price * discount)) * quantity)
                total_plus = (price - (price * discount)) * quantity
                x = str(self._products[z[t]])
                x = x.replace("|", "")
                c+= "-----------------\n" + "Product specification: \n" + x + "\n"
                c += "Amount for " + str(t+1) + " transaction: " + tot + "\n"

                total += total_plus
                t+=1
                tt+=1
        c += "-----------------"
        c += "\nOverall total amount: " + str(total) + "\n"     
        print(c)

        
    ################ _removeProduct #####################
    def _removeProduct(self):
        """ prompt the user for the product code that needs to be removed from the cart.
        print a message whether the product was removed from the card or the product code is invalid.
        """
        code = input("Enter the code: ")
        if code not in user.Customer.getK():
            print("\nNo such product in the cart!\n")
        elif code not in self._products.keys():
            print("\nInvalid Product")
        else:
            zz = user.Customer.getQ()
            o = self._products[code]
            this_q = 0
            for x in zz: # here we will return a quantity to the initial point
                if x[1] == code:
                    this_q += x[0]
            # this_q are summed quantites within all transactions with this product code        
            o.qoh += this_q
            b = self._customer
            b.removeProduct(code)
            print("\nProduct was removed")
            
    def _clearCart(self): # additional method to remove ALL products from the cart
        b = self._customer
        z = user.Customer.getK()
        zz = user.Customer.getQ()
        for x in zz:
            for y in z:
                if y == x[1]: # is two products codes are equal in the lists, we add a corresponding qunatity for that transaction to the correspoinding product via the code
                    o = self._products[y]
                    o.qoh += x[0]
            
        b.clean_the_cart()
        print("\nAll products were removed from the Cart!\n")

    def _updateQuan(self): # additional method to update a quantity for the exsiting code in the cart
        a = input("Enter the product: ")
        sec_key = user.Customer.getK()
        if a not in sec_key:
            print("\nNot reckognized product code!\n")
        else:
            o = self._products[a]
            c = int(input("Enter the quantity: "))
            if o.qoh < c:
                print("\nInvalid number\n")
            else:
                b = self._customer
                b.updateQ(a, c)
                o.qoh -= c
                print("\nQuantity was updated\n")
    
    @staticmethod            
    def choice():
        print("Main Menu\n")
        print("Enter 1 to register\n")
        print("Enter 2 to log in\n")
        a = input("Here: ")
        while a != "1" and a != "2":
            print("Print 1 or 2!\n")
            a = input("Here: ")
        return a
    
    @staticmethod 
    def register():
        try:
            words = []
            c = open("list.txt", 'r', encoding = 'utf-8')
            for x in c:
                words.append(x)
            del words[0]
            for x,y in enumerate(words):
                words[x] = words[x].strip("\n")
            c.close()
            print("Registration!\n")
            c = open("list.txt", 'a', encoding = 'utf-8')
        except FileNotFoundError:
            print("Wrong database name!")
            return -3
        def user_i(words):
            detect = False
            while detect == False:
                a = input("Enter your new ID: ")
                u = input("Enter your new password: ")
                check = a
                for x in words:
                    if check in x:
                        print("\nThis ID is occupied!\n")
                        print("Reenter your credentials!\n")
                        detect = False
                        break                    
                    else:
                        detect = True            
            return [a,u]

        info = user_i(words)


        c.write("\n" + info[0] + " " + info[1])
        c.close
        print("Thank you, registration is done!\n")        
            
    ################ quit #####################      
    def _quit(self):
        """ Assigns none to the current customer object, and print a message saying ' Have anice day!' 
        """
        self._customer = None
        self.detect = False
        print("\nHave a nice day!\n")
################ TESTING #####################      
def main():
    acs=ACS() # creating ACS object
    acs.run()

main()
