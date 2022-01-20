import mimetypes
import sys

from detect import potionDetect as pdt
from solve import puzzleSolve as ps, potionParse as pp, puzzleDisplay as pd

if __name__ == '__main__':

	if len(sys.argv) > 1:
		puzzle_path = sys.argv[1]
	else:
		puzzle_path = "./data/img_00.PNG"
		print("Reading from rxample image:", puzzle_path)

	mimetypes.init()
	mime_start = mimetypes.guess_type(puzzle_path)[0]
	potions = None

	if "image" in mime_start:
		potions = pdt.detect_potions(puzzle_path)
	elif mime_start == "text/plain":
		potions = pp.parse_potion_file(puzzle_path)
	else:
		raise ValueError(puzzle_path + " is not an image or plain text but " + mime_start)

	result = ps.find_pour_solution(potions)

	if result:
		pd.display_solution(potions, result)
	else:
		print("Could not find a solution for the puzzle :(")
