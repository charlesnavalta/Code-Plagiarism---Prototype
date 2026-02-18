def quick_sort(arr):
    if len(arr) < 2:
        return arr

    pivot = arr[0]
    less = []
    greater = []

    for element in arr[1:]:
        if element < pivot:
            less.append(element)
        else:
            greater.append(element)

    return quick_sort(less) + [pivot] + quick_sort(greater)
