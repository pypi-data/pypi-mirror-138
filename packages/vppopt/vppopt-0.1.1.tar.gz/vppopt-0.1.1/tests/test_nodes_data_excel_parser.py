import unittest
import os

from vppopt.nodes_utils import nodes_data_excel_parser

class TestNodesExcelParser(unittest.TestCase):

    excel_path = os.path.join(
        os.path.dirname(__file__),
        "data",
        "vppopt_basic_example.xlsx"
    )

    nodes = nodes_data_excel_parser(
        excel_path,
        engine = 'openpyxl'
    )

    def test_nodes_data_type(self):
        """
        Test
        """
        self.assertIsInstance(self.nodes,dict)

    def test_nodes_excel_keys(self):
        """
        assert keys for nodes parsed from excel input file
        """
        keys = [
            "buses",
            "commodity_sources",
            "demand",
            "powerlines",
            "renewables",
            "storages",
            "transformers",
            "transformers_chp",
            "timeseries",
            "financial"
        ]
        self.assertSetEqual(
            set(keys),
            set(self.nodes.keys())
        )

if __name__=='__main__':
    unittest.main()
