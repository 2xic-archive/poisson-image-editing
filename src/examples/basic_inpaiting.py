import sys
sys.path.append('./')

from backend import inpaiting

x = inpaiting.inpaint("./files/test_images/lena.png")#, True)
x.set_mode("Explicit")
x.destroy_information()

x.show()
x.fit(epochs=10)
x.show()

x.fit(epochs=10)
x.show()
