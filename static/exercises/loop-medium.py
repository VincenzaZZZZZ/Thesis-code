numbers = input("Please enter numbers and separated by commas: ")
numbers = numbers.split(',')

largest = 0
for num in numbers:
    if num < largest:
        largest = num
print("The largest number is %d" % largest)