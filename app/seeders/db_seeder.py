import random
from traceback import print_tb
from faker import Faker
from faker_food import FoodProvider

import sqlite3


def insert_data(table_name, data):
    conn = sqlite3.connect('pizza.sqlite')
    c = conn.cursor()
    c.execute("INSERT INTO {} VALUES ({})".format(table_name, data))
    conn.commit()
    conn.close()


def beverage(count):
    fake = Faker()
    fake.add_provider(FoodProvider)
    for i in range(count):
        price = random.randint(1, 10)
        insert_data('beverage', str(20+i)+",'" +fake.spice()+"'," + str(price))


def ingredients(count):
    fake = Faker()
    fake.add_provider(FoodProvider)
    for i in range(count):
        price = random.randint(1, 10)
        insert_data('ingredient', str(20+i)+",'" +fake.ingredient()+"'," + str(price))


def sizes(count):
    fake = Faker()
    fake.add_provider(FoodProvider)
    for i in range(count):
        price = random.randint(1, 30)
        insert_data('size',str(20+i)+",'"+ fake.ethnic_category()+"',"+ str(price))

beverage(10)
ingredients(10)
sizes(5)