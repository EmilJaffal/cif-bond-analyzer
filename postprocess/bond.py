from preprocess.cif_parser import get_atom_type
from itertools import permutations


def process_and_order_pairs(all_points, atomic_pair_list):
    processed_pairs = []
    
    for i in range(len(all_points)):
        pair_point = i + 1

        shortest_pair = None
        shortest_distance = float('inf')

        for pair in atomic_pair_list:
            if pair_point in pair["point_pair"] and pair["distance"] < shortest_distance:
                shortest_distance = pair["distance"]
                shortest_pair = pair

        if shortest_pair is not None:
            processed_pairs.append(shortest_pair)
    
    # Ordering the processed pairs based on atom types
    processed_pairs_ordered = []
    for pair in processed_pairs:
        atom_type_0 = get_atom_type(pair['labels'][0])
        atom_type_1 = get_atom_type(pair['labels'][1])

        if atom_type_0 > atom_type_1:
            pair['labels'] = pair['labels'][::-1]
            pair['point_pair'] = pair['point_pair'][::-1]
            pair['coordinates'] = pair['coordinates'][::-1]

        processed_pairs_ordered.append(pair)
    
    return processed_pairs_ordered


def strip_labels_and_remove_duplicate(unique_pairs_distances):
    '''
    unique_pairs_distances_test_2 = {
        ('Ga1A', 'Ga1'): ['2.601'],
        ('Ga1', 'La1'): ['3.291'],
        ('Co1B', 'Ga1'): ['2.601'],
        ('Ga1', 'Ga1A'): ['2.601'],
        ('Ga1', 'Ga1'): ['2.358']}
                                     
    to 
    
    adjusted_pairs_test_2 == {
        ('Ga', 'Ga'): ['2.358'],
        ('Ga', 'La'): ['3.291'],
        ('Co', 'Ga'): ['2.601']}
        
    '''
    adjusted_pairs = {}
    for pair, distances in unique_pairs_distances.items():
        simplified_pair = tuple(sorted(get_atom_type(atom) for atom in pair))
        current_distance = float(distances[0])  # Convert distance to float for comparison

        # If the pair already exists, compare distances and keep the smallest
        if simplified_pair in adjusted_pairs:
            existing_distance = float(adjusted_pairs[simplified_pair][0])
            if current_distance < existing_distance:
                adjusted_pairs[simplified_pair] = [distances[0]]
        else:
            adjusted_pairs[simplified_pair] = distances

    return adjusted_pairs


def get_missing_pairs(adjusted_unique_pairs_distances):
    # Extract all unique elements from the pairs
    unique_elements = list(set([element for pair in adjusted_unique_pairs_distances.keys() for element in pair]))

    # Generate all possible pairs (with ordering matter)
    all_possible_pairs = list(permutations(unique_elements, 2))

    # Make sure each pair is sorted
    all_possible_pairs = [tuple(sorted(pair)) for pair in all_possible_pairs]

    # Remove duplicates after sorting
    all_possible_pairs = list(set(all_possible_pairs))

    # Sort the pairs in the data as well before comparison
    sorted_pairs_data = [tuple(sorted(pair)) for pair in adjusted_unique_pairs_distances.keys()]

    # Find the pairs that are not in the data
    missing_pairs = [pair for pair in all_possible_pairs if pair not in sorted_pairs_data]

    return missing_pairs