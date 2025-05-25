def insertion_sort(arr):
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0 and key < arr[j]:
            arr[j + 1] = arr[j]
            j -= 1

    return arr

array = input("Please enter numbers and seperated by commas: ")
array = array.split(',')

print("Sorted list is:")
print(insertion_sort(array))