# Defi 1

mot = input("Entrez un mot : ")

word_index = {}

for index, word in enumerate(mot):
    if lettre in word_index:
        word_index[word].append(index)
    else:
     word_index[word] = [index]

print(word_index)

# Defi 2

items_purchase = {
    "Water": "$1",
    "Bread": "$3",
    "TV": "$1,000",
    "Fertilizer": "$20"
}

wallet = "$300"

money = int(wallet.replace("$", "").replace(",", ""))

basket = []

for item, price in items_purchase.items():
   
    price_clean = int(price.replace("$", "").replace(",", ""))

    if price_clean <= money:
        basket.append(item)
        money -= price_clean

if len(basket) == 0:
    print("Nothing")
else:
    print(sorted(basket))

