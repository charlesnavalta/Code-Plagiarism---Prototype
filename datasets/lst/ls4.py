def linear_search(arr, target):
    index = 0
    found = False
    while index < len(arr) and not found:
        if arr[index] == target:
            found = True
        index += 1
    return found

nums = [3, 7, 1, 9, 5]
print(linear_search(nums, 9))
