from typing import List


class Potion:

	def __init__(self, index: int, capacity: int, contents: List[chr]):
		self.index = index
		self._capacity = capacity
		self._liquids = contents

	def get_capacity(self) -> int:
		return self._capacity

	def get_liquids(self) -> List[chr]:
		return self._liquids

	def get_level(self) -> int:
		return len(self._liquids)

	def is_full(self) -> bool:
		return len(self._liquids) >= self._capacity

	def is_empty(self) -> bool:
		return not bool(self._liquids)

	def is_pure(self) -> bool:
		return not self.is_empty() and all(l == self._liquids[0] for l in self._liquids)

	def get_liquid(self, index: int) -> chr:
		return self._liquids[index] if index < len(self._liquids) else None

	def _pop_liquid(self) -> chr:
		if self.is_empty():
			return None
		return self._liquids.pop()

	def _push_liquid(self, liquid: chr):
		if self.is_full():
			raise ValueError("Potions is full")
		if not (self.is_empty() or self.peek_liquid() == liquid):
			raise ValueError(str(self) + " Cannot add liquid " + liquid + " on top of " + self.peek_liquid())
		self._liquids.append(liquid)

	def peek_liquid(self) -> chr:
		if self._liquids:
			return self._liquids[-1]
		else:
			return None

	def peek_liquid_depth(self) -> int:
		if not self._liquids:
			return 0
		peek = self.peek_liquid()
		for i in range(-2, -(self.get_level() + 1), -1):
			if self.get_liquid(i) != peek:
				return -(i + 1)
		return self.get_level()


	def can_be_poured_into(self, other) -> bool:
		if other.get_capacity() - other.get_level() < self.peek_liquid_depth():
			return False
		return other.is_empty() or self.peek_liquid() == other.peek_liquid()

	def pour_into(self, other):
		if other is self:
			raise ValueError("Cannot pour potion into itself")
		if not self.can_be_poured_into(other):
			return None
		pour_count = self.peek_liquid_depth()
		for i in range(pour_count):
			other._push_liquid(self._pop_liquid())
		from solve.pourAction import PourAction
		return PourAction(self.index, other.index, pour_count)

	def __repr__(self):
		contents_str = "".join(self._liquids)
		return "#" + str(self.index) + " [" + contents_str.ljust(self._capacity) + "]"
