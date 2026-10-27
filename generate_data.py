"""
Electric Vehicle Market Performance & Insights
Data Generator & SQLite Database Initialization Script
Generates a comprehensive, realistic dataset of Global EV Market Performance.
"""

import sqlite3
import random
import os

DB_PATH = os.path.join(os.path.dirname(__file__), 'database.db')

# Curated reference models for high authenticity
REFERENCE_MODELS = [
    # SUVs
    {"manufacturer": "Tesla", "model": "Model Y", "category": "SUV", "battery_tech": "LFP", "capacity": 60.0, "range_km": 455, "price": 43990, "charging_speed": 170, "country": "USA", "rating": 4.7, "sales": 1220000},
    {"manufacturer": "Tesla", "model": "Model Y Long Range", "category": "SUV", "battery_tech": "NMC", "capacity": 78.1, "range_km": 533, "price": 48990, "charging_speed": 250, "country": "USA", "rating": 4.8, "sales": 890000},
    {"manufacturer": "Tesla", "model": "Model X Plaid", "category": "SUV", "battery_tech": "NCA", "capacity": 100.0, "range_km": 543, "price": 94990, "charging_speed": 250, "country": "USA", "rating": 4.6, "sales": 48000},
    {"manufacturer": "BYD", "model": "Atto 3 (Yuan Plus)", "category": "SUV", "battery_tech": "LFP", "capacity": 60.5, "range_km": 420, "price": 34500, "charging_speed": 88, "country": "China", "rating": 4.5, "sales": 420000},
    {"manufacturer": "BYD", "model": "Tang EV", "category": "SUV", "battery_tech": "LFP", "capacity": 108.8, "range_km": 600, "price": 54000, "charging_speed": 140, "country": "China", "rating": 4.4, "sales": 135000},
    {"manufacturer": "BYD", "model": "Song Plus EV", "category": "SUV", "battery_tech": "LFP", "capacity": 71.8, "range_km": 505, "price": 31000, "charging_speed": 90, "country": "China", "rating": 4.6, "sales": 395000},
    {"manufacturer": "Volkswagen", "model": "ID.4 Pro", "category": "SUV", "battery_tech": "NMC", "capacity": 77.0, "range_km": 525, "price": 46500, "charging_speed": 135, "country": "Germany", "rating": 4.3, "sales": 192000},
    {"manufacturer": "Volkswagen", "model": "ID.5 GTX", "category": "SUV", "battery_tech": "NMC", "capacity": 77.0, "range_km": 490, "price": 56000, "charging_speed": 135, "country": "Germany", "rating": 4.2, "sales": 64000},
    {"manufacturer": "Hyundai", "model": "Ioniq 5 AWD", "category": "SUV", "battery_tech": "NMC", "capacity": 77.4, "range_km": 481, "price": 49500, "charging_speed": 350, "country": "South Korea", "rating": 4.8, "sales": 178000},
    {"manufacturer": "Hyundai", "model": "Kona Electric", "category": "SUV", "battery_tech": "NMC", "capacity": 65.4, "range_km": 490, "price": 36500, "charging_speed": 100, "country": "South Korea", "rating": 4.4, "sales": 84000},
    {"manufacturer": "Kia", "model": "EV6 Long Range", "category": "SUV", "battery_tech": "NMC", "capacity": 77.4, "range_km": 528, "price": 51000, "charging_speed": 350, "country": "South Korea", "rating": 4.8, "sales": 142000},
    {"manufacturer": "Kia", "model": "EV9 AWD", "category": "SUV", "battery_tech": "NMC", "capacity": 99.8, "range_km": 505, "price": 63900, "charging_speed": 350, "country": "South Korea", "rating": 4.7, "sales": 58000},
    {"manufacturer": "BMW", "model": "iX xDrive50", "category": "SUV", "battery_tech": "NMC", "capacity": 105.2, "range_km": 630, "price": 87500, "charging_speed": 195, "country": "Germany", "rating": 4.7, "sales": 72000},
    {"manufacturer": "BMW", "model": "iX3", "category": "SUV", "battery_tech": "NMC", "capacity": 74.0, "range_km": 460, "price": 64000, "charging_speed": 150, "country": "Germany", "rating": 4.3, "sales": 61000},
    {"manufacturer": "Rivian", "model": "R1S Adventure", "category": "SUV", "battery_tech": "NCA", "capacity": 135.0, "range_km": 560, "price": 78000, "charging_speed": 220, "country": "USA", "rating": 4.7, "sales": 32000},
    {"manufacturer": "Rivian", "model": "R1T Quad-Motor", "category": "SUV", "battery_tech": "NCA", "capacity": 135.0, "range_km": 528, "price": 87000, "charging_speed": 220, "country": "USA", "rating": 4.8, "sales": 28000},
    {"manufacturer": "Audi", "model": "Q8 e-tron", "category": "SUV", "battery_tech": "NMC", "capacity": 106.0, "range_km": 582, "price": 74400, "charging_speed": 170, "country": "Germany", "rating": 4.5, "sales": 49000},
    {"manufacturer": "Audi", "model": "Q4 e-tron", "category": "SUV", "battery_tech": "NMC", "capacity": 77.0, "range_km": 510, "price": 49800, "charging_speed": 135, "country": "Germany", "rating": 4.3, "sales": 78000},
    {"manufacturer": "Volvo", "model": "EX30 Extended", "category": "SUV", "battery_tech": "NMC", "capacity": 64.0, "range_km": 476, "price": 38900, "charging_speed": 153, "country": "Sweden", "rating": 4.6, "sales": 95000},
    {"manufacturer": "Volvo", "model": "EX90 Twin Motor", "category": "SUV", "battery_tech": "NMC", "capacity": 107.0, "range_km": 600, "price": 81000, "charging_speed": 250, "country": "Sweden", "rating": 4.7, "sales": 26000},
    {"manufacturer": "NIO", "model": "ES6", "category": "SUV", "battery_tech": "NMC", "capacity": 75.0, "range_km": 490, "price": 52000, "charging_speed": 180, "country": "China", "rating": 4.6, "sales": 84000},
    {"manufacturer": "NIO", "model": "ES8 Solid-State Pilot", "category": "SUV", "battery_tech": "Solid-State", "capacity": 150.0, "range_km": 930, "price": 89000, "charging_speed": 280, "country": "China", "rating": 4.9, "sales": 15000},
    {"manufacturer": "XPeng", "model": "G9 AWD", "category": "SUV", "battery_tech": "NMC", "capacity": 98.0, "range_km": 570, "price": 56000, "charging_speed": 300, "country": "China", "rating": 4.6, "sales": 45000},
    {"manufacturer": "XPeng", "model": "G6 Ultra", "category": "SUV", "battery_tech": "LFP", "capacity": 66.0, "range_km": 580, "price": 33500, "charging_speed": 280, "country": "China", "rating": 4.7, "sales": 88000},
    {"manufacturer": "Mercedes-Benz", "model": "EQE SUV 350+", "category": "SUV", "battery_tech": "NMC", "capacity": 90.6, "range_km": 590, "price": 77900, "charging_speed": 170, "country": "Germany", "rating": 4.6, "sales": 51000},
    {"manufacturer": "Mercedes-Benz", "model": "EQS SUV 450 4MATIC", "category": "SUV", "battery_tech": "NMC", "capacity": 108.4, "range_km": 610, "price": 104400, "charging_speed": 200, "country": "Germany", "rating": 4.7, "sales": 33000},
    {"manufacturer": "Toyota", "model": "bZ4X AWD", "category": "SUV", "battery_tech": "NMC", "capacity": 71.4, "range_km": 460, "price": 44000, "charging_speed": 100, "country": "Japan", "rating": 3.9, "sales": 52000},
    {"manufacturer": "Toyota", "model": "Solid-State Crown EV", "category": "SUV", "battery_tech": "Solid-State", "capacity": 120.0, "range_km": 850, "price": 78000, "charging_speed": 350, "country": "Japan", "rating": 4.8, "sales": 12000},
    {"manufacturer": "VinFast", "model": "VF 8 Eco", "category": "SUV", "battery_tech": "LFP", "capacity": 87.7, "range_km": 471, "price": 46000, "charging_speed": 150, "country": "Vietnam", "rating": 3.7, "sales": 34000},
    {"manufacturer": "Tata Motors", "model": "Nexon EV Long Range", "category": "SUV", "battery_tech": "LFP", "capacity": 40.5, "range_km": 465, "price": 21500, "charging_speed": 50, "country": "India", "rating": 4.4, "sales": 68000},
    {"manufacturer": "Tata Motors", "model": "Harrier.ev AWD", "category": "SUV", "battery_tech": "LFP", "capacity": 60.0, "range_km": 500, "price": 28000, "charging_speed": 60, "country": "India", "rating": 4.5, "sales": 32000},
    {"manufacturer": "Mahindra", "model": "XUV400 Pro", "category": "SUV", "battery_tech": "LFP", "capacity": 39.4, "range_km": 456, "price": 20000, "charging_speed": 50, "country": "India", "rating": 4.2, "sales": 27000},

    # Sedans
    {"manufacturer": "Tesla", "model": "Model 3 Standard", "category": "Sedan", "battery_tech": "LFP", "capacity": 60.0, "range_km": 513, "price": 38990, "charging_speed": 170, "country": "USA", "rating": 4.7, "sales": 640000},
    {"manufacturer": "Tesla", "model": "Model 3 Long Range", "category": "Sedan", "battery_tech": "NMC", "capacity": 75.0, "range_km": 629, "price": 47740, "charging_speed": 250, "country": "USA", "rating": 4.9, "sales": 480000},
    {"manufacturer": "Tesla", "model": "Model S Plaid", "category": "Sedan", "battery_tech": "NCA", "capacity": 100.0, "range_km": 600, "price": 89990, "charging_speed": 250, "country": "USA", "rating": 4.8, "sales": 39000},
    {"manufacturer": "BYD", "model": "Seal Design RWD", "category": "Sedan", "battery_tech": "LFP", "capacity": 82.5, "range_km": 570, "price": 43500, "charging_speed": 150, "country": "China", "rating": 4.7, "sales": 165000},
    {"manufacturer": "BYD", "model": "Han EV Flagship", "category": "Sedan", "battery_tech": "LFP", "capacity": 85.4, "range_km": 610, "price": 49000, "charging_speed": 120, "country": "China", "rating": 4.6, "sales": 195000},
    {"manufacturer": "BMW", "model": "i4 eDrive40", "category": "Sedan", "battery_tech": "NMC", "capacity": 80.7, "range_km": 590, "price": 57300, "charging_speed": 205, "country": "Germany", "rating": 4.7, "sales": 96000},
    {"manufacturer": "BMW", "model": "i7 xDrive60", "category": "Sedan", "battery_tech": "NMC", "capacity": 101.7, "range_km": 625, "price": 105700, "charging_speed": 195, "country": "Germany", "rating": 4.8, "sales": 29000},
    {"manufacturer": "Hyundai", "model": "Ioniq 6 Long Range", "category": "Sedan", "battery_tech": "NMC", "capacity": 77.4, "range_km": 614, "price": 45500, "charging_speed": 350, "country": "South Korea", "rating": 4.7, "sales": 87000},
    {"manufacturer": "Lucid", "model": "Air Pure RWD", "category": "Sedan", "battery_tech": "NMC", "capacity": 88.0, "range_km": 660, "price": 69900, "charging_speed": 250, "country": "USA", "rating": 4.8, "sales": 16000},
    {"manufacturer": "Lucid", "model": "Air Grand Touring", "category": "Sedan", "battery_tech": "NCA", "capacity": 118.0, "range_km": 830, "price": 110900, "charging_speed": 300, "country": "USA", "rating": 4.9, "sales": 11000},
    {"manufacturer": "Mercedes-Benz", "model": "EQE 350+", "category": "Sedan", "battery_tech": "NMC", "capacity": 89.0, "range_km": 639, "price": 74900, "charging_speed": 170, "country": "Germany", "rating": 4.5, "sales": 48000},
    {"manufacturer": "Mercedes-Benz", "model": "EQS 450+", "category": "Sedan", "battery_tech": "NMC", "capacity": 108.4, "range_km": 720, "price": 104400, "charging_speed": 200, "country": "Germany", "rating": 4.6, "sales": 31000},
    {"manufacturer": "Porsche", "model": "Taycan Performance Plus", "category": "Sedan", "battery_tech": "NMC", "capacity": 93.4, "range_km": 505, "price": 92500, "charging_speed": 270, "country": "Germany", "rating": 4.8, "sales": 41000},
    {"manufacturer": "NIO", "model": "ET7 Executive Edition", "category": "Sedan", "battery_tech": "Solid-State", "capacity": 150.0, "range_km": 1050, "price": 96000, "charging_speed": 280, "country": "China", "rating": 4.9, "sales": 19000},
    {"manufacturer": "NIO", "model": "ET5 Touring", "category": "Sedan", "battery_tech": "LFP", "capacity": 75.0, "range_km": 530, "price": 44000, "charging_speed": 180, "country": "China", "rating": 4.7, "sales": 67000},
    {"manufacturer": "Polestar", "model": "Polestar 2 Long Range", "category": "Sedan", "battery_tech": "NMC", "capacity": 82.0, "range_km": 655, "price": 51300, "charging_speed": 205, "country": "Sweden", "rating": 4.6, "sales": 54000},
    {"manufacturer": "Volkswagen", "model": "ID.7 Pro S", "category": "Sedan", "battery_tech": "NMC", "capacity": 86.0, "range_km": 700, "price": 57000, "charging_speed": 200, "country": "Germany", "rating": 4.6, "sales": 43000},
    {"manufacturer": "XPeng", "model": "P7i Max", "category": "Sedan", "battery_tech": "NMC", "capacity": 86.2, "range_km": 702, "price": 39000, "charging_speed": 175, "country": "China", "rating": 4.5, "sales": 72000},
    {"manufacturer": "QuantumScape Pilot", "model": "QS SolidDrive 1", "category": "Sedan", "battery_tech": "Solid-State", "capacity": 110.0, "range_km": 910, "price": 82000, "charging_speed": 350, "country": "USA", "rating": 4.9, "sales": 8500},

    # Hatchbacks
    {"manufacturer": "BYD", "model": "Dolphin Surf", "category": "Hatchback", "battery_tech": "LFP", "capacity": 44.9, "range_km": 340, "price": 28900, "charging_speed": 60, "country": "China", "rating": 4.6, "sales": 360000},
    {"manufacturer": "BYD", "model": "Seagull (Dolphin Mini)", "category": "Hatchback", "battery_tech": "LFP", "capacity": 38.8, "range_km": 305, "price": 13500, "charging_speed": 40, "country": "China", "rating": 4.5, "sales": 410000},
    {"manufacturer": "Volkswagen", "model": "ID.3 Pro", "category": "Hatchback", "battery_tech": "NMC", "capacity": 58.0, "range_km": 426, "price": 39900, "charging_speed": 120, "country": "Germany", "rating": 4.3, "sales": 140000},
    {"manufacturer": "MG", "model": "MG4 EV Long Range", "category": "Hatchback", "battery_tech": "NMC", "capacity": 64.0, "range_km": 450, "price": 32000, "charging_speed": 135, "country": "China", "rating": 4.6, "sales": 155000},
    {"manufacturer": "MG", "model": "MG4 EV Standard", "category": "Hatchback", "battery_tech": "LFP", "capacity": 51.0, "range_km": 350, "price": 26900, "charging_speed": 88, "country": "China", "rating": 4.4, "sales": 115000},
    {"manufacturer": "Renault", "model": "Megane E-Tech EV60", "category": "Hatchback", "battery_tech": "NMC", "capacity": 60.0, "range_km": 450, "price": 41000, "charging_speed": 130, "country": "France", "rating": 4.5, "sales": 69000},
    {"manufacturer": "Renault", "model": "5 E-Tech", "category": "Hatchback", "battery_tech": "NMC", "capacity": 52.0, "range_km": 400, "price": 27500, "charging_speed": 100, "country": "France", "rating": 4.7, "sales": 78000},
    {"manufacturer": "Peugeot", "model": "e-208 GT", "category": "Hatchback", "battery_tech": "NMC", "capacity": 51.0, "range_km": 400, "price": 34800, "charging_speed": 100, "country": "France", "rating": 4.4, "sales": 63000},
    {"manufacturer": "Nissan", "model": "Leaf SV Plus", "category": "Hatchback", "battery_tech": "NMC", "capacity": 60.0, "range_km": 342, "price": 36000, "charging_speed": 100, "country": "Japan", "rating": 4.1, "sales": 51000},
    {"manufacturer": "Fiat", "model": "500e Icon", "category": "Hatchback", "battery_tech": "NMC", "capacity": 42.0, "range_km": 320, "price": 32500, "charging_speed": 85, "country": "France", "rating": 4.3, "sales": 64000},
    {"manufacturer": "Tata Motors", "model": "Tiago EV Long Range", "category": "Hatchback", "battery_tech": "LFP", "capacity": 24.0, "range_km": 315, "price": 12800, "charging_speed": 25, "country": "India", "rating": 4.4, "sales": 58000},
    {"manufacturer": "Citroën", "model": "ë-C3 You", "category": "Hatchback", "battery_tech": "LFP", "capacity": 44.0, "range_km": 320, "price": 23300, "charging_speed": 100, "country": "France", "rating": 4.2, "sales": 49000},
    {"manufacturer": "SolidEnergy Labs", "model": "Nano Solid Hatch", "category": "Hatchback", "battery_tech": "Solid-State", "capacity": 65.0, "range_km": 610, "price": 42000, "charging_speed": 220, "country": "Japan", "rating": 4.7, "sales": 6500},

    # Two-Wheelers
    {"manufacturer": "Ola Electric", "model": "S1 Pro Gen 2", "category": "Two-Wheeler", "battery_tech": "NMC", "capacity": 4.0, "range_km": 195, "price": 1650, "charging_speed": 3.3, "country": "India", "rating": 4.5, "sales": 310000},
    {"manufacturer": "Ola Electric", "model": "S1 Air", "category": "Two-Wheeler", "battery_tech": "LFP", "capacity": 3.0, "range_km": 151, "price": 1250, "charging_speed": 2.5, "country": "India", "rating": 4.3, "sales": 210000},
    {"manufacturer": "Ola Electric", "model": "Diamondhead Superbike", "category": "Two-Wheeler", "battery_tech": "Solid-State", "capacity": 12.0, "range_km": 320, "price": 6500, "charging_speed": 15.0, "country": "India", "rating": 4.8, "sales": 18000},
    {"manufacturer": "Ather Energy", "model": "450X Gen 3", "category": "Two-Wheeler", "battery_tech": "NMC", "capacity": 3.7, "range_km": 150, "price": 1800, "charging_speed": 3.3, "country": "India", "rating": 4.8, "sales": 140000},
    {"manufacturer": "Ather Energy", "model": "450 Apex", "category": "Two-Wheeler", "battery_tech": "NMC", "capacity": 3.7, "range_km": 157, "price": 2300, "charging_speed": 3.3, "country": "India", "rating": 4.9, "sales": 45000},
    {"manufacturer": "TVS", "model": "iQube ST", "category": "Two-Wheeler", "battery_tech": "NMC", "capacity": 5.1, "range_km": 145, "price": 1700, "charging_speed": 2.5, "country": "India", "rating": 4.4, "sales": 185000},
    {"manufacturer": "Zero Motorcycles", "model": "DSR/X Adventure", "category": "Two-Wheeler", "battery_tech": "NMC", "capacity": 17.3, "range_km": 290, "price": 22995, "charging_speed": 12.0, "country": "USA", "rating": 4.7, "sales": 14000},
    {"manufacturer": "Zero Motorcycles", "model": "SR/S Sport", "category": "Two-Wheeler", "battery_tech": "NMC", "capacity": 17.3, "range_km": 301, "price": 20995, "charging_speed": 12.0, "country": "USA", "rating": 4.6, "sales": 16500},
    {"manufacturer": "LiveWire", "model": "S2 Del Mar", "category": "Two-Wheeler", "battery_tech": "NMC", "capacity": 10.5, "range_km": 182, "price": 15499, "charging_speed": 7.2, "country": "USA", "rating": 4.4, "sales": 12000},
    {"manufacturer": "NIU Technologies", "model": "MQi GT EVO", "category": "Two-Wheeler", "battery_tech": "LFP", "capacity": 3.7, "range_km": 100, "price": 3800, "charging_speed": 2.2, "country": "China", "rating": 4.3, "sales": 195000},
    {"manufacturer": "NIU Technologies", "model": "RQi Sport Electric", "category": "Two-Wheeler", "battery_tech": "NMC", "capacity": 5.2, "range_km": 115, "price": 6900, "charging_speed": 3.5, "country": "China", "rating": 4.5, "sales": 42000},
    {"manufacturer": "Yadea", "model": "Keeness VFD", "category": "Two-Wheeler", "battery_tech": "LFP", "capacity": 4.6, "range_km": 140, "price": 3500, "charging_speed": 2.5, "country": "China", "rating": 4.2, "sales": 260000},
    {"manufacturer": "Gogoro", "model": "SuperSport ACE", "category": "Two-Wheeler", "battery_tech": "NMC", "capacity": 3.4, "range_km": 120, "price": 2700, "charging_speed": 3.0, "country": "Vietnam", "rating": 4.6, "sales": 175000},
    {"manufacturer": "BMW", "model": "CE 04 Urban Cruiser", "category": "Two-Wheeler", "battery_tech": "NMC", "capacity": 8.9, "range_km": 130, "price": 12195, "charging_speed": 6.9, "country": "Germany", "rating": 4.6, "sales": 21000},
    {"manufacturer": "Energica", "model": "Eva Ribelle RS", "category": "Two-Wheeler", "battery_tech": "NCA", "capacity": 21.5, "range_km": 420, "price": 28800, "charging_speed": 24.0, "country": "Germany", "rating": 4.7, "sales": 7200},
    {"manufacturer": "Gogoro", "model": "Solid-State E-Scooter Concept", "category": "Two-Wheeler", "battery_tech": "Solid-State", "capacity": 5.0, "range_km": 240, "price": 3800, "charging_speed": 6.0, "country": "Vietnam", "rating": 4.8, "sales": 8000}
]

