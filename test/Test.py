import unittest
import potionParse as pp


class PotionTest(unittest.TestCase):

	def test_parse_potion(self):
		potion = pp.parse_potion("ab#")
		self.assertEqual(2, potion.get_level())
		self.assertEqual("a", potion.get_liquid(0))
		self.assertEqual("b", potion.get_liquid(1))

	def test_overflow_potion(self):
		potion = pp.parse_potion("abc")
		self.assertRaises(ValueError, potion.push_liquid, "d")

	def test_mix_two_single_liquid_potions(self):
		p1 = pp.parse_potion("a#")
		p2 = pp.parse_potion("a#")
		pour = p1.pour_into(p2)
		self.assertTrue(p1.is_empty())
		self.assertTrue(p2.is_full())
		self.assertTrue(1, pour.liquid_count)

	def test_pour_multiple_liquids(self):
		p1 = pp.parse_potion("aa#")
		p2 = pp.parse_potion("a##")
		pour = p1.pour_into(p2)
		self.assertTrue(p1.is_empty())
		self.assertTrue(p2.is_full())
		self.assertTrue(2, pour.liquid_count)

	def test_mix_unequal_liquids(self):
		p1 = pp.parse_potion("a#")
		p2 = pp.parse_potion("b#")
		self.assertFalse(p1.can_push_liquid(p2))
		p1.pour_into(p2)
		self.assertEqual(1, p1.get_level())
		self.assertEqual(1, p2.get_level())


