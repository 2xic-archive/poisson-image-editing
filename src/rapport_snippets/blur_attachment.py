
from PIL import Image
import sys
sys.path.append("./")
from backend import inpaiting
from extra import local_adaptive_histogram
from PIL import Image
from rapport_snippets.figs import *
import numpy as np
#from figs import *
from backend import blurring


def compile(output_dir):
	"""
	Compiles a .tex file for the blur function with data attachment

	Parameters
	----------
	output_dir : str
		the location to store the .tex with images
	"""

	make_dir(output_dir)

	path_latex = "glatting/attachment/"
	
	epochs = 1000
	lambda_val = 0.1

	results_doc = doc()
	blurring_obj = blurring.blur("./files/test_images/lena.png", True)
	blurring_obj.fit(epochs)

	"""
	Image to compare with
	"""
	name = "fit_{}_lambda_{}.png".format(epochs, 0)
	blurring_obj.save("{}/{}".format(output_dir, name))
	results_doc.add_row_element(subfigure(path="{}/{}".format(path_latex, name), text="Bilde uten attachment"))
	
	for epoch in [10, 100, epochs]:
		blurring_obj.reset()
		blurring_obj.set_lambda_size(lambda_val)
		blurring_obj.fit(epoch)

		name = "fit_{}_lambda_{}.png".format(epoch, lambda_val)
		blurring_obj.save("{}/{}".format(output_dir, name))
		results_doc.add_row_element(subfigure(path="{}/{}".format(path_latex, name), text="Bilde med attachment"))

	results_doc.add_row()
	results_doc.save(output_dir + "/resultat.tex")
