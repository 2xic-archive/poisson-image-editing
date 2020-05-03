from backend import anonymizing
from extra import local_adaptive_histogram
from PIL import Image
from rapport_snippets.figs import *
import numpy as np


def compile(output_dir="./rapport_snippets/output"):
	anon_obj = anonymizing.anonymous("./files/test_images/lena.png", True)

	epoch_count = {
		0.25:[1, 5, 10],
		0.3:[15, 30, 50]
	#	0.5:[5, 10, 15],
	#	0.75:[5, 10, 15]
	}


	#	https://previews.123rf.com/images/kurhan/kurhan1610/kurhan161000486/64970219-collection-of-smiling-faces-set-of-people-men-women-seniors-diversity-.jpg

	results_doc = compile_doc(anon_obj, epoch_count, "{}/anonymizing/".format(output_dir), "anonymisering/anonymizing")
	results_doc.save("{}/anonymizing/results.tex".format(output_dir))


