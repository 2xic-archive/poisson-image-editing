from backend import grayscale
from PIL import Image
from rapport_snippets.figs import *
import numpy as np



def compile():
	contrast_obj = grayscale.grayscale("./files/test_images/lena.png", True)

	epoch_count = {
		0.25:[1, 3, 5],
		0.5:[1, 3, 5],
		0.75:[1, 3, 5]
	}


	results_doc = compile_doc(contrast_obj, epoch_count, "./rapport_snippets/output/grayscale/", "grayscale/grayscale")

	results_doc.save("rapport_snippets/output/grayscale/results.tex")


