from flask import Flask, request, send_from_directory, flash
import os
from werkzeug.utils import secure_filename
from flask import render_template
from flask import request

#print('__file__={0:<35} | __name__={1:<20} | __package__={2:<20}'.format(__file__,__name__,str(__package__)))

import os
import sys
sys.path.append("../")
#from blurring import *
import blurring

# set the project root directory as the static folder, you can set others.
print(os.path.abspath('./html/'))
app = Flask(__name__, static_url_path="",template_folder="html")#os.path.abspath('./html/'))

@app.route('/')
def root():
	print("hei")
	return send_from_directory(os.path.abspath('./html/'), "index.html")

# 'GET', 
@app.route('/blur', methods=['POST'])
def blur():
	import base64
	if(request.form.get('bagel') != None):
		print(request.form.get('bagel'))
		username = os.path.abspath(request.form.get('bagel'))
		response = blurring.blur(username).fit(1).save(username.replace(".png", "_.png"))
		print(response)
		return request.form.get('bagel').replace(".png", "_.png")

	return "Bagel";

@app.route('/imageview')
def imageview():
#	print("hei")
#	return send_from_directory(os.path.abspath('./html/'), "index.html")
#	return send_from_directory(directory="./uploads", filename="Skjermbilde_2020-02-17_kl._10.31.46.png")
	filename = "Skjermbilde_2020-02-17_kl._10.31.46.png"
	return render_template("imageview.html", path='./uploads/' + filename)


@app.route('/uploads/<path:filename>', methods=['GET', 'POST'])
def download(filename):
	#uploads = os.path.join(current_app.root_path, app.config['UPLOAD_FOLDER'])
	print(filename)
	return send_from_directory(directory="./uploads", filename=filename)


@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
	if request.method == 'POST':
		print(request.files)
		if 'file' not in request.files:
			flash('No file part')
			return redirect(request.url)
		file = request.files['file']
	#	if file and allowed_file(file.filename):
		filename = secure_filename(file.filename)
		file.save(os.path.join(os.path.abspath('./uploads/'), filename))
		return render_template("imageview.html", path='./uploads/' + filename)
	else:
		return "<h1>no. post only </h1>"

if __name__ == "__main__":
	app.run()

