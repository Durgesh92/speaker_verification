import sys

max_ = float(0.0)
line = None
spk = None
score = None
with open(sys.argv[1],"r") as f1:
	for line in f1:
		ls = line.strip().split(" ")
		if float(ls[2]) > max_ :
			max_ = float(ls[2])
			#print(max_,line)
			line = line
			spk = ls[0]
			score = ls[2]
print("Identified as  : ",spk," score :",score)
