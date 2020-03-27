from experimental import implicit


x = implicit.blur("./files/test_images/lena.png")
x.fit(4)
x.show()