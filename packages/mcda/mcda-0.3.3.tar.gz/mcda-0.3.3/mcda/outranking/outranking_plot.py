"""This module implements the plot method for outranking algorithms

"""


from typing import List

import graphviz

from ..core.aliases import NumericValue


def plot_outranking(
    outranking_matrix: List[List[NumericValue]],
    alternatives: List[str] = None,
    edge_label: bool = False,
):
    """Create a graph for outranking matrix.

    This function creates a Graph using graphviz and display it.

    :param outranking_matrix: the matrix to display
    :param alternatives: (optional) the name for the actions
    :param edge_label: (optional) parameter to display the value of edges.
    """

    outranking_graph = graphviz.Digraph("outranking")
    if alternatives is None:
        alternatives = [
            "a" + str(i + 1) for i in range(len(outranking_matrix[0]))
        ]
    outranking_graph.attr("node", shape="box")
    for a in alternatives:
        outranking_graph.node(a)
    for i in range(len(outranking_matrix)):
        for j in range(len(outranking_matrix[i])):
            label = ""
            if edge_label:
                label = str(outranking_matrix[i][j])
            if outranking_matrix[i][j] == 1:
                outranking_graph.edge(
                    alternatives[i], alternatives[j], label=label
                )
    outranking_graph.render()
    return outranking_graph
