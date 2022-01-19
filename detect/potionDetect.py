import cv2 as cv

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


def is_contour_potion(img_width, contour):
	min_h = img_width / 4
	x, y, w, h = cv.boundingRect(contour)
	return h > min_h


def find_potions(img, contours):
	potions = []

	for i, cnt in enumerate(contours):
		x, y, w, h = cv.boundingRect(cnt)
		img_potion = img[y:y + h, x:x + w]
		colors = find_potion_colors(img_potion)

		mid = int(w / 2)
		for i in range(1, 5):
			y = int(h / 5 * i)
			cv.line(img_potion, (mid - 10, y), (mid + 10, y), (0, 0, 255), 2)

		cv.imshow(str(i), img_potion)


def find_potion_colors(img_potion, y_start=0, y_end=None):
	if y_end is None:
		y_end = img_potion.shape[0]


	pass


if __name__ == '__main__':
	image = cv.imread("../data/img01.bmp")
	aspect = image.shape[1] / image.shape[0]

	image = cv.resize(image, (int(1000 * aspect), 1000), interpolation=cv.INTER_AREA)
	img_h = image.shape[0]
	img_w = image.shape[1]

	blur = cv.bilateralFilter(image, 9, 75, 75)
	gray = cv.cvtColor(blur, cv.COLOR_BGR2GRAY)
	thresh = cv.adaptiveThreshold(gray, 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C, cv.THRESH_BINARY, 7, 2)
	# invert image in so findContours doesn't draw contour around the hole image
	thresh = 255 - thresh

	contours, hierarchy = cv.findContours(image=thresh, mode=cv.RETR_EXTERNAL, method=cv.CHAIN_APPROX_NONE)

	contours = list(filter(lambda c: is_contour_potion(img_w, c), contours))

	cv.drawContours(image=image, contours=contours, contourIdx=-1, color=(255, 0, 0), thickness=2, lineType=cv.LINE_AA)

	y1 = int(img_h * 1 / 4)
	cv.line(image, (0, y1), (0, y1 + int(img_w / 4)), (255, 0, 0), 5)

	find_potions(blur, contours)
	# cv.imshow("clear", image)
	# cv.imshow("blur", blur)
	cv.waitKey(0)
	cv.destroyAllWindows()
