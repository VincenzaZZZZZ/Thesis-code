def is_prime(n):
    for i in range(2, n):
        if n % i == 0:
            return False
    return True

def quick_sort(arr):
    if len(arr) <= 1:
        return arr

    pivot = arr[0]
    left = [x for x in arr[1:] if x < pivot]
    right = [x for x in arr[1:] if x > pivot]

    return quick_sort(left) + [pivot] + quick_sort(right)

def count_occurrence(message, letter):
    count = 0

    for char in message:
        if char == letter:
            count += 1

    return count


def check_answer(filename, user_inputs, correct_inputs):
    input_correct = False

    submitted_inputs = [x.strip() for x in user_inputs.split(',')]
    submitted_ints = []
    for x in submitted_inputs:
        try:
            submitted_ints.append(int(x))
        except ValueError:
            continue

    if filename == 'if-statement-easy':
        valid_input_count = 0
        for expected in correct_inputs:
            start, end = map(int, expected.split("-"))
            for num in submitted_ints:
                if start <= num <= end:
                    valid_input_count += 1

        if valid_input_count == len(submitted_inputs):
            input_correct = True
        else:
            input_correct = False

    elif filename == 'if-statement-medium' or filename == 'if-statement-hard':
        valid_input_count = 0
        for expected in correct_inputs:
            expected_val = int(expected)
            if expected_val in submitted_ints:
                valid_input_count += 1

        if valid_input_count == len(submitted_inputs):
            input_correct = True
        else:
            input_correct = False

    elif filename == 'loop-easy' or filename == 'function-easy' or filename == 'sorting-easy' or filename == 'sorting-medium':
        if submitted_inputs == correct_inputs:
            input_correct = True

    elif filename == 'loop-medium':
        for num in submitted_ints:
            if num < 0:
                input_correct = True

    elif filename == 'loop-hard':
        third = int(submitted_ints[2])
        for num in submitted_ints[3::]:
            if num > third:
                input_correct = True

    elif filename == 'function-medium':
        highest_count = 0
        most_used_letter = ''

        for letter in range(ord('a'), ord('z') + 1):
            count = count_occurrence(submitted_inputs[0], chr(letter))
            if count > highest_count:
                highest_count = count
                most_used_letter = chr(letter)

        if most_used_letter == 'z':
            input_correct = True

    elif filename == 'function-hard':
        valid_input_count = 0
        for num in submitted_ints:
            if is_prime(num):
                valid_input_count += 1

        if valid_input_count == len(submitted_ints):
            input_correct = True

    elif filename == 'sorting-hard':
        output_array = quick_sort(submitted_ints)
        if len(submitted_ints) != len(output_array):
            input_correct = True

    elif filename == 'real-world-example-easy':
        if submitted_ints[0] != submitted_ints[1]:
            input_correct = True

    elif filename == 'real-world-example-medium':
        grade_sum = 0.0
        for num in submitted_inputs:
            grade_sum += float(num)
        avg_grade = grade_sum / len(submitted_inputs)
        if 5.25<= avg_grade < 5.5:
            input_correct = True

    elif filename == 'real-world-example-hard':
        if len(user_inputs) >= 5 > len(submitted_inputs):
            input_correct = True

    return input_correct