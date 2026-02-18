def linear_search(lst, key):
    for item in lst:
        if item == key:
            return True
    return False

numbers = [3, 7, 1, 9, 5]
print(linear_search(numbers, 9))
