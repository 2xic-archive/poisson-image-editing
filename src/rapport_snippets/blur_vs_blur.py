from PIL import Image
from rapport_snippets.figs import *
from backend import blurring
from backend import non_edge_blurring
import scipy
import scipy.ndimage
import scipy.misc
import matplotlib.pyplot as plt
from matplotlib.pyplot import imread, imshow
import numpy as np
from scipy import ndimage


def compile_non_edge_blur(output_dir="./rapport_snippets/output/"):
	"""
	Compiles a .tex file for the non edge blur function

	Parameters
	----------
	output_dir : str
		the location to store the .tex with images
	"""

	make_dir(output_dir)

	non_edge_blur = non_edge_blurring.non_edge_blur("./files/test_images/lena.png")#
	blur = blurring.blur("./files/test_images/lena.png")	

	epoch_count = {
		0.2:[5, 10, 25]
	}

	results_doc = doc()
	path_latex = "glatting/glatting_vs_glatting/"

	for color in [False, True]:
		if color:
			non_edge_blur.change_color_state()
			blur.change_color_state()

		for alpha in epoch_count:
			"""
			Run for the non edge blur
			"""
			for epochs in epoch_count[alpha]:
				non_edge_blur.reset()
				non_edge_blur.alpha = alpha
				non_edge_blur.fit(epochs)
				non_edge_blur.save("{}/kant_blur_{}_{}_{}.png".format(output_dir, color, alpha, epochs))
				results_doc.add_row_element(subfigure(path=path_latex + "/kant_blur_{}_{}_{}.png".format(color, alpha, epochs), text="fancy blur($K={}, \\alpha = {}$, iteration={})".format(non_edge_blur.k, alpha, epochs)))

			"""
			Run for the edge blur
			"""
			results_doc.add_row()
			for epochs in epoch_count[alpha]:
				blur.reset()
				blur.alpha = alpha
				blur.fit(epochs)

				results_doc.add_row_element(subfigure(path=path_latex + "/blur_{}_{}_{}.png".format(color, alpha, epochs), text="Vanlig blur($\\alpha = {}$, iteration={})".format(alpha, epochs)))
				blur.save("{}/blur_{}_{}_{}.png".format(output_dir,color,alpha,epochs))
			results_doc.add_row()

	results_doc.add_caption("Blur mot Blur")
	results_doc.add_ref("Blur_vs_blur")
	results_doc.save("{}/results.tex".format(output_dir))




