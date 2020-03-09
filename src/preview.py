import matplotlib.pyplot as plt
import blurring
import numpy as np
from PIL import Image
import argparse
parser = argparse.ArgumentParser(description='vitprog')
parser.add_argument('function', type=str,
                    help='The function to preview')
parser.add_argument('--image', type=str,
					help='(optional) image to test on (default = lena).')
args = parser.parse_args()
#print(args.function)
#print(args.image)

def preview(function_def):
	image = function_def("test_images/lena.png", True)

	plt.ion()
	if(image.color):
		plt.imshow(image.data)
	else:
		plt.imshow(image.data, plt.cm.gray)

	plt.draw()

	epoch = 1
	while True:
		try:
			image.fit(1)
			if(image.color):
				plt.imshow(image.data)
			else:
				plt.imshow(image.data, plt.cm.gray)
			plt.draw()
			plt.title("Epoch {} (Alpha = {})".format(epoch, image.alpha))
			plt.pause(1)
			epoch += 1
		except Exception as e:
			print(e)
			break
	plt.close()

if __name__ == "__main__":
	if(args.function == "blur"):
		preview(blurring.blur)
	else:
		raise NotImplementedError


