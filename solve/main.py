from solve import puzzleSolve as ps, potionParse as pp, puzzleDisplay as pd

if __name__ == '__main__':
	potions = pp.parse_potion_file("data/puzzle09.txt")
	result = ps.find_pour_solution(potions)
	pd.display_solution(potions, result)
