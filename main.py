from solve import puzzleSolve as ps, potionParse as pp, puzzleDisplay as pd
from detect import potionDetect as pdt

if __name__ == '__main__':
	potions = pdt.detect_potions("./data/img_02.PNG")
	# potions = pp.parse_potion_file("./data/puzzle08.txt")

	print(potions)
	result = ps.find_pour_solution(potions)
	pd.display_solution(potions, result)
