import unittest
from solve import puzzleSolve as ps, potionParse as pp


class SolveTest(unittest.TestCase):

	def test_is_puzzle_solved(self):
		pot1 = pp.parse_potion("aaa")
		pot2 = pp.parse_potion("###")
		self.assertTrue(ps.is_puzzle_solved([pot1, pot2]))

	def test_is_not_puzzle_solved(self):
		pot1 = pp.parse_potion("aa#")
		pot2 = pp.parse_potion("aba")
		self.assertFalse(ps.is_puzzle_solved([pot1]))
		self.assertFalse(ps.is_puzzle_solved([pot2]))

	def test_sort_liquids_by_max_index(self):
		pot1 = pp.parse_potion("abc")
		pot2 = pp.parse_potion("abc")
		liquids = ps.sort_liquids_by_max_index([pot1, pot2])
		self.assertEqual(["c", "b", "a"], liquids)
