from backend import demosaicing
from extra import local_adaptive_histogram
from PIL import Image
from rapport_snippets.figs import *
import numpy as np



def compile():
	contrast_obj = demosaicing.Demosaic("./files/test_images/lena.png", True)

	epoch_count = {
		0.25:[1, 3, 5],
		0.5:[1, 3, 5],
		0.75:[1, 3, 5]
	}



	results_doc = compile_doc(contrast_obj, epoch_count, "./rapport_snippets/output/demosaic/", "demosaic/demosaic")#,

	results_doc.save("rapport_snippets/output/demosaic/results.tex")


