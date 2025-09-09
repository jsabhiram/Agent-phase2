class Inventory:
    def __init__(self,ls):
        self.itemname=ls.get('itemname')
        self.price=ls.get('price')
        self.quantity=ls.get('quantity',1)
        self.country=ls.get('country')
        self.vendor=ls.get('vendor')
        self.hsn=ls.get('hsn',0)
        self.risk=0 # indicates the risk level of product scales from 1,2,3,4,5

    