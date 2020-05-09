from backend import anonymizing
from extra import local_adaptive_histogram
from PIL import Image
from rapport_snippets.figs import *
import numpy as np


def compile(output_dir="./rapport_snippets/output"):
	"""
	Compiles a .tex file for the anonymizing function

	Parameters
	----------
	output_dir : str
		the location to store the .tex with images
	"""
	make_dir(output_dir)

	anon_obj = anonymizing.anonymous("./files/test_images/lena.png", True)
	epoch_count = {
		0.25:[1, 5, 10, 100],
		0.3:[15, 30, 50]
	}
	path_latex = "anonymisering/resultat/"

	results_doc = compile_doc(anon_obj, epoch_count, output_path=output_dir, path_latex=path_latex)
	results_doc.save("{}/resultat.tex".format(output_dir))