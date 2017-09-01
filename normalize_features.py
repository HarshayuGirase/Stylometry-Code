import sys,os
import string
import numpy as np
path='all/'
def normalize_features():
	fin=open(path+'combined_stylometry_feature_sample.csv','r')
	aid_feature={}
	aid_feature_values={}
	feature_length=0
	for l in fin:
		split_str=l.rstrip('\n').split(',',1)
		if split_str[0]=='aid': continue
		aid_feature[split_str[0]]=split_str[1]
		aid_feature_values[split_str[0]]=[]
		for v in split_str[1].split(','):
			aid_feature_values[split_str[0]].append(float(v))
		if feature_length==0:
			feature_length=len(split_str[1].split(','))
	fin.close()
	aver_values=[0.0 for i in range(feature_length)]
	nozero_count=[0.0 for i in range(feature_length)]
	for aid in aid_feature_values:
		values=aid_feature_values[aid]
		for i in range(len(values)):
			aver_values[i]+=values[i]
			if values[i]>0:
				nozero_count[i]+=1
	for i in range(len(aver_values)):
		if nozero_count[i]>0:
			aver_values[i]=aver_values[i]/nozero_count[i]
	for aid in aid_feature_values:
		for i in range(len(values)):
			if aver_values[i]>0:
				aid_feature_values[aid][i]=aid_feature_values[aid][i]/aver_values[i]
	for aid in aid_feature_values:
		values=aid_feature_values[aid]
		n=np.linalg.norm(values)
		aid_feature_values[aid]=values/n
	return aid_feature_values

def write_normalize_file():
	aid_feature_values=normalize_features()
	fout=open(path+'stylometry_feature_normalize_sample.csv','w')
	for aid in aid_feature_values:
		fout.write(aid)
		for v in aid_feature_values[aid]:
			fout.write(','+str(v))
		fout.write('\n')
	fout.close()

def main():
	write_normalize_file()

if __name__ == '__main__':
	main()