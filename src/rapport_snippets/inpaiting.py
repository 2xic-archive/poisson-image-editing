from backend import inpaiting
from extra import local_adaptive_histogram
from PIL import Image
from rapport_snippets.figs import *
import numpy as np
from extra.median_filter import median_filter

def compile(output_path):
	"""
	Compiles a .tex file for the inpaiting function

	Parameters
	----------
	output_dir : str
		the location to store the .tex with images
	"""

	epoch_count = {
		0.25:[3, 5, 8],
		0.5:[3, 5, 8],
		0.75:[3, 5, 8]
	}

	if not os.path.isdir(output_path):
		os.mkdir(output_path)		

	contrast_obj = inpaiting.inpaint("./files/test_images/lena.png")
	input_image = contrast_obj.destroy_information()#.copy()

	for color in [True, False]:
		naming = "_color" if color else "_gray"

		output_path_new = "{}inpainting{}/".format(output_path, naming)

		if not (color == contrast_obj.color):
			contrast_obj.change_color_state()
		make_dir(output_path_new)


		results_doc = doc()
		results_doc.add_row_element(subfigure(path="inpainting/inpainting{}/input.png".format(naming), text="Input image"))
		results_doc.add_row()

		results_doc = compile_doc(contrast_obj, epoch_count, "{}".format(output_path_new), "inpainting/inpainting{}".format(naming),
			extra=lambda x: x.destroy_information(), results_doc=results_doc)
		results_doc.save("{}/results.tex".format(output_path_new))

		Image.fromarray(np.uint8(255 * contrast_obj.original_data_copy)).save("{}/input.png".format(output_path_new))

def compile_median(output_path):
	make_dir(output_path)

	method = inpaiting.inpaint("./files/test_images/lena.png", True)

	method.destroy_information(3)

	median = method.original_data_copy.copy()

	for i in range(10):
		median = median_filter(median, method.mask)
	method.fit(epochs=10)

	Image.fromarray(np.uint8(255 * method.data)).save("{}/poisson.png".format(output_path))
	Image.fromarray(np.uint8(255 * median)).save("{}/median.png".format(output_path))
	Image.fromarray(np.uint8(255 * method.original_data_copy)).save("{}/input.png".format(output_path))

	results_doc = doc()
	results_doc.add_row_element(subfigure(path="inpainting/median/input.png", text="Input image"))
	results_doc.add_row_element(subfigure(path="inpainting/median/poisson.png", text="poisson image"))
	results_doc.add_row_element(subfigure(path="inpainting/median/median.png", text="median image"))
	results_doc.add_ref("median_vs_poisson")
	results_doc.add_row()

	results_doc.save("{}/results.tex".format(output_path))







