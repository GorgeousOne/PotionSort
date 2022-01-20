import math
from functools import cmp_to_key
from typing import List, Tuple

import cv2 as cv
import numpy as np

from solve.potion import Potion

potion_colors = {
	"k": np.array([228, 140, 233]),
	"r": np.array([201, 91, 87]),
	"o": np.array([233, 129, 53]),
	"i": np.array([238, 183, 98]),
	"y": np.array([253, 244, 117]),
	"l": np.array([114, 207, 115]),
	"g": np.array([56, 129, 34]),
	"s": np.array([81, 180, 231]),
	"b": np.array([78, 115, 225]),
	"p": np.array([148, 90, 187]),
	"w": np.array([150, 115, 90]),
	"e": np.array([153, 153, 153]),
}


def is_contour_potion(img_width, contour):
	min_h = img_width / 4
	x, y, w, h = cv.boundingRect(contour)
	return h > min_h


def find_potions(img, contours):
	potions = []
	potion_liquids = []
	all_liquids = []
	contours.sort(key=cmp_to_key(compare_y_x))

	for i, cnt in enumerate(contours):
		x, y, w, h = cv.boundingRect(cnt)
		img_potion = img[y:y + h, x:x + w]
		liquids = find_potion_colors(img_potion)
		all_liquids += liquids
		potion_liquids.append(liquids)

	liquids_unit = calculate_liquid_unit([liquid[1] for liquid in all_liquids])
	x, y, w, h = cv.boundingRect(contours[0])
	max_capacity = math.floor(h / liquids_unit)

	for i, liquids in enumerate(potion_liquids):
		liquids.reverse()
		potions.append(create_potion(liquids, liquids_unit, max_capacity, i))
	return potions


def compare_y_x(cnt1, cnt2):
	x1, y1, w1, h1 = cv.boundingRect(cnt1)
	x2, y2, w2, h2 = cv.boundingRect(cnt2)
	dx = x2 - x1
	dy = y2 - y1
	if abs(dy) > h1:
		return -np.sign(dy)
	elif abs(dx) > w1:
		return -np.sign(dx)
	return 0


def create_potion(liquids, liquids_unit, capacity, index):
	contents = []
	for liquids in liquids:
		for i in range(round(liquids[1] / liquids_unit)):
			contents.append(liquids[0])
	return Potion(index, capacity, contents)


def calculate_liquid_unit(sizes):
	epsilon = 0.1
	min_size = min(sizes)
	singles = []
	stacks = []
	for elem in sizes:
		if elem / min_size < 1 + epsilon:
			singles.append(elem)
		else:
			stacks.append(elem)
	single_unit = np.mean(singles)
	for elem in stacks:
		count = round(elem / single_unit)
		for i in range(count):
			singles.append(elem / count)
	return np.mean(singles)



def find_potion_colors(img_potion) -> List[Tuple[chr, int]]:
	found_colors = []
	current_color = None
	y_start = None

	x_mid = img_potion.shape[1] // 2
	potion_h = img_potion.shape[0]
	min_size = potion_h / 10

	for y in range(potion_h):
		match = match_color(img_potion[y, x_mid])

		# finishes the current color
		if not match and current_color:
			size = y - y_start
			if size >= min_size:
				found_colors.append((current_color, size))
			current_color = None
			y_start = None
		# enters a new color
		elif not current_color:
			y_start = y
			current_color = match
		# switches from one color to another
		elif current_color != match:
			size = y - y_start
			if size >= min_size:
				found_colors.append((current_color, size))
			current_color = match
			y_start = y

	return found_colors


def match_color(img_color):
	for char, color in potion_colors.items():
		diff = calc_color_diff(color, np.flip(img_color))
		if diff < 50:  # 56 is approximately the minimal distance between 2 existing potion colors
			return char
	return None


def calc_color_diff(c1, c2):
	diff = math.sqrt(
		math.pow(c1[0] - c2[0], 2) +
		math.pow(c1[1] - c2[1], 2) +
		math.pow(c1[2] - c2[2], 2))
	return diff


def numeric_compare(x, y):
	return x - y


def detect_potions(image_path: str):
	image = cv.imread(image_path)
	aspect = image.shape[1] / image.shape[0]

	image = cv.resize(image, (int(1000 * aspect), 1000), interpolation=cv.INTER_AREA)
	img_w = image.shape[1]

	blur = cv.bilateralFilter(image, 9, 75, 75)
	gray = cv.cvtColor(blur, cv.COLOR_BGR2GRAY)
	thresh = cv.adaptiveThreshold(gray, 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C, cv.THRESH_BINARY, 7, 2)
	# invert image in so findContours doesn't draw one contour around the hole image
	thresh = 255 - thresh

	contours, hierarchy = cv.findContours(image=thresh, mode=cv.RETR_EXTERNAL, method=cv.CHAIN_APPROX_NONE)
	contours = list(filter(lambda c: is_contour_potion(img_w, c), contours))

	return find_potions(blur, contours)
