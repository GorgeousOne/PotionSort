from copy import deepcopy
from typing import List

from potion import Potion
from pourAction import PourAction


def find_pour_solution(pots: List[Potion], pours=None, pot_index_from: int = None, pot_index_to: int = None) -> List[PourAction]:
	if not pours:
		pours = []
	pots = deepcopy(pots)
	pours = deepcopy(pours)

	if pot_index_from is not None and pot_index_to is not None:
		pours.append(pots[pot_index_from].pour_into(pots[pot_index_to]))
	if is_puzzle_solved(pots):
		return pours
	liquids = sort_liquids_by_max_index(pots)

	# fill liquids into already pure potions
	for pure_index in find_pure_unfull_pots(pots):
		l = pots[pure_index].peek_liquid()
		for pot_index in find_pots_with_top_liquid(pots, l, True):
			if not pots[pot_index].can_be_poured_into(pots[pure_index]):
				continue
			result = find_pour_solution(pots, pours, pot_index, pure_index)
			if result:
				return result
	# fill empty flasks
	for empty_index in find_empty_pots(pots):
		for l in liquids:
			for pot_index in find_pots_with_top_liquid(pots, l, True):
				result = find_pour_solution(pots, pours, pot_index, empty_index)
				if result:
					return result
	# decant any potion into any (brute force)
	for l in liquids:
		pot_indices = find_pots_with_top_liquid(pots, l)
		for i in pot_indices:
			for i2 in pot_indices:
				if i == i2 or not pots[i].can_be_poured_into(pots[i2]):
					continue
				result = find_pour_solution(pots, pours, i, i2)
				if result:
					return result
	return None


def get_index(pot: Potion):
	return pot.index


def find_pots_with_top_liquid(pots, liquid: chr, mixed_only: bool = False) -> List[int]:
	return list(
		map(get_index, filter(lambda pot: pot.peek_liquid() == liquid and not (mixed_only and pot.is_pure()), pots)))


def find_empty_pots(pots: List[Potion]) -> List[int]:
	return list(map(get_index, filter(lambda pot: pot.is_empty(), pots)))


def find_pure_unfull_pots(pots: List[Potion]) -> List[int]:
	return list(map(get_index, filter(lambda pot: not pot.is_full() and pot.is_pure(), pots)))


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
