import sys,os
import string
import networkx as nx
import community
import datetime
import numpy as np
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
		#if split_str[3]=='True': continue
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
		if '***' in about_stocks:
			aid_stocks[article_id]=include_stocks
		aid_time[article_id]=timestamps
	fin.close()
	fin=open('/cs/avenger/bolunwang/SeekingAlpha/merge_article/article_info.txt','r')
	for l in fin:
		if l.startswith('#'): continue
		split_str=l.rstrip('\n').split('\t')
		#if split_str[3]=='True': continue
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
		if '***' in about_stocks:
			aid_stocks[article_id]=include_stocks
		aid_time[article_id]=timestamps
	fin.close()
	return aid_author,aid_stocks,aid_time

def main():
	aid_author,aid_stocks,aid_time=get_aid_info()
	author_aids={}
	fin=open('all/slice_aid_text_sample.txt','r')
	fout=open('all/author_aid_map.txt','w')
	for l in fin:
		aid=l.split('\t')[0]
		author=aid_author[aid]
		try:
			author_aids[author].add(aid)
		except KeyError:
			author_aids[author]=set()
			author_aids[author].add(aid)
	fin.close()
	for author in author_aids:
		aids=author_aids[author]
		for aid in aids:
			fout.write(author+'\t'+aid+'\n')
	fout.close()


if __name__ == '__main__':
	main()


