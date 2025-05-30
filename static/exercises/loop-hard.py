numbers = input("Please enter numbers and separated by commas: ")
numbers = numbers.split(',')

smallest = int(numbers[0])
second_smallest = int(numbers[1])
third_smallest = int(numbers[2])

for number in numbers[3::]:
    number = int(number)

    if number < smallest:
        third_smallest = second_smallest
        second_smallest = smallest
        smallest = number
    elif number < second_smallest:
        third_smallest = second_smallest
        second_smallest = number
    else:
        third_smallest = number

print("The third smallest number is %d" % third_smallest)

