import random
from functools import reduce

from solution import solve


def try_get_param(params_dict, index):
    try:
        return params_dict[index]
    except KeyError:
        return None


def choice(possibilities, probabilities):
    assert len(possibilities) == len(probabilities)
    weighted = []
    for i in range(len(probabilities)):
        for _ in range(int(1000. * probabilities[i])):
            weighted.append(i)
    return possibilities[random.choice(weighted)]


def convert_index_to_value(index, value_counts):
    result = [0 for _ in range(len(value_counts))]
    carry = index
    for i in range(len(value_counts) - 1, -1, -1):
        result[i] = carry % value_counts[i]
        carry = carry // value_counts[i]
        if carry == 0:
            break
    return tuple(result)


def sample_from_bn(parent_lists, probability_dicts, value_counts):
    sample = []
    for parents, prob_dict, node in zip(parent_lists, probability_dicts, list(range(len(parent_lists)))):
        if len(parents) == 0:
            sample.append(choice(list(range(value_counts[node])), prob_dict))
        else:
            parent_values = tuple([sample[parent] for parent in parents])
            sample.append(choice(list(range(value_counts[node])), prob_dict[parent_values]))
    return sample


def generate_task(params):
    gen_node_count = try_get_param(params, "gen_node_count") or 10
    sensitivity_is_known = try_get_param(params, "sensitivity_is_known") or False
    possible_node_value_counts = try_get_param(params, "possible_node_value_counts") or (2, 3, 4)
    node_value_count_probabilities = try_get_param(params, "node_value_count_probabilities") or (0.7, 0.2, 0.1)
    possible_node_parent_counts = try_get_param(params, "possible_node_parent_counts") or (1, 2, 3, 4)
    node_parent_count_probabilities = try_get_param(params, "node_parent_count_probabilities") or (0.3, 0.3, 0.3, 0.1)
    unknown_gen_variables = try_get_param(params, "unknown_gen_variables") or 5
    evidence_index_upper_bound = try_get_param(params, "evidence_index_upper_bound") or gen_node_count - 3
    number_of_pred_evidences = try_get_param(params, "number_of_pred_evidences") or 1
    number_of_symptoms = try_get_param(params, "number_of_symptoms") or 3
    target_index = try_get_param(params, "target_index") or gen_node_count + 3

    if not (sensitivity_is_known or (unknown_gen_variables <= 10)):
        raise AttributeError("The sensitivity must be known if there are more than 10 unknown gen variables.")

    if gen_node_count < unknown_gen_variables:
        raise AttributeError("The number of unknown gen variables can't be greater "
                             "than the total number of gen variables.")

    number_of_gen_evidences = gen_node_count - unknown_gen_variables

    edges = [(0, 2), (1, 2)]
    for i in range(3, gen_node_count):
        parent_count = choice(possible_node_parent_counts, node_parent_count_probabilities)
        if parent_count > i:
            parent_count = i
        parents = sorted(random.sample(list(range(i)), parent_count))
        for parent in parents:
            edges.append((parent, i))

    parent_rows = [[] for i in range(gen_node_count)]
    for edge in edges:
        parent_rows[edge[1]].append(edge[0])
    value_counts = [choice(possible_node_value_counts, node_value_count_probabilities) for _ in range(len(parent_rows))]
    value_counts[-1] = 2
    probability_dicts = []
    for i in range(len(parent_rows)):
        if len(parent_rows[i]) == 0:
            combination_count = 1
        else:
            combination_count = reduce(lambda x, y: x*y, [value_counts[parent] for parent in parent_rows[i]])
        conditional_probabilities = []
        for _ in range(combination_count):
            probabilities = []
            for k in range(value_counts[i]):
                probabilities.append(random.random())
            prob_norm = sum(probabilities)
            probabilities = [round(prob / prob_norm, 5) for prob in probabilities]
            conditional_probabilities.append(probabilities)
        if len(parent_rows[i]) == 0:
            probability_dicts.append(conditional_probabilities[0])
        else:
            combinations = [convert_index_to_value(index, [value_counts[parent] for parent in parent_rows[i]]) for index in range(combination_count)]
            prob_dict = {}
            for combination, probabilities in zip(combinations, conditional_probabilities):
                prob_dict[combination] = probabilities
            probability_dicts.append(prob_dict)

    for _ in range(3):
        parent_rows.append([])
        value_counts.append(2)
    probability_dicts.append([0.9999, 0.0001])
    probability_dicts.append([0.7, 0.3])
    probability_dicts.append([0.7345, 0.2655])

    parent_rows.append([gen_node_count - 1, gen_node_count, gen_node_count + 1, gen_node_count + 2])
    value_counts.append(3)
    prob_dict = {
        (0, 0, 0, 0): [0.96, 0.03, 0.01],
        (1, 0, 0, 0): [0.41, 0.44, 0.15],
        (0, 0, 0, 1): [0.85, 0.13, 0.02],
        (1, 0, 0, 1): [0.27, 0.32, 0.41],
        (0, 0, 1, 0): [0.32, 0.56, 0.12],
        (1, 0, 1, 0): [0.07, 0.45, 0.48],
        (0, 0, 1, 1): [0.29, 0.61, 0.1],
        (1, 0, 1, 1): [0.12, 0.30, 0.58],
        (0, 1, 0, 0): [0.28, 0.38, 0.34],
        (1, 1, 0, 0): [0.14, 0.34, 0.52],
        (0, 1, 0, 1): [0.25, 0.33, 0.42],
        (1, 1, 0, 1): [0.07, 0.31, 0.62],
        (0, 1, 1, 0): [0.16, 0.43, 0.41],
        (1, 1, 1, 0): [0.07, 0.21, 0.72],
        (0, 1, 1, 1): [0.08, 0.16, 0.76],
        (1, 1, 1, 1): [0.01, 0.06, 0.93]
    }
    probability_dicts.append(prob_dict)

    for _ in range(5):
        parent_rows.append([gen_node_count + 3])
        value_counts.append(2)
    probability_dicts.append({
        (0,): [0.9, 0.1],
        (1,): [0.77, 0.23],
        (2,): [0.16, 0.84]
    })
    probability_dicts.append({
        (0,): [0.63, 0.37],
        (1,): [0.55, 0.45],
        (2,): [0.34, 0.66]
    })
    probability_dicts.append({
        (0,): [0.97, 0.03],
        (1,): [0.39, 0.61],
        (2,): [0.92, 0.08]
    })
    probability_dicts.append({
        (0,): [0.59, 0.41],
        (1,): [0.16, 0.84],
        (2,): [0.02, 0.98]
    })
    probability_dicts.append({
        (0,): [0.72, 0.28],
        (1,): [0.45, 0.55],
        (2,): [0.28, 0.72]
    })

    input_str = str(len(parent_rows)) + '\n'
    for i in range(len(parent_rows)):
        if len(parent_rows[i]) == 0:
            input_str = input_str + (str(value_counts[i]) + '\t' + str(len(parent_rows[i])) + '\t' +
                                     ','.join([str(element) for element in probability_dicts[i]])) + '\n'
        else:
            combination_count = reduce(lambda x, y: x * y, [value_counts[parent] for parent in parent_rows[i]])
            combinations = [convert_index_to_value(index, [value_counts[parent] for parent in parent_rows[i]]) for index in range(combination_count)]
            input_str = input_str + (str(value_counts[i]) + '\t' + str(len(parent_rows[i]))
                                     + '\t' + '\t'.join([str(element) for element in parent_rows[i]])
                                     + '\t' + '\t'.join([','.join([str(element) for element in combination]) +
                                                         ':' + ','.join([str(prob) for prob in probability_dicts[i][combination]])
                                                         for combination in combinations])) + '\n'

    sample = sample_from_bn(parent_rows, probability_dicts, value_counts)

    number_of_evidences = number_of_gen_evidences + number_of_pred_evidences + number_of_symptoms

    evidence_indices = sorted(random.sample(list(range(evidence_index_upper_bound)), number_of_gen_evidences))

    if sensitivity_is_known:
        evidence_indices.append(gen_node_count - 1)
        number_of_evidences += 1

    evidence_indices.extend(sorted(random.sample(list(range(gen_node_count, gen_node_count + 3)), number_of_pred_evidences)))
    evidence_indices.extend(sorted(random.sample(list(range(gen_node_count + 4, len(parent_rows))), number_of_symptoms)))
    evidences = [sample[index] for index in evidence_indices]

    input_str = input_str + (str(number_of_evidences)) + '\n'

    for index, evidence in zip(evidence_indices, evidences):
        input_str = input_str + (str(index) + '\t' + str(evidence)) + '\n'

    input_str = input_str + (str(target_index)) + '\n'

    target_output = solve(input_str)

    return input_str, target_output


if __name__ == "__main__":
    task = generate_task({})
    print task[0]
    print task[1]
