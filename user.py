import string
import random
import datetime
import prod_cart_module

class Person:
    __nbPersons = 0
    def __init__(self,userid,pwd):
        self.id = userid
        self.__pwd = pwd
        Person.__nbPersons +=1
    def __str__(self):
        result = ("User ID: " + str(self.id)) + '\n'
        result += ("User password: " + str(self.__pwd))
        return result
    @staticmethod # no need to provide self as an argument here, since nbPersons is class variable
    def getNumPersons():
        return "There are "+ str(Person.__nbPersons) + ' ' + "instances of the class Person!"
    def getPwd(self):
        return self.__pwd
    def changePwd(self, oldpwd, newpwd):
        if oldpwd == self.__pwd:
            self.__pwd = newpwd
        else:
            print("Wrong password!")
    def resetPwd(self):
        self.__pwd = ''.join(random.choices(string.ascii_uppercase + string.digits + string.ascii_lowercase, k=10))


class Customer(Person):
    __nbCustomers = 0
    key = []
    q = []
    signal = False
    l_s = None


    def __init__(self,userid,pwd):
        Customer.__nbCustomers += 1
        self.joinedSince = datetime.datetime.now()
        self.a = []
        super().__init__(userid,pwd)

    def __str__(self):
        result = "\nCustomer profile: " + '\n'
        result += 'The object was created at: ' + str(self.joinedSince) + '\n'
        result += super().__str__()
        return result
    @staticmethod
    def getNumCustomers():
         return "There are " + str(Customer.__nbCustomers) + ' ' + "instances of the class Customer!"

    def addProduct(self,product,qty):
        self.a.append(prod_cart_module.CartLine(product, qty)) # here we create an object of Cart Line class and append it to the list
        i = len(self.a)
        t = 0
        for x in range(i):
            self.a[t] = str(self.a[t]) + "\n" # we convert object description to the string type, so it will be a list of strings
            t+=1
        Customer.key.append(product) # codes list
        Customer.q.append([qty,product]) # codes and quantity list

        

    # two special class methods to access the lists  
    @classmethod
    def getK(cls):
        return Customer.key
    @classmethod
    def getQ(cls):
        return Customer.q

    def viewCart(self): # here we add only Cart Line object, the crucial transformation is happening in main module
        p = ""  # we will add each string represantation of the Cart Line here
        for x in self.a:
            p+=x
        result = "\nCustomer profile: " + '\n'
        result += 'The object was created at: ' + str(self.joinedSince) + '\n'
        result += super().__str__() + "\n" # this is str of Person
        result += "\nShopping Cart:" + "\n" + "------------\n"
        result += "\n" + p + "\n"
        return result
    @classmethod
    def c_v(cls,v):
        cls.l_s = v
    @classmethod
    def getS(cls):
        return cls.signal

    def removeProduct(self, product):
        for x in Customer.key:
            if x == product:
                Customer.key.remove(x)
        for y in Customer.q:
            if y[1] == product:
                Customer.q.remove(y) # we are removing the data from the lists
        Customer.c_v(product)
        for q in self.a:
            if product in q:
                self.a.remove(q)

    def clean_the_cart(self): # here we will delete every record from the lists
        self.a.clear()
        Customer.q.clear()
        Customer.key.clear()
    

    def updateQ(self, prod, qua): # addtional method to update a quantity
        z = 0
        for i in Customer.q:
            if i[1] == prod:
                z+=i[0]
        for x in Customer.q:
            if x[1] == prod:
                x[0] += qua
        # so qua is new quantity and z is an old quantity, then we sum them up

        t = 0
        for y in range(len(self.a)): # here we update a lists of the strings by creating new Cart Line object and removing the old one if it includes the product code
            if prod in self.a[t]:
                self.a.remove(self.a[t])
                self.a.append(prod_cart_module.CartLine(prod, qua+z))
                self.a[t] = str(self.a[t]) + "\n"
                t+=1
  
        

                
                
            
            
        

                



      


    

