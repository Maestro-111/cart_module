
class Product(object):
    def __init__(self,pcode,pdesc,price,qoh=0,discount=0):
        self.pcode = pcode
        self.pdesc = pdesc
        self.price = price
        self.qoh = qoh
        self.discount = discount
    def getCode(self):
        return self.pcode
    def getDesc(self):
        return self.pdesc
    def getPrice(self):
        return self.price
    def QOH(self):
        return self.qoh
    def getDiscount(self):
        return self.discount
    def updateQOH(self, qty):
        self.qoh = qty
    def updatePrice(self, newprice):
        self.price = newprice
    def updateDiscount(self, newdiscount):
        self.discount = newdiscount
    def __str__(self):
        result = "|" + str(self.pdesc) + "%10s" % " " + "|"
        result += str(self.price) + " " + "|"
        result += str(self.qoh) + " " + "|"
        result += str(self.discount) + "\n"
        return result
class CartLine(object):
    def __init__(self,product,qty):
        self.product = product
        self.qty = qty
    def updateQTY(self, newqty):
        self.qty = newqty
    def __str__(self):
        result = "Code: " + str(self.product) + " "
        result += "Quantity: " + str(self.qty)
        return result
    def __repr__(self):
        result = str(self.product) + " "
        result += str(self.qty) + " "
        return result
