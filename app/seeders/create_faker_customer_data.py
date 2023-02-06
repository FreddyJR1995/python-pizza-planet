from faker import Faker
import csv

fake = Faker()

rows = []

for _ in range(15):
    name = fake.name()
    dni = fake.ssn()
    address = fake.address()
    phone = fake.phone_number()
    row = [name, dni, address, phone]
    rows.append(row)

filename = 'app/seeders/customers.csv'

with open(filename, 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerows(rows)