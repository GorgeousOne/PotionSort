from typing import List
from potion import Potion


def parse_potion_file(file_path: str) -> List[Potion]:
	potions = []
	with open(file_path, "r") as f:
		for i, line in enumerate(f):
			if line.strip():
				potions.append(parse_potion(line.strip(), i))
	if not all(p.get_capacity() == potions[0].get_capacity() for p in potions):
		raise ValueError("Not all potions have the same capacity")
	return potions


def parse_potion(potion_string: str, pot_index: int = 0) -> Potion:
	potion = Potion(pot_index, len(potion_string), [liquid_chr for liquid_chr in potion_string if liquid_chr != "#"])
	return potion
