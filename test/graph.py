import unittest
from networkx import NodeNotFound, NetworkXNoPath, shortest_path
from lib.graph import bootstrap_graph, fetch_target_share

data = [
    {'source_name': 'A', 'target_name': 'B', 'share': '50%'},
    {'source_name': 'B', 'target_name': 'C', 'share': '50-100%'},
    {'source_name': 'C', 'target_name': 'D', 'share': '<50%'},
    {'source_name': 'C', 'target_name': 'E', 'share': '100%'}
]


class TestGraphFunctions(unittest.TestCase):
    def test_bootstrap_graph(self):
        graph = bootstrap_graph(data)

        # (A, B, C, D, E)
        self.assertEqual(len(graph.nodes), 5)

        # (A -> B, B -> C, C -> D, C -> E)
        self.assertEqual(len(graph.edges), 4)

        # Check edge data (share_range)
        edge_data_ab = graph.get_edge_data('A', 'B')
        edge_data_bc = graph.get_edge_data('B', 'C')
        edge_data_cd = graph.get_edge_data('C', 'D')
        edge_data_ce = graph.get_edge_data('C', 'E')

        self.assertEqual(edge_data_ab['share_range'], (0.5, 0.5))
        self.assertEqual(edge_data_bc['share_range'], (0.5, 1))
        self.assertEqual(edge_data_cd['share_range'], (0, 0.5))
        self.assertEqual(edge_data_ce['share_range'], (1, 1))

    def test_fetch_target_share_ac(self):
        graph = bootstrap_graph(data)

        result = fetch_target_share('A', 'C', graph)

        self.assertAlmostEqual(result['real_lower_share'], 0.5 * 0.5)
        self.assertAlmostEqual(result['real_average_share'], (0.5 * 0.5 + 0.5 * 1) / 2)
        self.assertAlmostEqual(result['real_upper_share'], 0.5 * 1)

        self.assertEqual(shortest_path(graph, source='A', target='C'), ['A', 'B', 'C'])

    def test_fetch_target_share_ae(self):
        graph = bootstrap_graph(data)

        result = fetch_target_share('A', 'E', graph)

        self.assertAlmostEqual(result['real_lower_share'], 0.5 * 0.5 * 1)
        self.assertAlmostEqual(result['real_average_share'], (0.5 * 0.5 * 1 + 0.5 * 1 * 1) / 2)
        self.assertAlmostEqual(result['real_upper_share'], 0.5 * 1 * 1)

        self.assertEqual(shortest_path(graph, source='A', target='E'), ['A', 'B', 'C', 'E'])

    def test_no_path_in_graph(self):
        graph = bootstrap_graph(data)

        with self.assertRaises(NetworkXNoPath):
            fetch_target_share('D', 'E', graph)

    def test_no_source_node_in_graph(self):
        graph = bootstrap_graph(data)

        with self.assertRaises(NodeNotFound):
            fetch_target_share('NON_EXISTENT', 'E', graph)

    def test_no_target_node_in_graph(self):
        graph = bootstrap_graph(data)

        with self.assertRaises(NodeNotFound):
            fetch_target_share('D', 'NON_EXISTENT', graph)
