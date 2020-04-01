from backend import anonymizing
from extra import local_adaptive_histogram
from PIL import Image
from rapport_snippets.figs import *
import numpy as np


def compile():
	contrast_obj = anonymizing.anonymous("./files/test_images/faces.jpg", True)

	epoch_count = {
		0.25:[1, 5, 10],
		0.3:[15, 30, 50]
	#	0.5:[5, 10, 15],
	#	0.75:[5, 10, 15]
	}


	#	https://previews.123rf.com/images/kurhan/kurhan1610/kurhan161000486/64970219-collection-of-smiling-faces-set-of-people-men-women-seniors-diversity-.jpg

	results_doc = compile_doc(contrast_obj, epoch_count, "./rapport_snippets/output/anonymizing/", "anonymisering")

	results_doc.save("rapport_snippets/output/anonymizing/results.tex")


