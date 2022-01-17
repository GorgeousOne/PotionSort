from copy import deepcopy
from typing import List

from potion import Potion
from pourAction import PourAction
import potionParse as pp


def display_solution(pots: List[Potion], pours: List[PourAction]):
	display_potions(pots)
	for pour in pours:
		print("-" * (len(pots) * 7 - 4))
		display_pour(pots, pour)
		print()
		apply_pour(pots, pour)
		display_potions(pots)


def display_potions(pots: List[Potion]):
	capacity = pots[0].get_capacity()
	for i in range(capacity - 1, -1, -1):
		for p in pots:
			print_flask_piece(p, i)
			print_space(1, 4)
		print()


def display_pour(pots: List[Potion], pour: PourAction):
	i_from = pour.fromIndex
	i_to = pour.toIndex
	pot_from = potions[i_from]
	pot_to = potions[i_to]

	capacity = pots[0].get_capacity()
	for i in range(capacity - 1, -1, -1):
		if i_from < i_to:
			print_space(i_from)
			print_flask_piece(pot_from, i)

			if pot_from.get_level() > i >= pot_from.get_level() - pour.liquid_count:
				print(" -> ", end="")
			else:
				print_space(1, 4)
			print_space(i_to - i_from - 1)
			print_flask_piece(pot_to, i)

		else:
			print_space(i_to)
			print_flask_piece(pot_to, i)
			print_space(i_from - i_to - 1)

			if pot_from.get_level() > i >= pot_from.get_level() - pour.liquid_count:
				print(" <- ", end="")
			else:
				print_space(1, 4)

			print_flask_piece(pot_from, i)

		print()

def print_space(cols, col_width = 7):
	print(" " * cols * col_width, end="")


def print_flask_piece(pot: Potion, index: int):
	print("|", pot.get_liquid(index) if pot.get_level() > index else " ", "|", sep="", end="")


def apply_pour(pots: List[Potion], pour: PourAction):
	pot_from = pots[pour.fromIndex]
	pot_to = pots[pour.toIndex]
	for i in range(pour.liquid_count):
		pot_to.push_liquid(pot_from.pop_liquid())

if __name__ == '__main__':
	potions = pp.parse_potion_file("./res/puzzle05.txt")

	test = deepcopy(potions)
	pours = [test[0].pour_into(test[3]), test[2].pour_into(test[0])]

	# display_potions(potions)
	display_solution(potions, pours)