def generate_ev_dataset():
    """Generates an extensive dataset of 120+ EV records with realistic variations."""
    records = []
    
    # Add all curated reference models
    for m in REFERENCE_MODELS:
        records.append({
            "manufacturer": m["manufacturer"],
            "model": m["model"],
            "vehicle_category": m["category"],
            "battery_tech": m["battery_tech"],
            "battery_capacity": round(float(m["capacity"]), 1),
            "driving_range": int(m["range_km"]),
            "price": int(m["price"]),
            "charging_speed": round(float(m["charging_speed"]), 1),
            "manufacturing_country": m["country"],
            "customer_rating": round(float(m["rating"]), 1),
            "annual_sales": int(m["sales"])
        })
    
    # Generate variations to ensure statistical richness and diverse segment coverage
    manufacturers_by_country = {
        "USA": ["Tesla", "Rivian", "Lucid", "Cadillac", "Ford", "Chevrolet"],
        "China": ["BYD", "NIO", "XPeng", "Geely", "Zeekr", "GAC Aion", "Li Auto"],
        "Germany": ["Volkswagen", "BMW", "Mercedes-Benz", "Audi", "Porsche"],
        "South Korea": ["Hyundai", "Kia", "Genesis"],
        "Japan": ["Toyota", "Nissan", "Honda", "Lexus"],
        "India": ["Tata Motors", "Mahindra", "Ola Electric", "Ather Energy", "TVS"],
        "Sweden": ["Volvo", "Polestar"],
        "France": ["Renault", "Peugeot", "Citroën"],
        "Vietnam": ["VinFast", "Gogoro"]
    }

    categories = ["SUV", "Sedan", "Hatchback", "Two-Wheeler"]
    battery_types = ["LFP", "NMC", "NCA", "Solid-State"]

    random.seed(42) # Reproducible high quality generation

    # Generate additional 75 realistic variants
    for i in range(1, 76):
        country = random.choice(list(manufacturers_by_country.keys()))
        mfr = random.choice(manufacturers_by_country[country])
        
        # Two-wheelers mostly for India, China, Vietnam, USA
        if country in ["India", "Vietnam"] and random.random() < 0.4:
            category = "Two-Wheeler"
        elif country in ["USA", "Germany", "Sweden"]:
            category = random.choices(["SUV", "Sedan", "Hatchback", "Two-Wheeler"], weights=[0.48, 0.35, 0.12, 0.05])[0]
        else:
            category = random.choice(categories)

        # Battery Tech distribution realistic weights
        if category == "Two-Wheeler":
            battery_tech = random.choices(["LFP", "NMC", "Solid-State"], weights=[0.45, 0.50, 0.05])[0]
            capacity = round(random.uniform(2.5, 16.0), 1)
            # Range: ~30-40 km per kWh for 2-wheeler
            range_km = int(capacity * random.uniform(25, 42) + random.randint(10, 30))
            price = int(random.uniform(1200, 18000))
            charging_speed = round(random.uniform(1.8, 14.0), 1)
            sales = random.randint(15000, 280000)
            model_name = f"{mfr} E-Glide {chr(65 + (i % 26))}{i}"
        elif category == "Hatchback":
            battery_tech = random.choices(["LFP", "NMC", "Solid-State"], weights=[0.55, 0.40, 0.05])[0]
            capacity = round(random.uniform(30.0, 68.0), 1)
            range_km = int(capacity * random.uniform(6.5, 8.8) + random.randint(20, 50))
            price = int(random.uniform(14000, 42000))
            charging_speed = round(random.uniform(40.0, 150.0), 1)
            sales = random.randint(25000, 310000)
            model_name = f"{mfr} Urban {chr(65 + (i % 26))}-{i*10}"
        elif category == "Sedan":
            battery_tech = random.choices(["LFP", "NMC", "NCA", "Solid-State"], weights=[0.30, 0.45, 0.18, 0.07])[0]
            capacity = round(random.uniform(55.0, 115.0), 1)
            # Higher efficiency for sedans
            range_km = int(capacity * random.uniform(6.8, 9.2) + random.randint(30, 60))
            price = int(random.uniform(34000, 105000))
            charging_speed = round(random.uniform(120.0, 320.0), 1)
            sales = random.randint(18000, 350000)
            model_name = f"{mfr} Aero {i*100}"
        else: # SUV
            battery_tech = random.choices(["LFP", "NMC", "NCA", "Solid-State"], weights=[0.35, 0.45, 0.15, 0.05])[0]
            capacity = round(random.uniform(58.0, 130.0), 1)
            range_km = int(capacity * random.uniform(5.5, 7.8) + random.randint(20, 50))
            price = int(random.uniform(38000, 118000))
            charging_speed = round(random.uniform(100.0, 350.0), 1)
            sales = random.randint(22000, 520000)
            model_name = f"{mfr} Horizon X{i}"

        # Solid-State tech premiums
        if battery_tech == "Solid-State":
            range_km = int(range_km * 1.35)
            price = int(price * 1.25)
            charging_speed = round(min(charging_speed * 1.4, 360.0), 1)
            sales = int(sales * 0.25) # Early production / pilot units

        # Customer rating correlates somewhat with range, charging speed and value
        base_rating = 4.1 + (0.5 if range_km > 500 else 0.0) + (0.3 if charging_speed > 150 else 0.0) - (0.4 if price > 85000 and range_km < 550 else 0.0)
        rating = round(min(5.0, max(3.2, base_rating + random.uniform(-0.35, 0.4))), 1)

        records.append({
            "manufacturer": mfr,
            "model": model_name,
            "vehicle_category": category,
            "battery_tech": battery_tech,
            "battery_capacity": capacity,
            "driving_range": range_km,
            "price": price,
            "charging_speed": charging_speed,
            "manufacturing_country": country,
            "customer_rating": rating,
            "annual_sales": sales
        })

    return records

