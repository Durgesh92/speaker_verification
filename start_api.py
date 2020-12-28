from flask import render_template
from flask import request, redirect, url_for,flash
from werkzeug.utils import secure_filename
import os
from flask import Flask
import subprocess
import json
from compute_cosin import estimate_speaker_similarity,get_lowest_match 
from add_signatures import add_new_speaker
app = Flask(__name__)

# Create a directory in a known location to save files to.
uploads_dir = "/home/vox/durgesh/speaker_verification/uploads"

@app.route('/verify', methods=['GET', 'POST'])
def upload():
	if request.method == 'POST':
		audio = request.files['audio']
		fn = os.path.join(uploads_dir, secure_filename(audio.filename))
		audio.save(fn)
		process = subprocess.Popen(['bash','decode.sh',fn], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
		out, err = process.communicate()
		if os.path.isfile("test/test_global_mean.ark"):
			score_dict = estimate_speaker_similarity("test/test_global_mean.ark")
			spk,score,name = get_lowest_match(score_dict)
			dict1 = {}
			dict1["spekaer_id"] = spk
			dict1["speaker_name"] = name
			dict1["score"] = score
			return json.dumps(dict1)
		else:
			dict1["Error"] = "Something went wrong"
			return json.dumps(dict1)

@app.route('/enroll', methods=['GET', 'POST'])
def add_new():
	if request.method == 'POST':
		audio = request.files['audio']
		fn = os.path.join(uploads_dir, secure_filename(audio.filename))
		audio.save(fn)
		process = subprocess.Popen(['bash','decode.sh',fn], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
		out, err = process.communicate()
		dict1 = {}
		if os.path.isfile("test/test_global_mean.ark"):
			id = request.args.get('id')
			name = request.args.get('name')
			status = add_new_speaker(audio,id,name)
			if status:
				dict1["Message"] = "Successfully added new speaker with "+id+" as id and "+name+" as name"
				return json.dumps(dict1)
			else:
				dict1["Error"] = "Something went wrong while adding speaker signature, either the audio is too short. Please make sure audio length is > 4sec"
				return json.dumps(dict1)
		else:
			dict1["Error"] = "Something went wrong"
			return json.dumps(dict1)

if __name__ == '__main__':
	app.run(host='0.0.0.0', port=7489)
