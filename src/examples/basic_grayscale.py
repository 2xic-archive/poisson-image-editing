import sys
sys.path.append('./')

from backend import grayscale

x = grayscale.grayscale("./files/test_images/lena.png", True)
x.set_mode("Explicit")

x.fit(epochs=100)
x.show()
