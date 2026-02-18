def sort_list(values):
    if len(values) <= 1:
        return values

    middle = len(values) // 2
    first_half = sort_list(values[:middle])
    second_half = sort_list(values[middle:])

    return combine(first_half, second_half)


def combine(a, b):
    merged = []
    x = y = 0

    while x < len(a) and y < len(b):
        if a[x] < b[y]:
            merged.append(a[x])
            x += 1
        else:
            merged.append(b[y])
            y += 1

    merged.extend(a[x:])
    merged.extend(b[y:])
    return merged
