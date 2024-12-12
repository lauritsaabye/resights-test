import networkx as nx
from typing import Any, Dict, List

from lib.utilities import convert_to_bounds


def bootstrap_graph(data: List[Dict[str, Any]]):
    """
        Bootstraps a `DiGraph` from a list of dictionaries.

        This function takes a list of dictionaries, where each dictionary contains both node and edge data, and converts it to a `DiGaph`
        Edges are added to the graph with a `share_range`. Nodes are implicitly added when adding an edge (if the node doesn't already exist).

        Args:
            data (List[Dict[str, Any]]): A list of dictionaries, where each dictionary contains:
                - 'source_name' (str): The identifier of the source node (source company) in the graph.
                - 'target_name' (str): The identifier of the target node (target company) in the graph.
                - 'share' (str): The share value, which will be converted into a tuple by the `convert_to_bounds` function.

        Returns:
            nx.DiGraph: A `DiGraph` with nodes and edges added based on the input data.
                Each edge has a `share_range` attribute.

        Note:
            A human-readable id is used for the nodes, `source_name`. Perhaps we want to use a unique id?
    """

    graph = nx.DiGraph()

    for entry in data:
        graph.add_edge(
            entry['source_name'],
            entry['target_name'],
            share_range=convert_to_bounds(entry['share'])
        )
    return graph


def fetch_target_share(source: str, target: str, data: nx.DiGraph):
    """
        Calculates the real lower, real average, and real upper share values as a percentage for the path between a
        source company and a target company.

        Args:
            source (str): id of starting node (source company) in the graph. Not necessarily unique, as `source_name` is used as the identifier.
            target (str): id of target node (target company) in the graph. Not necessarily unique, as `source_name` is used as the identifier.
            data (nx.DiGraph): graph data to search through

        Returns:
            dict:
                - 'real_lower_share' (float): The accumulated lower bound of share percentage.
                - 'real_average_share' (float): The average of the accumulated lower and upper bound share percentage.
                - 'real_upper_share' (float): The accumulated upper bound of share percentage.
    """
    # The assumption here is that there can only exist 1 path from source to target. Other cases are not handled here
    shortest_path = nx.shortest_path(data, source=source, target=target)

    lower_bound_acc = upper_bound_acc = 1
    for node, next_node in zip(shortest_path, shortest_path[1:]):
        edge_data = data.get_edge_data(node, next_node)

        lower_bound, upper_bound = edge_data['share_range']
        lower_bound_acc *= lower_bound
        upper_bound_acc *= upper_bound
    return {
        'real_lower_share': lower_bound_acc,
        'real_average_share': (upper_bound_acc + lower_bound_acc) / 2,
        'real_upper_share': upper_bound_acc
    }
