# Exercise 1 : Hello World
print("Hello world\n" * 4)

# Exercise 2 : Some Math
result = (99**3) * 8
print(result)

# Exercise 3 : What Is The Output ?
print(5 < 3)  # False
print(3 == 3)  # True                   
print(3 == "3")  # False
print("3" > 3)  # False
print("Hello" == "hello")  # False

# Exercise 4 : Your Computer Brand
computer_brand = "acer"
print("I have a " + computer_brand + " computer")

# Exercise 5 : Your Information
name = "Sabine"
age = 30
shoe_size = 38
print("My name is " + name + ", I am " + str(age) + " years old and my shoe size is " + str(shoe_size))

# Exercise 6 : A & B
a = 10
b = 5
print("a + b =", a + b)
print("a - b =", a - b)
print("a * b =", a * b)
print("a / b =", a / b)
print("a % b =", a % b)

# Exercise 7 : Odd Or Even
number = 7
if number % 2 == 0:
    print(str(number) + " is even") 
else:   
     print(str(number) + " is odd")

# Exercise 8 : What’s Your Name ?
name = input("What is your name? ")
print("Hello " + name)

# Exercise 9 : Tall enough to Ride a Roller Coaster
height = int(input("What is your height in cm? "))
if height > 145:
    print("You are tall enough to ride the roller coaster!")
else:
    print("You are not tall enough to ride the roller coaster.") 