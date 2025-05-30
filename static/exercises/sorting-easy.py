def bubble_sort(arr):
    n = len(arr)
    for i in range(n):
        for j in range(0, n - i - 1):
            if arr[j] < arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]

    return arr

array = input("Please enter numbers and separated by commas: ")
array = array.split(',')

print("Sorted list is:")
print(bubble_sort(array))
