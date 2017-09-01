import sys,os
import string
import numpy as np
from scipy.spatial import distance
import datetime
import random
path='all/'

def get_author_map():
	old_new_names={}
	fin=open('../recrawl_SA/author_name_check.txt','r')
	for l in fin:
		if l.startswith('1'):
			split_str=l.rstrip('\n').split()
			old_new_names[split_str[1]]=split_str[2]
	fin.close()
	return old_new_names

def get_aid_info():
# aid---author,
# aid---stocks,
	aid_author={}
	aid_stocks={}
	aid_time={}
	old_new_names=get_author_map()
	fin=open('/cs/avenger/bolunwang/SeekingAlpha/ParseArticles/info_final.txt','r')
	for l in fin:
		split_str=l.rstrip('\n').split('\t')
		article_id=split_str[0]
		timestamps=datetime.datetime.strptime(split_str[2],'%b %d %Y, %H:%M')
		#timestamps=(timestamps-datetime.datetime(2000,1,1,0,0,0)).days
		author_url=split_str[6]
		if author_url in old_new_names:
			author_url=old_new_names[author_url]
		article_url=split_str[7]
		about_stocks=split_str[8].lower().strip('@').split('@')
		include_stocks=split_str[9].lower().strip('@').split('@')
		aid_author[article_id]=author_url
		aid_stocks[article_id]=about_stocks
		aid_time[article_id]=timestamps
	fin.close()
	fin=open('/cs/avenger/bolunwang/SeekingAlpha/merge_article/article_info.txt','r')
	for l in fin:
		if l.startswith('#'): continue
		split_str=l.rstrip('\n').split('\t')
		article_id=split_str[0]
		timestamps=datetime.datetime.strptime(split_str[2],'%b %d %Y, %H:%M')
		#timestamps=(timestamps-datetime.datetime(2000,1,1,0,0,0)).days
		author_url=split_str[6]
		if author_url in old_new_names:
			author_url=old_new_names[author_url]
		article_url=split_str[7]
		about_stocks=split_str[8].lower().strip('@').split('@')
		include_stocks=split_str[9].lower().strip('@').split('@')
		aid_author[article_id]=author_url
		aid_stocks[article_id]=about_stocks
		aid_time[article_id]=timestamps
	fin.close()
	#return aid_author,aid_stocks,aid_time
	return aid_author,aid_time
def get_author_articles(author):
	all_aids=[]
	aids=[]
	fin=open('/cs/avenger/bolunwang/SeekingAlpha/ParseArticles/info_final.txt','r')
	for l in fin:
		split_str=l.rstrip('\n').split('\t')
		article_id=split_str[0]
		author_url=split_str[6]
		if author==author_url:
			aids.append(article_id)
		all_aids.append(article_id)
	fin.close()
	fin=open('/cs/avenger/bolunwang/SeekingAlpha/merge_article/article_info.txt','r')
	for l in fin:
		if l.startswith('#'): continue
		split_str=l.rstrip('\n').split('\t')
		article_id=split_str[0]
		author_url=split_str[6]
		if author==author_url:
			aids.append(article_id)
		all_aids.append(article_id)
	fin.close()
	return all_aids,aids

#method1: normalize to 0-1 space
#method2: normalize to same mean and std

def get_author_article_count():
	all_aids=[]
	author_aids={}
	old_new_names=get_author_map()
	fin=open('/cs/avenger/bolunwang/SeekingAlpha/ParseArticles/info_final.txt','r')
	for l in fin:
		split_str=l.rstrip('\n').split('\t')
		article_id=split_str[0]
		author_url=split_str[6]
		if author_url in old_new_names:
			author_url=old_new_names[author_url]
		all_aids.append(article_id)
		try:
			author_aids[author_url].append(article_id)
		except KeyError:
			author_aids[author_url]=[]
			author_aids[author_url].append(article_id)
	fin.close()
	fin=open('/cs/avenger/bolunwang/SeekingAlpha/merge_article/article_info.txt','r')
	for l in fin:
		if l.startswith('#'): continue
		split_str=l.rstrip('\n').split('\t')
		article_id=split_str[0]
		author_url=split_str[6]
		if author_url in old_new_names:
			author_url=old_new_names[author_url]
		all_aids.append(article_id)
		try:
			author_aids[author_url].append(article_id)
		except KeyError:
			author_aids[author_url]=[]
			author_aids[author_url].append(article_id)
	fin.close()
	author_acnt={}
	for author in author_aids:
		author_acnt[author]=len(set(author_aids[author]))
	return author_acnt,author_aids,all_aids


