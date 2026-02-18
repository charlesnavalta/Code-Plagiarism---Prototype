def linear_search(arr, target):
    for i in range(len(arr)):
        if arr[i] == target:
            return True
    return False

numbers = [3, 7, 1, 9, 5]
print(linear_search(numbers, 9))
