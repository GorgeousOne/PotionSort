from copy import deepcopy
from typing import List

from potion import Potion
from pourAction import PourAction

maxDepth = 0


def find_pour_solution(pots: List[Potion], pours=None, depth: int = 0) -> List[PourAction]:
	global maxDepth
	if depth >= maxDepth + 100:
		maxDepth = depth
		print("deep", maxDepth)

	if not pours:
		pours = []
	if is_puzzle_solved(pots):
		return pours
	liquids = sort_liquids_by_max_index(pots)

	# fill empty flasks
	for empty_index in find_empty_pots(pots):
		for l in liquids:
			for pot_index in find_pots_with_top_liquid(pots, l):
				# stops re-pouring pure flasks into empty ones to stop recursion overflow
				if pots[pot_index].is_pure():
					continue
				copy_pots = deepcopy(pots)
				copy_pours = deepcopy(pours)
				copy_pours.append(copy_pots[pot_index].pour_into(copy_pots[empty_index]))
				result = find_pour_solution(copy_pots, copy_pours, depth + 1)
				if result:
					return result
	for l in liquids:
		pot_indices = find_pots_with_top_liquid(pots, l)
		for i in pot_indices:
			for i2 in pot_indices:
				if i == i2 or not pots[i2].can_push_liquid(l, pots[i].peek_liquid_depth()):
					continue
				copy_pots = deepcopy(pots)
				copy_pours = deepcopy(pours)
				copy_pours.append(copy_pots[i].pour_into(copy_pots[i2]))
				result = find_pour_solution(copy_pots, copy_pours, depth + 1)
				if result:
					return result
	return None


def get_index(pot: Potion):
	return pot.index


def find_pots_with_top_liquid(pots, liquid: chr) -> List[int]:
	return list(map(get_index, filter(lambda pot: pot.peek_liquid() == liquid, pots)))


def find_empty_pots(pots: List[Potion]) -> List[int]:
	return list(map(get_index, filter(lambda pot: pot.is_empty(), pots)))


def sort_liquids_by_max_index(pots: List[Potion]) -> List[chr]:
	scores = {}
	for pot in pots:
		if pot.is_full() and pot.is_pure():
			continue
		for i, liquid in enumerate(pot.get_liquids()):
			scores[liquid] = scores.get(liquid, 0) + pot.get_level() - i
	return sorted(scores.keys(), key=scores.get)


def is_puzzle_solved(pots: List[Potion]):
	return all(pot.is_full() and pot.is_pure() or pot.is_empty() for pot in pots)
