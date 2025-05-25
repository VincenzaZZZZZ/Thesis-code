def round_to_nearest_half(f):
    return int(2 * f + 0.5) / 2

def calculate_average_grade(grades):
    grade_sum = 0.0
    for grade in grades:
        grade_sum += float(grade)
    return grade_sum / len(grades)

def determine_final_grade(grades):
    grade = calculate_average_grade(grades)
    grade = round_to_nearest_half(grade)
    if 5.5 <= grade < 6.0:
        return "6-"
    else:
        return str(grade)

grades = input("Please enter grades and seperated by commas: ").split(',')
print("The student has a final grade of %s" % (determine_final_grade(grades)))