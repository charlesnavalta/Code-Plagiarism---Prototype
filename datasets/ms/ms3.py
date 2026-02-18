def merge_sort(arr):
    if len(arr) <= 1:
        return arr

    mid_index = len(arr) // 2
    left = arr[:mid_index]
    right = arr[mid_index:]

    left_sorted = merge_sort(left)
    right_sorted = merge_sort(right)

    return merge_lists(left_sorted, right_sorted)


def merge_lists(list1, list2):
    result = []
    p1 = p2 = 0

    while p1 < len(list1):
        if p2 >= len(list2) or list1[p1] < list2[p2]:
            result.append(list1[p1])
            p1 += 1
        else:
            result.append(list2[p2])
            p2 += 1

    while p2 < len(list2):
        result.append(list2[p2])
        p2 += 1

    return result
