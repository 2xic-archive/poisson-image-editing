"""
snippts.py
====================================
Makes all the figures and tables(?) for the report
"""
import glob
import os

from engine import image_handler
from rapport_snippets import inpaiting
from rapport_snippets import blur
from rapport_snippets import anonymizing
from rapport_snippets import blur_attachment
from rapport_snippets import demosaic
from rapport_snippets import matting
from rapport_snippets import non_edge_blurring
from rapport_snippets import blur_vs_blur
from rapport_snippets import contrasting
from rapport_snippets import grayscale

if __name__ == "__main__":
    location = os.path.dirname(os.path.abspath(__file__))
    location += "/" if not location.endswith("/") else ""
    location += "../rapport/paper/"

    anonymizing.compile(location + "/anonymisering/resultat/")
    #anonymizing.compile_faces(location + "/anonymisering/")
    #blur.compile(location + "/glatting/blur/")
    #blur_attachment.compile(location + "/glatting/attachment/")
    # blur.test_blur_filter(location + "/glatting/gaussian/")
    """
    blur_vs_blur.compile_NonEdgeBlur(location + "/glatting/glatting_vs_glatting/")
    """

    #inpaiting.compile(location + "/inpainting/")
    # inpaiting.compile_zoom(location + "inpainting/extra/")
    # inpaiting.compile_zoom(location + "inpainting/extra/", SIZE=10)
    # inpaiting.compile_median(location + "inpainting/median/")

    #contrasting.compile(location + "/kontrastforsterkning/contrast/")
    #contrasting.compile_color(location + "/kontrastforsterkning/contrast_color/")

#    demosaic.compile(location + "/demosaicing/demosaic/")
    #demosaic.compile_zoom(location + "/demosaicing/demosaic_zoom/")

    grayscale.compile(location + "/farge_gråtone/grayscale/")
   # grayscale.compule_side_by_side(location + "/farge_gråtone/grayscale_side/")

    #non_edge_blurring.compile(location + "/glatting/non_edge_blur/")

    #matting.compile(location + "/sømløs kloning/")
    #matting.compile_noisy(location + "/sømløs kloning/matting_noise/")
    #matting.compile_parameters(location + "/sømløs kloning/parametere/")
    #matting.compile_oraple(location + "/sømløs kloning/oraple/")
    #matting.compile_applange(location + "/sømløs kloning/applange/")

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
    hdr.plot_function(images = [
        image_handler.ImageHandler('../hdr-bilder/Ocean/Ocean_00064.png'),
        image_handler.ImageHandler('../hdr-bilder/Ocean/Ocean_00128.png'),
        image_handler.ImageHandler('../hdr-bilder/Ocean/Ocean_00256.png'),
        image_handler.ImageHandler('../hdr-bilder/Ocean/Ocean_00512.png')
    ])
    hdr.compile(location + "/hdr/res3/", images=[
        image_handler.ImageHandler(i)
        for i in glob.glob('../hdr-bilder/Ocean/*.png')
    ])
    """