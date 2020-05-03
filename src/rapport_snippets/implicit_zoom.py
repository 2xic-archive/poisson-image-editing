from PIL import Image
import sys
sys.path.append("./")
from backend import inpaiting
from extra import local_adaptive_histogram
from PIL import Image
from rapport_snippets.figs import *
import numpy as np
from figs import *

def zoom_at(img, x, y, zoom):
	w, h = img.size
	zoom2 = zoom * 2
	img = img.crop((x - w / zoom2, y - h / zoom2, 
                    x + w / zoom2, y + h / zoom2))
	return img.resize((w, h), Image.LANCZOS).convert('RGB')

location = os.path.dirname(os.path.abspath(__file__))
location += "/" if not location.endswith("/") else ""
location += "../../rapport/paper/"
location += "inpainting/extra/"

contrast_obj = inpaiting.inpaint("./files/test_images/lena.png", True)
#input_image = contrast_obj.destroy_information()#.copy()

mask = np.ones((contrast_obj.data.shape[:2]))

x_m, y_m, _ = contrast_obj.data.shape

SIZE = 5

mask[x_m//2: x_m//2 + SIZE, 
	 y_m//2: y_m//2 + SIZE] = 0


og = np.zeros((contrast_obj.data.shape))
for i in range(contrast_obj.data.shape[-1]):
	og[:, :, i] = contrast_obj.data[:, :, i] * mask


contrast_obj.data = og

IN = Image.fromarray(np.uint8(og * 255))
out_mask= zoom_at(IN,
	x_m // 2, y_m // 2, 5)#.show()

contrast_obj.fit(
	og,
	og,
	mask,
	epochs=10
)

IN = Image.fromarray(np.uint8(contrast_obj.data * 255))
out_fixed = zoom_at(IN,
	x_m // 2, y_m // 2, 5)#.show()

IN = Image.fromarray(np.uint8(contrast_obj.data_copy * 255))
out_original = zoom_at(IN,
	x_m // 2, y_m // 2, 5)#.show()

out_mask.save(location + "mask.png")
out_fixed.save(location + "fixed.png")
out_original.save(location + "original.png")

Image.fromarray(np.uint8(contrast_obj.data * 255)).save(location + "full.png")

x = doc()
x.add_row_element(subfigure(path="./inpainting/extra/mask.png", text="Bilde med glitch"))
x.add_row_element(subfigure(path="./inpainting/extra/fixed.png", text="Bilde med 10 iterations"))
x.add_row_element(subfigure(path="./inpainting/extra/original.png", text="original bilde"))
x.add_row()
x.add_row_element(subfigure(path="./inpainting/extra/full.png", text="Fulle bilde med 10 iterations"))
x.add_row()
x.save(location + "results.tex")


"""
IN = Image.open("/Users/2xic/Desktop/NTNU/Andre semester/Fag/vitenskapelig programmering/imt3881-2020-prosjekt/rapport/paper/inpainting/inpainting_color_explicit/lena.png")
zoom_at(IN,
	IN.size[0]//2, IN.size[0]//2, 4).show()
"""