inputs = input("Please enter weights and seperated by commas: ")
weights = inputs
total_costs = 0

for weight in weights.split(','):
    weight = int(weight)

    if weight <= 4:
        total_costs += 4.25
    elif weight <= 10:
        total_costs += 12.50
    else:
        total_costs += 28.00

print("Total costs: %.2f euro" % total_costs)

if len(weights) >= 5:
    print("Because you are sending 5 or more packages together, you get a 5% discount!")
    print("Amount to be paid: %.2f euro" % (total_costs * 0.95))