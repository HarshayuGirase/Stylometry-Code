import sys,os
import string
import networkx as nx
import community
import datetime
import numpy as np
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

def get_author_articles():
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
	return author_aids

def get_comment_pairs(aid_author):
	filename1='/cs/avenger/tianyi/SeekingAlpha/comments/data/comment_meta.txt'
	filename2='/cs/avenger/bolunwang/SeekingAlpha/comments/comment_meta_for_tianyi.txt'
	filenames=[filename1,filename2]
	old_new_names=get_author_map()
	author_commenter={}
	author_comm_cnt={}
	for f in filenames:
		fin=open(f,'r')
		for l in fin:
			split_str=l.rstrip('\n').split('\t')
			aid=split_str[0]
			if aid not in aid_author: continue
			author=aid_author[aid]
			commenter=split_str[5]
			if not author in author_comm_cnt:
				author_comm_cnt[author]=0
			author_comm_cnt[author]+=1
			if commenter.startswith('/user'): continue
			if commenter.startswith('/author'):
				commenter=commenter.split('/')[-1]
			if commenter in old_new_names:
				commenter=old_new_names[commenter]
			if not author in author_commenter:
				author_commenter[author]=set()
			author_commenter[author].add(commenter)
		fin.close()
	return author_commenter,author_comm_cnt

def stock_interval(sid_timelist1,sid_timelist2):
	min_v=100000
	for sid in set(sid_timelist1)&set(sid_timelist2):
		timelist1=sid_timelist1[sid]
		timelist2=sid_timelist2[sid]
		for t1 in timelist1:
			for t2 in timelist2:
				min_v=min(abs((t2-t1).days),min_v)
	return min_v

def main():
	aid_author,aid_stocks,aid_time=get_aid_info()
	author_commenter,author_comm_cnt=get_comment_pairs(aid_author)
	author_aids=get_author_articles()
	author_stocks={}
	author_times={}
	author_all_count={}
	author_sid_timelist={}
	fin=open(path+'author_keys.txt','r')
	for l in fin:
		author=l.rstrip('\n').split('\t')[0]
		#authors.append(author)
		aid=l.rstrip('\n').split('\t')[1]
		#aid_author[aid]=author
		try:
			author_all_count[author]+=1.0
		except KeyError:
			author_all_count[author]=1.0
	fin.close()

	for author in author_aids:
		aids=author_aids[author]
		#author_stocks[author]=set()
		tmp_stocklist=[]
		tmp_timelist=[]
		sid_timelist={}
		for aid in aids:
			tmp_stocklist+=aid_stocks[aid]
			tmp_timelist.append(aid_time[aid])
			for sid in aid_stocks[aid]:
				try:
					sid_timelist[sid].append(aid_time[aid])
				except:
					sid_timelist[sid]=[]
					sid_timelist[sid].append(aid_time[aid])
		author_stocks[author]=set(tmp_stocklist)
		author_times[author]=set(tmp_timelist)
		author_sid_timelist[author]=sid_timelist
	author_idx={}
	idx_authors={}
	fin=open(path+'similar_author_cluster_idx_50_14_1_clique.txt','r')
	for l in fin:
		split_str=l.rstrip('\n').split('\t')
		author_idx[split_str[1]]=int(split_str[0])
		try:
			idx_authors[int(split_str[0])].append(split_str[1])
		except KeyError:
			idx_authors[int(split_str[0])]=[]
			idx_authors[int(split_str[0])].append(split_str[1])
	fin.close()
	for idx in idx_authors:
		authors=idx_authors[idx]
		tstart=[]
		tend=[]
		for author in authors:
			tstart.append(min(author_times[author]))
		print idx, sorted(tstart)




if __name__ == '__main__':
	main()