from PIL import Image
from rapport_snippets.figs import *
from backend import non_edge_blurring


def compile(output_dir="./rapport_snippets/output/"):
	"""
	Compiles a .tex file for the non edge blurring function

	Parameters
	----------
	output_dir : str
		the location to store the .tex with images
	"""
	for color in [True, False]:
		name = ("color" if color else "gray")
		output_dir_path =  output_dir + name
		make_dir(output_dir_path)

		blurring_obj = non_edge_blurring.non_edge_blur("./files/test_images/lena.png", color)
		epoch_count = {
			0.25:[3, 5, 10],
			0.5:[1, 3, 5, 10],
			0.75:[1, 3, 5, 10]
		}
		results_doc = compile_doc(blurring_obj, epoch_count, "{}/".format(output_dir_path), "glatting/non_edge_blur_{}/".format(name))
		results_doc.save("{}/results.tex".format(output_dir_path))