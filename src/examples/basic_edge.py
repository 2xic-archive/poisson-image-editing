import sys
sys.path.append('./')

from backend import non_edge_blurring

x = non_edge_blurring.non_edge_blur("./files/test_images/lena.png")#, True)
x.set_mode("Explicit")

x.fit(epochs=30)
x.show()
