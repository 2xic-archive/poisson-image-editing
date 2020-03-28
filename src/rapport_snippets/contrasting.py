from backend import contrasting
from extra import local_adaptive_histogram
from PIL import Image
from rapport_snippets.figs import *
import numpy as np

contrast_obj = contrasting.Contrast("./files/test_images/contrast.jpg", False)

epoch_count = {
	0.25:[1, 3, 5],
	0.5:[1, 3, 5],
	0.75:[1, 3, 5]
}

def intensity():
	import matplotlib.pyplot as plt
	plt.plot(local_adaptive_histogram.intensity(img))
	plt.show()


intensity()

results_doc = compile_doc(contrast_obj, epoch_count, "./rapport_snippets/output/contrast/", "kontrastforsterkning", setup=lambda x: x.destroy_information(2))

results_doc.save("rapport_snippets/output/contrast/results.tex")


