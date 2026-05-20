# Defi 1

mot = input("Entrez un mot : ")

lettres_index = {}

for index, lettre in enumerate(mot):
    if lettre in lettres_index:
        lettres_index[lettre].append(index)
    else:
        lettres_index[lettre] = [index]

print(lettres_index)

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

