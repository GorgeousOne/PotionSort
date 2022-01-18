from typing import List


class Potion:

	def __init__(self, index: int, capacity: int, contents: List[chr]):
		self.index = index
		self._capacity = capacity
		self._liquids = contents

	def get_capacity(self) -> int:
		return self._capacity

	def can_push_liquid(self, liquid: chr, amount: int = 1) -> bool:
		if self._capacity - self.get_level() < amount:
			return False
		return self.is_empty() or liquid == self.peek_liquid()

	def push_liquid(self, liquid_char: chr):
		if not self.can_push_liquid(liquid_char):
			raise ValueError("Cannot add liquid " + liquid_char + " to potion " + str(self))
		self._liquids.append(liquid_char)

	def get_liquid(self, index: int) -> chr:
		return self._liquids[index] if index < len(self._liquids) else None

	def pop_liquid(self) -> chr:
		return self._liquids.pop()

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

	def is_full(self) -> bool:
		return len(self._liquids) >= self._capacity

	def is_empty(self) -> bool:
		return not bool(self._liquids)

	def is_pure(self) -> bool:
		return not self.is_empty() and all(l == self._liquids[0] for l in self._liquids)

	def get_level(self) -> int:
		return len(self._liquids)

	def pour_into(self, other):
		pour_count = 0
		while True:
			if self.is_empty() or not other.can_push_liquid(self.peek_liquid()):
				break
			other.push_liquid(self.pop_liquid())
			pour_count += 1
		from pourAction import PourAction
		return PourAction(self.index, other.index, pour_count) if pour_count > 0 else None

	def __repr__(self):
		contents_str = "".join(self._liquids)
		return "[" + contents_str.ljust(self._capacity) + "]"

	def get_liquids(self) -> List[chr]:
		return self._liquids
