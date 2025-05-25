def quick_sort(arr):
    if len(arr) <= 1:
        return arr

    pivot = arr[0]
    left = [x for x in arr[1:] if x < pivot]
    right = [x for x in arr[1:] if x > pivot]

    return quick_sort(left) + [pivot] + quick_sort(right)

array = input("Please enter numbers and seperated by commas: ")
array = array.split(',')

print("Sorted list is:")
print(quick_sort(array))