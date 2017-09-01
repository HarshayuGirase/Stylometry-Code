'''
combine stylometry features.
normalize
'''
import sys,os
import string
path='all/'
def get_feature2(keys,key_values):
	key_value_pairs={}
	for key in keys:
		key_value_pairs[key]=0
	for tmp_key_value in key_values:
		tmp_key=tmp_key_value.split(': ')[0].strip('\'')
		if tmp_key=='': continue
		tmp_value=int(tmp_key_value.split(': ')[1])
		key_value_pairs[tmp_key]=tmp_value
	feature2=''
	for key in keys:
		feature2+=','+str(key_value_pairs[key])
	return feature2	

def main():
	aid_feature1={}
	aid_feature2={}
	fin=open(path+'stylometry_feature_sample.csv','r')
	for l in fin:
		split_str=l.rstrip('\n').split(',',1)
		aid=split_str[0]
		feature1=split_str[1]
		aid_feature1[aid]=feature1
	fin.close()
	keys=set()
	fin=open('syntactic_keys.txt','r')
	for l in fin:
		keys.add(l.rstrip('\n'))
	fin.close()
	servers=['antman','blackwidow','captainamerica','drstrange','hawkeye','namor','quicksilver','ultron']
	servers+=['colossus','jeanerey','beast','gambit','nightcrawler','bishop','havok','marrow']
	filenames=os.listdir(path+'syntactic_features/')
	for s in servers:
		for idx in range(8):
			if 'syntactic_feature_sample_'+s+str(idx)+'.csv' not in filenames: continue
			fin=open(path+'syntactic_features/syntactic_feature_sample_'+s+str(idx)+'.csv','r')
			for l in fin:
				split_str=l.rstrip('\n').split(',',1)
				aid=split_str[0]
				key_values=split_str[1].strip('{}').split(', ')
				feature2=get_feature2(keys,key_values)
				aid_feature2[aid]=feature2
			fin.close()
	fout=open(path+'combined_stylometry_feature_sample.csv','w')
	for aid in set(aid_feature1)&set(aid_feature2):
		fout.write(aid+','+aid_feature1[aid]+aid_feature2[aid]+'\n')
	fout.close()

if __name__ == '__main__':
	main()
