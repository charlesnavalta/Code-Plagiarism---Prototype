def unique_quick_sort(sequence):
    # 1. Base case is structurally identical but variable names differ
    if len(sequence) < 2:
        return sequence
    
    # 2. Structural Change: Using the FIRST element as pivot (Original used last)
    # This changes the array slicing logic slightly
    pivot_value = sequence[0]
    
    # 3. Major AST Change: List Comprehensions
    # The original used a 'for' loop with 'append'. 
    # This uses 'ListComp' nodes, which look completely different to an AST parser.
    items_lower = [x for x in sequence[1:] if x <= pivot_value]
    items_higher = [x for x in sequence[1:] if x > pivot_value]
    
    # 4. Recursive return
    return unique_quick_sort(items_lower) + [pivot_value] + unique_quick_sort(items_higher)

if __name__ == "__main__":
    # Test Data
    test_data = [10, 7, 8, 9, 1, 5]
    print(unique_quick_sort(test_data))