from copy import deepcopy
from typing import List
from colored import fg, attr

from potion import Potion
from pourAction import PourAction
import potionParse as pp


def display_solution(pots: List[Potion], pours: List[PourAction], use_colors: bool = True):
	display_potions(pots, use_colors)
	for pour in pours:
		print("-" * (len(pots) * 7 - 4))
		display_pour(pots, pour, use_colors)
		print()
		apply_pour(pots, pour)
	display_potions(pots, use_colors)


def display_potions(pots: List[Potion], use_colors: bool = True):
	capacity = pots[0].get_capacity()
	for i in range(capacity - 1, -1, -1):
		for p in pots:
			print_flask_piece(p, i, use_colors)
			print_space(1, 4)
		print()


def display_pour(pots: List[Potion], pour: PourAction, use_colors: bool = True):
	i_from = pour.fromIndex
	i_to = pour.toIndex
	pot_from = pots[i_from]
	pot_to = pots[i_to]

	capacity = pots[0].get_capacity()
	for i in range(capacity - 1, -1, -1):
		if i_from < i_to:
			print_space(i_from)
			print_flask_piece(pot_from, i, use_colors)

			if pot_from.get_level() > i >= pot_from.get_level() - pour.liquid_count:
				print(" -> ", end="")
			else:
				print_space(1, 4)
			print_space(i_to - i_from - 1)
			print_flask_piece(pot_to, i, use_colors)

		else:
			print_space(i_to)
			print_flask_piece(pot_to, i, use_colors)
			print_space(i_from - i_to - 1)

			if pot_from.get_level() > i >= pot_from.get_level() - pour.liquid_count:
				print(" <- ", end="")
			else:
				print_space(1, 4)

			print_flask_piece(pot_from, i, use_colors)

		print()


def print_space(cols, col_width=7):
	print(" " * cols * col_width, end="")


colors = {
	"k": "#E48CE9",
	"r": "#C95B57",
	"o": "#E98135",
	"i": "#EEB762",
	"y": "#FDF475",
	"l": "#72CF73",
	"g": "#388122",
	"s": "#51B4E7",
	"b": "#4E73E1",
	"p": "#945ABB",
	"w": "#96735A",
	"e": "#999999",
}


def print_flask_piece(pot: Potion, index: int, use_colors: bool = True):
	liquid = pot.get_liquid(index) if pot.get_level() > index else " "
	if use_colors and liquid in colors:
		liquid = fg(colors[liquid]) + chr(9608) + attr("reset")
	print("|", liquid, "|", sep="", end="")


def apply_pour(pots: List[Potion], pour: PourAction):
	pot_from = pots[pour.fromIndex]
	pot_to = pots[pour.toIndex]
	for i in range(pour.liquid_count):
		pot_to.push_liquid(pot_from.pop_liquid())


if __name__ == '__main__':
	potions = pp.parse_potion_file("res/puzzle04.txt")

	test = deepcopy(potions)
	pours = [test[0].pour_into(test[3]), test[2].pour_into(test[0])]

	# display_potions(potions)
	display_solution(potions, pours)
