def get_index_combinations(multiplicity):
    index_combinations = []

    # Calculates each unique combination of indexes.
    for n2 in range(1, multiplicity):
        for n1 in range(0, n2):
            combination = (n1, n2)
            index_combinations.append(combination)

    return index_combinations