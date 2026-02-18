def quick_sort(arr):
    if len(arr) <= 1:
        return arr

    pivot = arr[-1]
    left, right = partition(arr[:-1], pivot)

    return quick_sort(left) + [pivot] + quick_sort(right)


def partition(arr, pivot):
    smaller = []
    larger = []

    for value in arr:
        if value <= pivot:
            smaller.append(value)
        else:
            larger.append(value)

    return smaller, larger
