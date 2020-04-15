from backend import demosaicing
from extra import local_adaptive_histogram
from PIL import Image
from rapport_snippets.figs import *
import numpy as np



def compile(output_dir="demosaic"):
	contrast_obj = demosaicing.Demosaic("./files/test_images/lena.png", True)

	epoch_count = {
		0.25:[1, 3, 5],
		0.5:[1, 3, 5],
		0.75:[1, 3, 5]
	}



	results_doc = compile_doc(contrast_obj, epoch_count, "{}/demosaic/".format(output_dir), "demosaic/demosaic", extra=lambda x: x.simulate())#,

	results_doc.save("{}/demosaic/results.tex".format(output_dir))


