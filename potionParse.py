from typing import List
from typing import Dict
from potion import Potion


def parse_potion_file(file_path: str) -> List[Potion]:
	potions = []
	with open(file_path, "r") as f:
		for i, line in enumerate(f):
			if line.strip():
				potions.append(parse_potion(line.strip(), i))
	first_capacity = potions[0].get_capacity()
	if not all(p.get_capacity() == first_capacity for p in potions):
		raise ValueError("Not all potions have capacity " + str(first_capacity))
	if not all(first_capacity == count for count in count_liquids(potions).values()):
		raise ValueError("Not all liquids are present " + str(first_capacity) + " times")
	return potions


def count_liquids(pots: List[Potion]) -> Dict[chr, int]:
	scores = {}
	for pot in pots:
		if pot.is_full() and pot.is_pure():
			continue
		for i, liquid in enumerate(pot.get_liquids()):
			scores[liquid] = scores.get(liquid, 0) + 1
	return scores


def parse_potion(potion_string: str, pot_index: int = 0) -> Potion:
	potion = Potion(pot_index, len(potion_string), [liquid_chr for liquid_chr in potion_string if liquid_chr != "#"])
	return potion
