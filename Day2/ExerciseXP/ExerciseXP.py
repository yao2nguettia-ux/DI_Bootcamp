# Exercise 1

keys = ['Ten', 'Twenty', 'Thirty']
values = [10, 20, 30]

result = dict(zip(keys, values))
print(result)

# Exercise 2

family = {"rick": 43, "beth": 13, "morty": 5, "summer": 8}

total_cost = 0

for name, age in family.items():
    if age < 3:
        price = 0
    elif 3 <= age <= 12:
        price = 10
    else:
        price = 15
    
    print(f"{name} doit payer {price}$")
    total_cost += price

print(f"Coût total de la famille : {total_cost}$")

# Exercise 3

brand = {
    "name": "Zara",
    "creation_date": 1975,
    "creator_name": "Amancio Ortega Gaona",
    "type_of_clothes": ["men", "women", "children", "home"],
    "international_competitors": ["Gap", "H&M", "Benetton"],
    "number_stores": 7000,
    "major_color": {
        "France": "blue",
        "Spain": "red",
        "US": ["pink", "green"]
    }
}

brand["number_stores"] = 2

print(f"Zara crée des vêtements pour {', '.join(brand['type_of_clothes'])}.")

brand["country_creation"] = "Spain"

if "international_competitors" in brand:
    brand["international_competitors"].append("Desigual")

brand.pop("creation_date")

print(brand["international_competitors"][-1])

print(brand["major_color"]["US"])

print(len(brand))

print(brand.keys())

more_on_zara = {
    "creation_date": 1975,
    "number_stores": 10000
}

brand.update(more_on_zara)
print(brand)

# Exercise 4

def describe_city(city, country="Unknown"):
    print(f"{city} is in {country}.")

describe_city("Reykjavik", "Iceland")
describe_city("Paris")

# Exercise 5

import random

def compare_number(user_number):
    random_number = random.randint(1, 100)
    
    if user_number == random_number:
        print("Success!")
    else:
        print(f"Fail! Your number: {user_number}, Random number: {random_number}")

compare_number(50)

# Exercise 6

def make_shirt(size="large", text="I love Python"):
    print(f"The size of the shirt is {size} and the text is '{text}'.")

make_shirt()
make_shirt(size="medium")
make_shirt("small", "Custom message")
make_shirt(size="small", text="Hello!")

# Exercise 7

import random

def get_random_temp():
    return random.randint(-10, 40)

def main():
    temp = get_random_temp()
    print(f"The temperature right now is {temp} degrees Celsius.")
    
    if temp < 0:
        print("Brrr, it's freezing! Wear extra layers.")
    elif 0 <= temp <= 16:
        print("It's quite cold! Don't forget your coat.")
    elif 17 <= temp <= 23:
        print("Nice weather.")
    elif 24 <= temp <= 32:
        print("It's warm, stay hydrated.")
    else:
        print("It's really hot! Stay cool.")

main()

# Exercise 8

toppings = []
price = 10

while True:
    topping = input("Enter a topping (or 'quit' to finish): ")
    
    if topping == 'quit':
        break
    
    toppings.append(topping)
    price += 2.5
    print(f"Adding {topping} to your pizza.")

print("\nYour pizza toppings:")
for t in toppings:
    print(f"- {t}")

print(f"Total price: ${price}")