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

def process(img):
	if len(img.shape) == 2:
		img = img.reshape(img.shape + (1,))
	if np.max(img) <= 1:
		img *= 255
		img = img.astype(np.uint8)
	else:
		img = img.astype(np.uint8)
	return img 

def intensity():
	import matplotlib.pyplot as plt
	plt.plot(local_adaptive_histogram.intensity(process(contrast_obj.data.copy())))
	plt.savefig("rapport_snippets/output/contrast/intensity.png")
#	plt.show(block=False)
	contrast_obj.alpha = 0.05
	contrast_obj.fit(1)
	plt.cla()
	plt.plot(local_adaptive_histogram.intensity(process(contrast_obj.data.copy())))
	plt.savefig("rapport_snippets/output/contrast/intensity_13.png")

	plt.cla()
	lah = local_adaptive_histogram.contrast_enhancement(process(contrast_obj.data.copy()))
	plt.plot(local_adaptive_histogram.intensity(process(lah)))
	plt.savefig("rapport_snippets/output/contrast/intensity_adaptive.png")
	exit(0)


intensity()

results_doc = compile_doc(contrast_obj, epoch_count, "./rapport_snippets/output/contrast/", "kontrastforsterkning", setup=lambda x: x.destroy_information(2))

results_doc.save("rapport_snippets/output/contrast/results.tex")


