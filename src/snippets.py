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
from rapport_snippets import blur
from rapport_snippets import hdr
import os

if __name__ == "__main__":
	location = os.path.dirname(os.path.abspath(__file__))
	location += "/" if not location.endswith("/") else ""
	location += "../rapport/paper/"

	#blur.compile(location + "/glatting/")
	#contrasting.compile(location + "/kontrastforsterkning/contrast/")
	#matting.compile(location + "/sømløs kloning/")
	#inpaiting.compile(location + "/inpainting/")
	#anonymizing.compile(location + "/anonymisering/")
	
	#demosaic.compile(location + "/demosaicing/")
	hdr.compile(location + "/hdr/res/")

	#non_edge_blurring.compile(location + "/glatting/")
	#grayscale.compile(location + "/farge_gråtone/")
