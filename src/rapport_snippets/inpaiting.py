from backend import inpaiting
from extra import local_adaptive_histogram
from PIL import Image
from rapport_snippets.figs import *
import numpy as np

contrast_obj = inpaiting.inpaint("./files/test_images/lena.png", False)

epoch_count = {
	0.25:[1, 3, 5],
	0.5:[1, 3, 5],
	0.75:[1, 3, 5]
}

contrast_obj.destroy_information()

results_doc = compile_doc(contrast_obj, epoch_count, "./rapport_snippets/output/inpainting/", "inpainting/inpainting",
							extra=lambda x: x.destroy_information())
results_doc.save("rapport_snippets/output/inpainting/results.tex")


