def sort_numbers(values):
    if len(values) <= 1:
        return values

    p = values[-1]
    smaller = []
    larger = []

    for index in range(len(values) - 1):
        if values[index] <= p:
            smaller.append(values[index])
        else:
            larger.append(values[index])

    return sort_numbers(smaller) + [p] + sort_numbers(larger)
