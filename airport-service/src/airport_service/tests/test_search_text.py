import unittest

from airport_service.domain.search_text import normalize_search_text


class SearchTextTestCase(unittest.TestCase):
    def test_normalizes_case_and_accents(self) -> None:
        self.assertEqual(normalize_search_text(" Bogotá "), "bogota")
        self.assertEqual(normalize_search_text("MEDELLIN"), "medellin")
        self.assertEqual(normalize_search_text("Medellín"), "medellin")
