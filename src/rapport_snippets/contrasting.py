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

def intensity(path):
	import matplotlib.pyplot as plt
#	plt.savefig(path + "intensity.png")
#	plt.show(block=False)
	contrast_obj.alpha = 0.2

	contrast_obj.save(path + "orginal.png")


	plt.plot(local_adaptive_histogram.intensity(process(contrast_obj.data.copy())), color="r")
#	plt.savefig(path + "test_poission_before.png")
	contrast_obj.fit(2)
#	plt.cla()
	plt.plot(local_adaptive_histogram.intensity(process(contrast_obj.data.copy())), color="g")
	plt.savefig(path + "poisson.png")

	contrast_obj.save(path + "poisson_output.png")

	contrast_obj.reset()

	plt.cla()
	plt.plot(local_adaptive_histogram.intensity(process(contrast_obj.data.copy())), color="r")
	lah = np.cumsum(local_adaptive_histogram.intensity(process(contrast_obj.data.copy())))
	plt.plot(lah, color="g")
	plt.savefig(path + "intensity_adaptive.png")

	output_file = (local_adaptive_histogram.contrast_enhancement(process(contrast_obj.data.copy())))
	im = Image.fromarray(np.uint8(output_file*255))
	im.save(path + "lah_output.png")

	exit(0)
#	exit(0)

#intensity()

def compile(output_path="./rapport_snippets/output/"):
	if not os.path.isdir(output_path):
		os.mkdir(output_path)
	intensity(output_path)
	results_doc = compile_doc(contrast_obj, epoch_count, output_path, "kontrastforsterkning")#, setup=lambda x: x.destroy_information(2))
	results_doc.save("{}/results.tex".format(output_path))

