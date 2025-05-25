customer_ages = input("Please enter customer ages and seperated by commas: ")
customer_ages = customer_ages.split(",")
total_price = 0

for customer_age in customer_ages:
    customer_age = int(customer_age)

    if customer_age < 4:
        print("Small children are not allowed in this cinema!")
        exit(1)
    elif customer_age <= 11:
        total_price += 8.50
    elif customer_age <= 64:
        total_price += 11.00
    elif customer_age >= 65:
        total_price += 9.50

if len(customer_ages) >= 4:
    print("Discount: 10% (family discount)")
    total_price *= 0.9

print("Amount to be paid: %.2f euro" % total_price)