def init_database():
    """Initializes SQLite database and seeds with EV market dataset."""
    db_file = DB_PATH
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    cursor.execute("DROP TABLE IF EXISTS ev_market;")

    cursor.execute("""
    CREATE TABLE ev_market (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        manufacturer TEXT NOT NULL,
        model TEXT NOT NULL,
        vehicle_category TEXT NOT NULL,
        battery_tech TEXT NOT NULL,
        battery_capacity REAL NOT NULL,
        driving_range INTEGER NOT NULL,
        price INTEGER NOT NULL,
        charging_speed REAL NOT NULL,
        manufacturing_country TEXT NOT NULL,
        customer_rating REAL NOT NULL,
        annual_sales INTEGER NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)

    # Create strategic indices for dashboard query speed
    cursor.execute("CREATE INDEX idx_mfr ON ev_market(manufacturer);")
    cursor.execute("CREATE INDEX idx_category ON ev_market(vehicle_category);")
    cursor.execute("CREATE INDEX idx_battery ON ev_market(battery_tech);")
    cursor.execute("CREATE INDEX idx_country ON ev_market(manufacturing_country);")
    cursor.execute("CREATE INDEX idx_price ON ev_market(price);")

    dataset = generate_ev_dataset()

    for item in dataset:
        cursor.execute("""
        INSERT INTO ev_market (
            manufacturer, model, vehicle_category, battery_tech,
            battery_capacity, driving_range, price, charging_speed,
            manufacturing_country, customer_rating, annual_sales
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            item["manufacturer"],
            item["model"],
            item["vehicle_category"],
            item["battery_tech"],
            item["battery_capacity"],
            item["driving_range"],
            item["price"],
            item["charging_speed"],
            item["manufacturing_country"],
            item["customer_rating"],
            item["annual_sales"]
        ))

    conn.commit()
    count = cursor.execute("SELECT COUNT(*) FROM ev_market;").fetchone()[0]
    conn.close()
    print(f"Database successfully initialized at: {db_file}")
    print(f"Total EV records inserted: {count}")

if __name__ == "__main__":
    init_database()
