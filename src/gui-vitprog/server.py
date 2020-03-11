from flask import Flask, request, send_from_directory, flash
import os
from werkzeug.utils import secure_filename
from flask import render_template
from flask import request
import os
import sys
sys.path.append("../")
#from blurring import *
import blurring

print(os.path.abspath('./html/'))
app = Flask(__name__, static_url_path="",template_folder="html")

@app.route('/')
def root():
	return send_from_directory(os.path.abspath('./html/'), "index.html")

# 'GET', 
@app.route('/blur', methods=['POST'])
def blur():
	import base64
	if(request.form.get('image_info') != None):
		print(request.form.get('image_info'))
		path = os.path.abspath(request.form.get('image_info'))
		response = blurring.blur(path).fit(1).save(path.replace(".png", "_.png"))
		print(response)
		return request.form.get('image_info').replace(".png", "_.png")

	return "bad_return"

@app.route('/noise', methods=['POST'])
def blur():
	import base64
	if(request.form.get('image_info') != None):
		print(request.form.get('image_info'))
		path = os.path.abspath(request.form.get('image_info'))
		response = blurring.blur(path).fit(1).save(path.replace(".png", "_.png"))
		print(response)
		return request.form.get('image_info').replace(".png", "_.png")

	return "bad_return"

@app.route('/imageview')
def imageview():
	filename = "Skjermbilde_2020-02-17_kl._10.31.46.png"
	return render_template("imageview.html", path='./uploads/' + filename)


@app.route('/uploads/<path:filename>', methods=['GET', 'POST'])
def download(filename):
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
		filename = secure_filename(file.filename)
		file.save(os.path.join(os.path.abspath('./uploads/'), filename))
		return render_template("imageview.html", path='./uploads/' + filename)
	else:
		return "<h1>no. post only </h1>"

if __name__ == "__main__":
	app.run()

