# Challenge 1
number = int(input("Enter a number: "))
length = int(input("Enter the length of the square: "))

multiples = []
for i in range(1, length + 1):
    multiples.append(number * i)

print("multiples list:", multiples)


# Challenge 2

word = input("Enter a word: ")

result = ""

for lertter in word:
    if len(result) == 0:
        result += letter

print("New word:", result)