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
from rapport_snippets import blur_attacment
from rapport_snippets import blur
from rapport_snippets import hdr
from rapport_snippets import laplacian
from rapport_snippets import blur_vs_blur
import os

if __name__ == "__main__":
	location = os.path.dirname(os.path.abspath(__file__))
	location += "/" if not location.endswith("/") else ""
	location += "../rapport/paper/"

	#blur.compile(location + "/glatting/")
	
	#contrasting.compile(location + "/kontrastforsterkning/contrast/")
	#contrasting.compile_color(location + "/kontrastforsterkning/contrast_2/")
	
	#blur_vs_blur.compile_non_edge_blur(location + "/glatting/")

	#matting.compile(location + "/sømløs kloning/")
	#matting.compile_noisy(location + "/sømløs kloning/")
	#matting.compile_parameters(location + "/sømløs kloning/")
	#matting.compile_moapple(location + "/sømløs kloning/")

	#laplacian.compile_parameters(location)
	#blur_attacment.compile(location + "/glatting/")

	#inpaiting.compile(location + "/inpainting/")
	#anonymizing.compile(location + "/anonymisering/")
	
	demosaic.compile(location + "/demosaicing/")
	#hdr.compile(location + "/hdr/res/")

	#non_edge_blurring.compile(location + "/glatting/")
	#grayscale.compile(location + "/farge_gråtone/")
	#grayscale.compule_side_by_side(location + "/farge_gråtone/")
