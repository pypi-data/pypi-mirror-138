import unittest
import os
from oemof.solph import Bus

from vppopt.nodes_utils import nodes_data_excel_parser, nodes_from_dict, get_node_from_list


class TestNodesFromDict(unittest.TestCase):
    excel_path = os.path.join(
        os.path.dirname(__file__),
        "data",
        "vppopt_basic_example.xlsx"
    )

    # parse data from excel file into a dictionary
    nodes = nodes_data_excel_parser(
        excel_path,
        engine = 'openpyxl'
    )

    es_nodes = nodes_from_dict(nd=nodes)

    def test_es_nodes_type(self):

        self.assertIsInstance(
            self.es_nodes,
            list
        )
    def test_es_nodes_content(self):
        """
        nodes containes
        - Bus
        - Sink
        - Transformer
        - GenericStorage
        """

        node_label_list = [
            "bel",
            "bel_excess",
            "bgas",
            "rgas",
            "wind",
            "pv",
            "demand_el",
            "pp_gas",
            "generic_storage"
        ]

        self.assertTrue(
            all(
                label in [node.label for node in self.es_nodes] for label in node_label_list
            )
        )
        self.assertTrue("bel" in [node.label for node in self.es_nodes if isinstance(node,Bus)])

    def test_get_node_from_list(self):

        bel = get_node_from_list(self.es_nodes,Bus,'bel')
        self.assertIsInstance(bel,Bus)
        self.assertEqual(bel.label,"bel")

if __name__=='__main__':
    unittest.main()
