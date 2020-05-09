from backend import matting, blurring
from extra import local_adaptive_histogram
from PIL import Image
from rapport_snippets.figs import *
import numpy as np

def compile_parameters(output_dir="./rapport_snippets/output/"):
	"""
	Compiles a .tex file for the laplacian function

	Parameters
	----------
	output_dir : str
		the location to store the .tex with images
	"""

	blurring_obj = blurring.blur("./files/test_images/lena.png", False)
	blurring_obj.data[1:-1, 1:-1] = blurring_obj.get_laplace_explicit(blurring_obj.data, alpha=False)
	blurring_obj.save("{}/laplacian.png".format(output_dir))

	x = doc()
	x.add_row_element(subfigure(path="./img/laplacian.png", text="Bilde med 100 iterations"))
	x.add_row()
	x.add_caption("laplacian")
	x.add_ref("LaplacianImg")
	x.save("{}/results.tex".format(output_dir))