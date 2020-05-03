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
	contrast_obj = non_edge_blurring.non_edge_blur("./files/test_images/lena.png")#"./files/test_images/orange.png", "./files/test_images/apple.png")
	blur = blurring.blur("./files/test_images/lena.png")#"./files/test_images/orange.png", "./files/test_images/apple.png")
	
	epoch_count = {
		0.2:[5, 10, 25]#,
		#0.5:[5, 10, 25]
	}

	results_doc = doc()
	path_latex = "glatting/glatting_vs_glatting/"

	count = 0
	for color in [False, True]:
		if color:
			contrast_obj.change_color_state()
			blur.change_color_state()

		for alpha in epoch_count:
			for epochs in epoch_count[alpha]:
				contrast_obj.reset()
				contrast_obj.alpha = alpha
				contrast_obj.fit(epochs)
				contrast_obj.save(output_dir + "glatting_vs_glatting/" + "/kant_blur_{}_{}_{}.png".format(color,alpha,epochs))
				results_doc.add_row_element(subfigure(path=path_latex + "/blur_{}_{}_{}.png".format(color,alpha,epochs), text="Vanlig blur($\\alpha = {}$, iteration={})".format(alpha, epochs)))

			results_doc.add_row()
			for epochs in epoch_count[alpha]:
				blur.reset()
				blur.alpha = alpha
				blur.fit(epochs)

				results_doc.add_row_element(subfigure(path=path_latex + "/kant_blur_{}_{}_{}.png".format(color,alpha,epochs), text="fancy blur($K=10000, \\alpha = {}$, iteration={})".format(alpha, epochs)))
				blur.save(output_dir + "glatting_vs_glatting/" + "/blur_{}_{}_{}.png".format(color,alpha,epochs))
			results_doc.add_row()
#	results_doc.add_row()
	results_doc.add_caption("Blur mot Blur")
	results_doc.add_ref("Blur_vs_blur")
	results_doc.save("{}/glatting_vs_glatting/results.tex".format(output_dir))




