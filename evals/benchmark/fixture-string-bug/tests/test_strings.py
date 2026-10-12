import unittest

from string_ops import normalize_email


class StringTests(unittest.TestCase):
    def test_strips_spaces_and_normalizes_case(self):
        self.assertEqual(normalize_email("  USER@Example.COM  "), "user@example.com")


if __name__ == "__main__":
    unittest.main()
