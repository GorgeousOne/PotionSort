from typing import List


class Potion:

	def __init__(self, index: int, capacity: int, contents: List[chr]):
		self.index = index
		self._capacity = capacity
		self._contents = contents

	def get_capacity(self) -> int:
		return self._capacity

	def can_push_liquid(self, liquid: chr) -> bool:
		if self.is_full():
			return False
		return self.is_empty() or liquid == self.peek_liquid()

	def push_liquid(self, liquid_char: chr):
		if not self.can_push_liquid(liquid_char):
			raise ValueError("Cannot add liquid " + liquid_char + " to potion " + str(self))
		self._contents.append(liquid_char)

	def get_liquid(self, index: int) -> chr:
		return self._contents[index] if index < len(self._contents) else None

	def pop_liquid(self) -> chr:
		return self._contents.pop()

	def peek_liquid(self) -> chr:
		if self._contents:
			return self._contents[-1]
		else:
			return None

	def is_full(self) -> bool:
		return len(self._contents) >= self._capacity

	def is_empty(self) -> bool:
		return not bool(self._contents)

	def is_pure(self) -> bool:
		return not self.is_empty() and all(l == self._contents[0] for l in self._contents)

	def get_level(self) -> int:
		return len(self._contents)

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
		contents_str = "".join(self._contents)
		return "[" + contents_str.ljust(self._capacity) + "]"