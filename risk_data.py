
from mdb import extract_all_details as gather

class Inventory:
    def __init__(self,ls):
        self.itemname=ls.get('itemname')
        self.price=ls.get('price')
        self.quantity=ls.get('quantity',1)
        self.country=ls.get('country')
        self.vendor=ls.get('vendor')
        self.hsn=ls.get('hsn',0)
        self.unit=ls.get('unit','units')
        self.risk=0
        self.risk_details=""


    def vendor_fn(self,vendors):
        if self.vendor in vendors:
            self.risk+=1
            self.risk_details+=f'Exact match in vendor watchlist-{self.vendor} \n'
        else:
            pass

    def country_fn(self,countries):
        if self.country in countries:
            self.risk+=1
            self.risk_details+=f"Country is flagged {self.country}\n "
        else:
            pass
    def hsn_fn(self,hsn):
        if self.hsn in hsn:
            self.risk+=1
            self.risk_details+=f"HSN code flagged :{self.hsn}\n"
        else:
            pass

    def quantity_fn(self,pair):
        name=self.itemname
        if name in pair.keys():
            # print("Entered")
            a=pair[name]['unit']
            # print(a)
            if a == self.unit:
                
                b=(pair[name]['max_quantity'])
                if (self.quantity)>b:
                    self.risk+=1
                    self.risk_details+=f"Quantity limit exceeded by {self.quantity-b} {self.unit}\n"



'''
✅ Extracted 1 products
[{'itemname': 'Sadow LAN Cable 25 m', 'quantity': 1, 'vendor': 'SADOW TECHNOLOGIES', 
'goods/HSN': '85177090', 'price': 480.0, 'country': 'IN'}]
🔎🔎🔎🔎🔎Debugging {'itemname': 'Sadow LAN Cable 25 m', 'quantity': 1, 
'vendor': 'SADOW TECHNOLOGIES', 'goods/HSN': '85177090', 'price': 480.0, 'country': 'IN'}
🔎🔎🔎🔎🔎Debugging {'itemname': 'Sadow LAN Cable 25 m', 'quantity': 1, 
'vendor': 'SADOW TECHNOLOGIES', 'goods/HSN': '85177090', 'price': 480.0, 'country': 'IN', 'risk': 3}    
🔍 Processing: Sadow LAN Cable 25 m
Searching online...
'''

def organize(ls):
    obj=Inventory(ls)
    database=gather()
    obj.vendor_fn(database['vendors'])
    obj.hsn_fn(database['hsn_codes'])
    obj.quantity_fn(database['quantity_limits'])
    obj.country_fn(database['countries'])
    ls['risk']=obj.risk
    ls['risk_details']=obj.risk_details
    return ls




if __name__ =='__main__':
    ls={'itemname': 'Sadow LAN Cable 25 m', 'quantity': 1 ,'vendor': 'SADOW TECHNOLOGIES', 
    'goods/HSN': '85177090', 'price': 480.0, 'country': 'IN','unit':'units'}
    print(organize(ls))
    
    



    