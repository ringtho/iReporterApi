import unittest
from api.routes import app
import json

class TestRedFlags(unittest.TestCase):
    def setUp(self):
        """initialise test client"""
        self.test_client = app.test_client()
      


if __name__ == '__main__':
    unittest.main()