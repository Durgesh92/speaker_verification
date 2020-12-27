import sys
import wave
import json
import os
import numpy as np

def load_():
	dict1 = {}
	with open("exp/xvector_nnet_1a/train_global_mean.ark","r") as f1:
		for line in f1:
			ls = line.strip().split(" ")
			f1 = True
			spk_id = ""
			spk_vector = []
			for x in ls:
				if x.strip() == '':
					continue
				if f1:
					spk_id = x
					f1 = False
					continue
				if "[" not in x and "]" not in x:
					spk_vector.append(float(x.strip()))
			dict1[spk_id] = spk_vector
	return dict1

def estimate_speaker_similarity(sig):
	dict1 = load_()
	with open(sig,"r") as f1:
		for line in f1:
			ls = line.strip().split(" ")
			f1 = True
			spk_id = ""
			spk_vector = []
			for x in ls:
				if x.strip() == '':
					continue
				if f1:
					spk_id = x
					f1 = False
					continue
				if "[" not in x and "]" not in x:
					spk_vector.append(float(x.strip()))
	sig = spk_vector
	similarity_dict = {}
	for x in dict1:
		nx = np.array(dict1[x])
		ny = np.array(sig)
		dist = 1 - np.dot(nx, ny) / np.linalg.norm(nx) / np.linalg.norm(ny)
		similarity_dict[x] = dist
	return similarity_dict

def load_id_names(spk_id):
	dict2 = {}
	with open("person_identification.csv","r") as f1:
		for line in f1:
			ls = line.strip().split(",")
			dict2[ls[2]] = ls[3]
	return dict2[spk_id]

def get_lowest_match(scores):
	l = 0
	spk_id = ""
	f1 = True
	for x in scores:
		if f1:
			spk_id = x
			l = scores[x]
			f1 = False
			continue
		if scores[x] < l:
			l = scores[x]
			spk_id = x
	return spk_id,l,load_id_names(spk_id)

#print(get_lowest_match(estimate_speaker_similarity(sys.argv[1])))
