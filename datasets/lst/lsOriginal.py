def linear_search(arr, target):
    for i in arr:
        if i == target:
            return True
    return False

nums = [3, 7, 1, 9, 5]
print(linear_search(nums, 9))
