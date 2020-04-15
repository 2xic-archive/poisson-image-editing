from backend import grayscale
from PIL import Image
from rapport_snippets.figs import *
import numpy as np



def compile(output_dir="./rapport_snippets/output"):
	contrast_obj = grayscale.grayscale("./files/test_images/lena.png", True)

	epoch_count = {
		0.25:[1, 3, 5],
		0.5:[1, 3, 5],
		0.75:[1, 3, 5]
	}


	results_doc = compile_doc(contrast_obj, epoch_count, "{}/grayscale/".format(output_dir), "grayscale/grayscale")

	results_doc.save("{}/grayscale/results.tex".format(output_dir))


