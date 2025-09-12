'''
# risk_data.py

This module contains the `Inventory` class and the `organize` function for analyzing and organizing risk data.

## Imports

- `from mdb import extract_all_details as gather`: Imports the `extract_all_details` function from the `mdb` module.

## Classes

- `Inventory`: A class that represents an inventory item with associated risk data.

## Functions

- `organize(ls)`: A function that takes a dictionary `ls` representing an inventory item and returns the organized risk data.

## Inventory Class

The `Inventory` class represents an inventory item with associated risk data. It has the following attributes:

- `itemname`: The name of the item.
- `price`: The price of the item.
- `quantity`: The quantity of the item.
- `country`: The country of origin of the item.
- `vendor`: The vendor of the item.
- `hsn`: The Harmonized System (HS) code of the item.
- `unit`: The unit of measurement for the item.
- `risk`: The risk level associated with the item.
- `risk_details`: Additional details about the risk associated with the item.

The `Inventory` class has the following methods:

- `vendor_fn(vendors)`: A method that checks if the vendor is in the vendor watchlist and updates the risk and risk details accordingly.
- `country_fn(countries)`: A method that checks if the country is in the country watchlist and updates the risk and risk details accordingly.
- `hsn_fn(hsn)`: A method that checks if the HS code is in the HS code watchlist and updates the risk and risk details accordingly.
- `quantity_fn(pair)`: A method that checks if the quantity exceeds the limit for the item and updates the risk and risk details accordingly.

## organize function

The `organize` function takes a dictionary `ls` representing an inventory item and returns the organized risk data. It creates an instance of the `Inventory` class and calls its methods to check for potential risks. The risk and risk details are updated accordingly, and the dictionary `ls` is modified with the risk information.

## Usage

To use this module, you can import the `Inventory` class and the `organize` function from `risk_data.py`. Here's an example:

```python
from risk_data import Inventory, organize

ls = {'itemname': 'Sadow LAN Cable 25 m', 'quantity': 1, 'vendor': 'SADOW TECHNOLOGIES', 'goods/HSN': '85177090', 'price': 480.0, 'country': 'IN'}
inventory = Inventory(ls)
inventory.vendor_fn(database['vendors'])
inventory.country_fn(database['countries'])
inventory.hsn_fn(database['hsn_codes'])
inventory.quantity_fn(database['quantity_limits'])

ls['risk'] = inventory.risk

'''
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
    
    



    