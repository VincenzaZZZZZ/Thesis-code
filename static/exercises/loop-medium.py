numbers = input("Please enter numbers and seperated by commas: ")
numbers = numbers.split(',')

smallest = 0
for num in numbers[1::]:
    if num < smallest:
        smallest = num
print("The smallest number is %d" % smallest)