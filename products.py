products = []

while True:
    try:
        num_products = int(input("How many products do you want to enter? "))
        if num_products > 0:
            break
        else:
            print("Please enter a positive number.")
    except ValueError:
        print("Please enter a valid number.")

print("\nEnter details for each product:")
for i in range(1, num_products + 1):
    print(f"\nProduct {i}:")
    
    name = input("  Product name: ").strip()
    
    while True:
        try:
            stock = int(input("  Stock quantity: "))
            break
        except ValueError:
            print("  Please enter a valid number for stock.")
    
    products.append({"name": name, "stock": stock})

def show_low_stock(threshold=10):
    print(f"\nProducts with stock less than {threshold}:")    
    low_stock_found = False
    
    for product in products:
        if product["stock"] < threshold:
            print(f"  {product['name']:20} | Stock: {product['stock']:3}")
            low_stock_found = True
    
    if not low_stock_found:
        print("  No products have stock below", threshold)

print(f"  Total products entered: {len(products)}")



for p in products:
    print(f"  {p['name']:20} : {p['stock']}")

show_low_stock(10)

while True:
    again = input("\nCheck with a different threshold? (y/n): ").strip().lower()
    if again == 'y':
        try:
            new_threshold = int(input("Enter new threshold: "))
            show_low_stock(new_threshold)
        except ValueError:
            print("Invalid number - using 10 instead")
            show_low_stock(10)
    else:
        break