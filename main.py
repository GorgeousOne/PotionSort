import potionParse as pp
import puzzleSolve as ps
import puzzleDisplay as pd

if __name__ == '__main__':
	potions = pp.parse_potion_file("res/puzzle07.txt")
	result = ps.find_pour_solution(potions)
	pd.display_solution(potions, result)
