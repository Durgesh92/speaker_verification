import os
import subprocess
import json

# Create a directory in a known location to save files to.

def add_new_speaker(audio,id,name):
	print("----------------- Creating Signature for "+id+" - "+name+" ----------------------------")
	#process = subprocess.Popen(['bash','decode.sh',audio], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	#out, err = process.communicate()
	#print(out)
	#print("err : ",err)
	#with open("exp/xvector_nnet_1a/train_global_mean.ark","r") as f1:
	with open("test/test_global_mean.ark","r") as f1:
		for line in f1:
			ls = line.strip().split(" ")
			f1 = True
			spk_id = ""
			spk_vector = []
			data = ""
			for x in ls:
				if x.strip() == '':
					continue
				if f1:
					spk_id = x
					f1 = False
					continue
				else:
					data = data +" "+ x.strip()
			data = id + "  " + data
	if len(data.split(" ")) == 205:
		op1 = open("exp/xvector_nnet_1a/train_global_mean.ark","a")
		op1.write(data+"\n")
		op2 = open("id_name.txt","a")
		op2.write(id+","+name+"\n")
		print("Added")
		return True
	else:
		return False
	

#add_new_speaker("test_audios/nakano.wav","86b45","nakano")
