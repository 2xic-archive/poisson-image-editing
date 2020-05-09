"""
snippts.py
====================================
Makes all the figures and tables(?) for the report
"""
#import rapport_snippets
from rapport_snippets import contrasting
from rapport_snippets import inpaiting
from rapport_snippets import matting
from rapport_snippets import anonymizing
from rapport_snippets import demosaic
from rapport_snippets import non_edge_blurring
from rapport_snippets import grayscale
from rapport_snippets import blur_attachment
from rapport_snippets import blur
from rapport_snippets import hdr
from rapport_snippets import laplacian
from rapport_snippets import blur_vs_blur
import os
from engine import image_handler

if __name__ == "__main__":
	location = os.path.dirname(os.path.abspath(__file__))
	location += "/" if not location.endswith("/") else ""
	location += "../rapport/paper/"

	#anonymizing.compile(location + "/anonymisering/resultat/")
	
	"""
	blur.compile(location + "/glatting/blur/")
	blur.test_blur_filter(location + "/glatting/gaussian/")
	blur_attachment.compile(location + "/glatting/attachment/")
	blur_vs_blur.compile_non_edge_blur(location + "/glatting/glatting_vs_glatting/")
	"""

	#contrasting.compile(location + "/kontrastforsterkning/contrast/")
	#contrasting.compile_color(location + "/kontrastforsterkning/contrast_color/")
	
	#demosaic.compile(location + "/demosaicing/demosaic/")

	#grayscale.compile(location + "/farge_gråtone/grayscale/")
	#grayscale.compule_side_by_side(location + "/farge_gråtone/grayscale_side/")

	#matting.compile(location + "/sømløs kloning/matting/")
	#matting.compile_noisy(location + "/sømløs kloning/matting_noise/")
	#matting.compile_parameters(location + "/sømløs kloning/parametere/")
	#matting.compile_moapple(location + "/sømløs kloning/oraple/")

	#laplacian.compile_parameters(location + "/img/")

	#inpaiting.compile(location + "/inpainting/res/")
	#inpaiting.compile_zoom(location + "inpainting/extra/")
	inpaiting.compile_median(location + "inpainting/median/")
	
	"""
	hdr.compile(location + "/hdr/res/", images = [
		image_handler.ImageHandler('../hdr-bilder/Adjuster/Adjuster_00064.png'),
		image_handler.ImageHandler('../hdr-bilder/Adjuster/Adjuster_00128.png'),
		image_handler.ImageHandler('../hdr-bilder/Adjuster/Adjuster_00256.png'),
		image_handler.ImageHandler('../hdr-bilder/Adjuster/Adjuster_00512.png')
	])

	hdr.compile(location + "/hdr/res2/", images = [
		image_handler.ImageHandler('../hdr-bilder/Ocean/Ocean_00064.png'),
		image_handler.ImageHandler('../hdr-bilder/Ocean/Ocean_00128.png'),
		image_handler.ImageHandler('../hdr-bilder/Ocean/Ocean_00256.png'),
		image_handler.ImageHandler('../hdr-bilder/Ocean/Ocean_00512.png')
	], latex_name="res2")
	"""
	#non_edge_blurring.compile(location + "/glatting/non_edge_blur/")
