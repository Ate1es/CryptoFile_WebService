import os
from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
import errno
import enc
from flask import send_file

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/encrypt')
def index2():
	return render_template('encfile.html')

@app.route('/decrypt')
def index3():
	return render_template('decfile.html')

@app.route('/fileupload', methods=['POST'])
def file_upload():
	file=request.files['file']
	pw=request.form['pw']
	passward=enc.getKey(pw)
	filename = secure_filename(file.filename)
	try:
		os.makedirs('./upload/file')
	except OSError, e:
		if e.errno != errno.EEXIST:
			raise
		pass
	file.save(os.path.join('./upload/file', filename))
	enc.encrypt(passward,'./upload/file/'+file.filename)
	return render_template('down.html')

@app.route('/downfile', methods=['POST'])
def downfile():
	filename=request.form['filename']
	os.remove('./upload/file/'+filename)
	return send_file('./upload/file/'+filename+'.enc', mimetype='text/txt',as_attachment=True)

@app.route('/decryptfile', methods=['POST'])
def decrypt_file():
	pw=request.form['pw']
	passward=enc.getKey(pw)
	filename=request.form['filename']
	enc.decrypt(passward,'./upload/file/'+filename+'.enc')
	return send_file('./upload/file/'+filename+'.enc.dec', mimetype='text/txt', attachment_filename=filename, as_attachment=True)

if __name__=='__main__':
    app.run(debug=True, host='0.0.0.0')
