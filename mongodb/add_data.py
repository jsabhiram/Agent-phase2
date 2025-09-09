from pymongo import MongoClient
import os

uri="mongodb+srv://jsabhiramsuresh:AtUKr9R9r9ozELf4@cluster1.kky8xoc.mongodb.net/" # Ensure your environment variable is set
print(uri)
def insert_sample_data():

    client = MongoClient(uri)
    db = client["sample_mflix"]
    print(db)

    db["watchlist_vendors"].insert_many([
        # { "name": "Globex Corporation" },
        # { "name": "Umbrella Ltd" },
        # { "name": "Vehement Holdings" }
                { "name": "Techtronics Ltd" },
                { "name": "MediCare Supplies" },
                { "name": "Steel & Co" },
                { "name": "AgroMart" },
                { "name": "GreenFuel Pvt Ltd" },
                { "name": "FiberTech India" },
                { "name": "PharmaTrust" },
                { "name": "AquaPure Systems" },
                { "name": "NeoMachinery" },
                { "name": "EcoPlastics" },
                { "name": "AutoSpare Corp" },
                { "name": "NanoElectronics" },
                { "name": "Global Cement Ltd" },
                { "name": "FreshPack Foods" },
                { "name": "SmartHome Devices" },
                { "name": "TruWood Exports" },
                { "name": "Skyline Textiles" },
                { "name": "BioCrop Seeds" },
                { "name": "UrbanLights Pvt Ltd" },
                { "name": "Metallix Inc" }

    ])

    db["watchlist_countries"].insert_many([
        { "name": "Narnia" },
        { "name": "Wakanda" },
        { "name": "Elbonia" }
    ])

    db["watchlist_hsn"].insert_many([
        { "code": 8483 },
        { "code": 9021 },
        { "code": 7308 }
    ])

    db["benchmark_prices"].insert_many([
        { "item": "High-Precision Gear", "price": 800 },
        { "item": "Thermal Sensor Unit", "price": 1500 },
        { "item": "Industrial Lubricant", "price": 300 },
        { "item": "Steel Beams", "price": 700 }
    ])

    db["quantity_limits"].insert_many([
        { "item": "High-Precision Gear", "unit": "units", "max_quantity": 100 },
        { "item": "Thermal Sensor Unit", "unit": "units", "max_quantity": 50 },
        { "item": "Industrial Lubricant", "unit": "kg", "max_quantity": 500 },
        { "item": "Steel Beams", "unit": "ton", "max_quantity": 25 }
    ])

    print("Sample data inserted successfully.")

insert_sample_data()
