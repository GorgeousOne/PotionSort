from potion import Potion


class PourAction:

	def __init__(self, p_from: Potion, p_to: Potion):
		self.pFrom = p_from
		self.pTo = p_to
		self._poured_liquids = []

	def add_poured_liquid(self, liquid: chr):
		self._poured_liquids.append(liquid)

	def is_empty(self) -> bool:
		return not bool(self._poured_liquids)