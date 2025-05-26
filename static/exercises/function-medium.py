def count_occurrence(message, letter):
    count = 0

    for char in message:
        if char == letter:
            count += 1

    return count

message = input('Enter your message: ')

most_used_letter = 'a'
highest_count = 0

for letter in range(ord('a'), ord('z')):
    count = count_occurrence(message, chr(letter))
    if count > highest_count:
        highest_count = count
        most_used_letter = chr(letter)

print("The letter that appears most often in %s is %s" % (message, most_used_letter))