def get_aid_normalize():
	#pro_feature=open('pro_stylometry_features.txt','r').readline()
	#pro_feature=pro_feature.rstrip('\n')
	fin=open(path+'stylometry_feature_normalize_sample.csv','r')
	aid_feature_normalize={}
	aid_feature_values={}
	feature_length=0
	for l in fin:
		split_str=l.rstrip('\n').split(',',1)
		if split_str[0]=='aid': continue
		#if pro_feature==split_str[1]: continue
		aid_feature_normalize[split_str[0]]=split_str[1]
		aid_feature_values[split_str[0]]=[]
		if feature_length==0:
			feature_length=len(split_str[1].split(','))
		#for v in split_str[1].split(','):
		#	aid_feature_values[split_str[0]].append(float(v))
	fin.close()
	return aid_feature_normalize,aid_feature_values,feature_length

def generate_training_testing_file(author,author_aids,aid_feature_normalize,feature_length):
	fout=open(path+'training_testing/'+author+'_training.csv','w')
	fout.write('aid,')
	for i in range(feature_length):
		fout.write('F'+str(i)+',')
	fout.write('label\n')
	aids1=list(set(author_aids[author])&set(aid_feature_normalize))
	aids2=list(set(aid_feature_normalize)-set(aids1))
	random.shuffle(aids1)
	random.shuffle(aids2)
	if len(aids1)>500:
		aids1=aids1[:500]
	for aid in aids1:
		fout.write(aid+','+aid_feature_normalize[aid]+','+'True'+'\n')
	for aid in aids2[:len(aids1)*5]:
		fout.write(aid+','+aid_feature_normalize[aid]+','+'False'+'\n')
	fout.close()
	return

def main():
	key_feature_normalize,key_feature_values,feature_length=get_aid_normalize()
	#aid_author,aid_time=get_aid_info()
	
	aid_author={}
	fin=open(path+'author_aid_map.txt','r')
	for l in fin:
		author=l.rstrip('\n').split('\t')[0]
		aid=l.rstrip('\n').split('\t')[1]
		aid_author[aid]=author
	fin.close()
	
	author_keys={}
	for key in key_feature_normalize:
		aid=key.split('_')[0]
		author=aid_author[aid]
		try:
			author_keys[author].add(key)
		except KeyError:
			author_keys[author]=set()
			author_keys[author].add(key)
	fout=open(path+'author_keys.txt','w')
	'''
	authors=author_keys.keys()
	random.shuffle(authors)
	for author in authors[:50]:
		keys=list(author_keys[author])
		random.shuffle(keys)
		idx=random.randint(1,10)
		author_keys[author]=set(keys[:idx+1])
	'''
	for author in author_keys:
		for key in author_keys[author]:
			fout.write(author+'\t'+key+'\n')
	fout.close()
	fout=open(path+'training_testing/'+'all_testing.csv','w')
	fout2=open(path+'training_testing/'+'testing_keys.txt','w')
	fout.write('aid,')
	for i in range(feature_length):
		fout.write('F'+str(i)+',')
	fout.write('label\n')
	for author in author_keys:
		keys=author_keys[author]
		for key in keys:
			fout.write(key+','+key_feature_normalize[key]+','+'True'+'\n')
			fout2.write(key+'\n')
	fout.write(key+','+key_feature_normalize[key]+','+'False'+'\n')
	fout2.write(key+'\n')
	fout.close()
	fout2.close()
	for author in author_keys:
		if author=='http://seekingalpha.com/srch': continue
		generate_training_testing_file(author,author_keys,key_feature_normalize,feature_length)

if __name__ == '__main__':
	main()