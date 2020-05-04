from unittest import TestCase

from scrapers import bla

class FirstTest(TestCase):

    def test_hello(self):
        result = bla.hello("world")
        self.assertEqual("Hello world", result)

if __name__ == '__main__':
    unittest.main()