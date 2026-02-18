def quick_sort(arr):
    if len(arr) <= 1:
        return arr

    pivot = arr[-1]
    left = []
    right = []

    for i in range(len(arr) - 1):
        if arr[i] <= pivot:
            left.append(arr[i])
        else:
            right.append(arr[i])

    return quick_sort(left) + [pivot] + quick_sort(right)


if __name__ == "__main__":
    data = [10, 7, 8, 9, 1, 5]
    print(quick_sort(data))
