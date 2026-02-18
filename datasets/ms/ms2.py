def merge_sort(arr):
    if len(arr) < 2:
        return arr

    half = len(arr) // 2
    left_part = merge_sort(arr[:half])
    right_part = merge_sort(arr[half:])

    sorted_list = []
    i = j = 0

    while i < len(left_part) and j < len(right_part):
        if left_part[i] <= right_part[j]:
            sorted_list.append(left_part[i])
            i += 1
        else:
            sorted_list.append(right_part[j])
            j += 1

    sorted_list += left_part[i:]
    sorted_list += right_part[j:]

    return sorted_list
