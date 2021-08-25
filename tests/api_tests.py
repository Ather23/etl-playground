import unittest
import request


TMGjL4r9yytuHjSVaXcjNY4KF
class ApiTests(unittest.TestCase):
    def test_fetch_data_from_scorata(self):
        result = request.get()
        self.assertEqual(True, False)


if __name__ == '__main__':
    unittest.main()
