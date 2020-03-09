import matplotlib.pyplot as plt
import blurring
import numpy as np
from PIL import Image
import argparse
import inpaiting
parser = argparse.ArgumentParser(description='vitprog')
parser.add_argument('function', type=str,
                    help='The function to preview')
parser.add_argument('--image', type=str,
					help='(optional) image to test on (default = lena).')
parser.add_argument('--color', type=int,
					help='(optional) color gray or color')
args = parser.parse_args()
#print(args.function)
#print(args.image)

def preview(image):
#	image = function_def("test_images/lena.png", True)
	plt.ion()
	if(image.color):
		plt.imshow(image.data)
	else:
		plt.imshow(image.data, plt.cm.gray)

	plt.draw()
	epoch = 0
	plt.title("Epoch {} (Alpha = {})".format(epoch, image.alpha))			
	plt.pause(1)
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
	image_path = "test_images/lena.png" if args.image is None else args.image
	color = True if args.color is None else bool(args.color)
	print(color, args.color)
	if(args.function == "blur"):
		image = blurring.blur(image_path, color)
		image.add_nosise()
		preview(image)
	elif(args.function == "inpaiting"):
		image = inpaiting.inpait(image_path, color)
	#	image.add_nosise()
		preview(image)
	else:
		raise NotImplementedError
