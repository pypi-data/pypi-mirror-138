"""This module implements the electre 1 algorithm.

Implementation and naming conventions are taken from
:cite:p:`vincke1998electre1`.
"""

from typing import List, cast

from ..core.aliases import NumericPerformanceTable, NumericValue


def delta_calculation(
    performance_table: NumericPerformanceTable,
) -> NumericValue:
    """Compute delta for discordancce.

    :param performance_table:
    :return: the value of the discordance's delta"""

    list_diff_features = []
    for feature_index in range(len(performance_table[0])):
        maximum = cast(NumericValue, 0)
        minimum = performance_table[0][feature_index]
        for index_action in range(len(performance_table)):
            if performance_table[index_action][feature_index] > maximum:
                maximum = performance_table[index_action][feature_index]
            elif performance_table[index_action][feature_index] < minimum:
                minimum = performance_table[index_action][feature_index]
        list_diff_features.append(maximum - minimum)
    return max(list_diff_features)


def pairwise_concordance(
    list1: List[NumericValue],
    list2: List[NumericValue],
    criteria_weights: List[NumericValue],
) -> NumericValue:
    """Compute the concordance comparison of 2 actions.

    :param list1:
    :param list2:
    :param criteria_weights:
    :return: concordance index"""
    sum_weight = sum(criteria_weights)
    concordance_value = 0.0
    for k in range(len(list1)):
        concordance_value = (
            concordance_value + criteria_weights[k]
            if list1[k] >= list2[k]
            else concordance_value
        )
    concordance_value = concordance_value / sum_weight
    assert concordance_value >= 0
    return concordance_value


def concordance(
    performance_table: NumericPerformanceTable,
    criteria_weights: List[NumericValue],
) -> List[List[NumericValue]]:
    """Compute the discordance comparison of 2 actions.

    :param performance_table:
    :param criteria_weights:
    :return: concordance matrix"""
    nb_columns = len(performance_table)
    nb_lines = len(performance_table)
    return [
        [
            pairwise_concordance(
                performance_table[i], performance_table[j], criteria_weights
            )
            for j in range(nb_columns)
        ]
        for i in range(nb_lines)
    ]


def pairwise_discordance(
    list1: List[NumericValue], list2: List[NumericValue], delta: NumericValue
) -> NumericValue:
    """Compute the discordance comparison of 2 actions.

    :param list1:
    :param list2:
    :param delta: discordance delta
    :return: discordance index"""
    return (
        max([element2 - element1 for element1, element2 in zip(list1, list2)])
        / delta
    )


def discordance(
    performance_table: NumericPerformanceTable,
) -> List[List[NumericValue]]:
    """Compute the discordance matrix.

    :param performance_table: Numeric Performance Table
    :return: the disocrdance matrix"""
    delta = delta_calculation(performance_table)
    nb_columns = len(performance_table)
    nb_lines = len(performance_table)
    return [
        [
            pairwise_discordance(
                performance_table[i], performance_table[j], delta
            )
            for j in range(nb_columns)
        ]
        for i in range(nb_lines)
    ]


def outranking(
    concordance: List[List[NumericValue]],
    discordance: List[List[NumericValue]],
    c_hat: NumericValue,
    d_hat: NumericValue,
) -> List[List[NumericValue]]:
    """Compute the outranking matrix.

    :param discordance: discordance matrix
    :param concordance: concordance matrix
    :param c_hat: concordance threshold
    :param d_hat: discordance threshold
    :return: the outranking matrix of the performance table"""
    nb_columns = len(concordance[0])
    nb_lines = len(concordance)
    return [
        [
            0.0
            if i == j
            else (
                1.0
                if (concordance[i][j] >= c_hat and discordance[i][j] <= d_hat)
                else 0.0
            )
            for j in range(nb_columns)
        ]
        for i in range(nb_lines)
    ]


def electre1(
    performance_table: NumericPerformanceTable,
    criteria_weights: List[NumericValue],
    c_hat: NumericValue,
    d_hat: NumericValue,
) -> List[List[NumericValue]]:
    """Compute the outranking matrix using electre1 method.

    :param performance_table:
    :param criteria_weights:
    :param c_hat: concordance threshold
    :param d_hat: discordance threshold
    :return: the outranking matrix of the performance table"""
    concordance_matrix = concordance(performance_table, criteria_weights)
    discordance_matrix = discordance(performance_table)
    return outranking(concordance_matrix, discordance_matrix, c_hat, d_hat)


# check dominance matrix
# check electre i and s
