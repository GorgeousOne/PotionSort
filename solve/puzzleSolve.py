from copy import deepcopy
from typing import List, Tuple

from solve.potion import Potion
from solve.pourAction import PourAction
from solve import puzzleDisplay as pd

counter = 0
original = None


def find_pour_solution(pots: List[Potion], pours=None, pour_indices: Tuple[int, int] = None, last_pour_indices: Tuple[int, int] = None) -> List[PourAction]:
	global counter
	global original

	if not pours:
		original = deepcopy(pots)
		pours = []

	if pour_indices is not None:
		# if pour_indices[::-1] == last_pour_indices:
		# 	return None
		# if pots[pour_indices[0]].is_pure() and pots[pour_indices[1]].is_pure() and pour_indices[0] > pour_indices[1]:
		# 	return None
		pots = deepcopy(pots)
		pours = deepcopy(pours)
		pours.append(pots[pour_indices[0]].pour_into(pots[pour_indices[1]]))

	if is_puzzle_solved(pots):
		counter += 1
		if counter % 1000 == 0:
			print(counter)
		return None
		# return pours
	liquids = sort_liquids_by_max_index(pots)

	# fill liquids into already pure potions
	for pure_index in find_pure_unfull_pots(pots):
		l = pots[pure_index].peek_liquid()
		for pot_index in find_pots_with_top_liquid(pots, l):
			if not pots[pot_index].can_be_poured_into(pots[pure_index]):
				continue
			result = find_pour_solution(pots, pours, (pot_index, pure_index), pour_indices)
			if result:
				return result
	# fill empty flasks
	for empty_index in find_empty_pots(pots):
		for l in liquids:
			for pot_index in find_pots_with_top_liquid(pots, l, True):
				result = find_pour_solution(pots, pours, (pot_index, empty_index), pour_indices)
				if result:
					return result
	# decant any potion into any other (brute force)
	for l in liquids:
		pot_indices = find_pots_with_top_liquid(pots, l)
		for i2 in pot_indices:
			if pots[i2].is_empty() or pots[i2].is_pure():
				continue
			for i in pot_indices:
				if not pots[i].can_be_poured_into(pots[i2]):
					continue
				result = find_pour_solution(pots, pours, (i, i2), pour_indices)
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
