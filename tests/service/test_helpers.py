import os
import unittest

from src.service.helpers import read_yaml


class TestHelpers(unittest.TestCase):

    def test_read_yaml(self):
        config = read_yaml(f'{os.path.dirname(__file__)}/validation_config.yaml')
        self.assertEqual(5, len(config))


if __name__ == '__main__':
    unittest.main()
