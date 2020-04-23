import sys
sys.path.append('./')

from backend import matting

x = matting.matting()#("./files/test_images/lena.png")#, True)
x.set_mode("Explicit")

x.fit(epochs=10)
x.show()
