import random
import csv
import requests
from datetime import datetime, timedelta
from faker import Faker
from faker_food import FoodProvider

URL = 'http://127.0.0.1:5000/order/'

with open('app/seeders/customers.csv', "r", encoding="utf-8-sig") as file:
    reader = csv.reader(file)
    customers = list(reader)

fake = Faker()
fake.add_provider(FoodProvider)

def seed_order(count):
    for _ in range(count):
        customer = customers[random.randint(0, len(customers) - 1)]
        order_date = fake.date_time_between(start_date='-1y', end_date='now', tzinfo=None)
        order = {
            "client_name": customer[0],
            "client_dni": customer[1],
            "client_address": customer[2],
            "client_phone": customer[3],
            "date": order_date.strftime("%Y-%m-%d %H:%M:%S"),
            "size_id": str(random.randint(20, 24)),
            "ingredients": [
                str(random.randint(20, 35)),
                str(random.randint(20, 35)),
                str(random.randint(20, 35))
            ],
            "beverages": [
                str(random.randint(20, 35)),
                str(random.randint(20, 35)),
            ]
        }
        response = requests.post(URL, json=order)
        print(response.text)

seed_order(100)
