from collections import defaultdict


def dict_with_sequences(post_dict):
    sequence = []
    alt_sequence = defaultdict(list)
    for key, item in post_dict.items():
        if item and key.startswith('sequence'):
            sequence.append(item)
        if item and key.startswith('alt_sequence'):
            step = key.split('alt_sequence')[1].split('.')[0]
            alt_sequence[step].append(item)
    final_dict = post_dict.copy()
    final_dict['sequence'] = sequence
    final_dict['alt_sequence'] = alt_sequence
    return final_dict
