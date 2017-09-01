import sys,os
import string
import networkx as nx
import community
import datetime
import numpy as np
path='all/'
T=0.5
interval=14
num_sid=1
postname=str(int(T*100))+'_'+str(interval)+'_'+str(num_sid)+'_clique'
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
	G=nx.DiGraph()
	fout=open(path+'author_similarity_by_SVM_filter_'+postname+'.txt','w')
	fin=open(path+'author_similarity_by_SVM_all.txt','r')
	for l in fin:
		split_str=l.rstrip('\n').split('\t')
		author1=split_str[0]
		author2=split_str[1]
		prob=float(split_str[2])
		if author1==author2: continue
		if author1=='' or author1=='***': continue
		if author2=='' or author2=='***': continue
		if prob<=T: continue
		#if author_all_count[author2]<=5: continue
		if len(set(author_stocks[author1])&set(author_stocks[author2]))<num_sid: continue
		#if '***' in author_stocks[author1]: continue
		if '***' in author_stocks[author2]: continue
		if stock_interval(author_sid_timelist[author1],author_sid_timelist[author2])>interval: continue
		#if min(author_times[author1])> max(author_times[author2]) or max(author_times[author1])<min(author_times[author2]):
		#	continue
		G.add_edge(author1,author2)
		if author_all_count[author2]<=10:
			G.add_edge(author2,author1)
		fout.write(l)
	fin.close()
	fout.close()
	G=G.to_undirected(reciprocal=False)
	print len(G.nodes())
	print len(G.edges())
	flog=open(path+'similar_author_info_'+postname+'.txt','w')
	
	node_degree={}
	for n in G.nodes():
		node_degree[n]=G.degree(n)
	sorted_final = [(k,v) for v,k in sorted([(v,k) for k,v in node_degree.items()],reverse=True)]
	#for it in sorted_final:
	#	print it[0],it[1]
	components=nx.connected_components(G)
	communities=components
	#partition = community.best_partition(G)
	#communities=[[] for k in range(len(set(partition.values())))]
	#for n in partition:
	#	communities[partition[n]].append(n)
	all_cliques=[]
	fout=open(path+'similar_author_clique_'+postname+'.txt','w')
	for idx in range(len(communities)):
		nodes=communities[idx]
		subG=nx.Graph()
		for e in G.edges():
			if e[0] in nodes and e[1] in nodes:
				subG.add_edge(e[0],e[1])
		cliques=list(nx.find_cliques(subG))
		max_size=max([len(clique) for clique in cliques])
		for clique in cliques:
			if len(clique)>=min(max_size+10,3):
				all_cliques.append(clique)
				fout.write(str(idx)+'\t'+str(clique)+'\n')
		'''
		max_size2=0
		cliques=set(nx.k_clique_communities(subG,min(max(2,max_size),4)))
		for clique in cliques:
			max_size2=max(len(clique),max_size2)
			fout.write(str(idx)+'\t'+str(clique)+'\n')
		'''
		#idx_info[idx]['max_clique']=max_size
	fout.close()
	
	G=nx.Graph()
	fout=open(path+'similar_author_by_clique_'+postname+'.txt','w')
	for idx in range(len(all_cliques)):
		clique=all_cliques[idx]
		for i in range(len(clique)):
			for k in range(i+1,len(clique)):
				fout.write(clique[i]+'\t'+clique[k]+'\n')
				G.add_edge(clique[i],clique[k])
	fout.close()
	
	flog.write('number of nodes:\t'+str(len(G.nodes()))+'\n')
	flog.write('number of edges:\t'+str(len(G.edges()))+'\n')
	components=nx.connected_components(G)
	communities=components
	flog.write('number of components:\t'+str(len(components))+'\n')
	flog.write('number of communities:\t'+str(len(communities))+'\n')
	#cliques=list(set(nx.k_clique_communities(G,4)))
	#communities=cliques
	idx_info=[]
	for idx in range(len(communities)):
		idx_info.append({})
		idx_info[idx]['length']=len(communities[idx])
	flog.flush()
	fout=open(path+'similar_author_clique_'+postname+'.txt','w')
	for idx in range(len(communities)):
		nodes=communities[idx]
		subG=nx.Graph()
		for e in G.edges():
			if e[0] in nodes and e[1] in nodes:
				subG.add_edge(e[0],e[1])
		cliques=list(nx.find_cliques(subG))
		max_size=max([len(clique) for clique in cliques])
		
		for clique in cliques:
			if len(clique)>=min(max_size+10,3):
				fout.write(str(idx)+'\t'+str(clique)+'\n')
		'''
		max_size2=0
		cliques=set(nx.k_clique_communities(subG,min(max(2,max_size),4)))
		for clique in cliques:
			max_size2=max(len(clique),max_size2)
			fout.write(str(idx)+'\t'+str(clique)+'\n')
		'''
		idx_info[idx]['max_clique']=max_size
	fout.close()

	fout=open(path+'similar_author_cluster_idx_'+postname+'.txt','w')
	for idx in range(len(communities)):
		#print len(c)
		tmp_authors=communities[idx]
		for author in tmp_authors:
			fout.write(str(idx)+'\t'+author+'\n')
			#fout.write(str(idx)+'\t'+author+'\t'+str(node_degree[author])+'\t'+str(author_all_count[author])+'\n')
	fout.close()
	#sys.exit(0)
	fout=open(path+'similar_author_burst_'+postname+'.txt','w')
	for idx in range(len(communities)):
		tmp_authors=communities[idx]
		count_1d=0.0
		count_1w=0.0
		count_2w=0.0
		count_1m=0.0
		count_1a=0.0
		for author in tmp_authors:
			aids=author_aids[author]
			timelist=[]
			for aid in aids:
				timelist.append(aid_time[aid])
			timelist=sorted(timelist)
			intervals=[]
			for k in range(1,len(timelist)):
				intervals.append((timelist[k]-timelist[k-1]).days)
			if len(intervals)>0:
				min_interval=min(intervals)
				aver_interval=np.mean(intervals)
				if min_interval<=1:
					count_1d+=1.0/len(tmp_authors)
				if min_interval<=7:
					count_1w+=1.0/len(tmp_authors)
				if min_interval<=14:
					count_2w+=1.0/len(tmp_authors)
				if min_interval<=30:
					count_1m+=1.0/len(tmp_authors)
			else:
				min_interval=0.0
				aver_interval=0.0
				count_1a+=1.0/len(tmp_authors)
			fout.write(str(idx)+'\t'+author+'\t'+str(min_interval)+'\t'+str(aver_interval)+'\n')
		idx_info[idx]['burst']=[count_1d,count_1w,count_2w,count_1m,count_1a]
	fout.close()
	fout=open(path+'similar_author_stocks_'+postname+'.txt','w')
	for idx in range(len(communities)):
		#print len(c)
		tmp_authors=communities[idx]
		stock_cnt={}
		for author in tmp_authors:
			if author=='***': continue
			sids=author_stocks[author]
			for sid in sids:
				if sid=='***': continue
				try:
					stock_cnt[sid]+=1.0
				except KeyError:
					stock_cnt[sid]=1.0
		sorted_final = [(k,v) for v,k in sorted([(v,k) for k,v in stock_cnt.items()],reverse=True)]
		#print idx, sorted_final[0]
		if len(sorted_final)>0:
			idx_info[idx]['stock']=sorted_final[0][1]
		else:
			idx_info[idx]['stock']=0
		for it in sorted_final:
			s=it[0]
			if s=='***': continue
			fout.write(str(idx)+'\t'+s+'\t'+str(stock_cnt[s])+'\n')
	fout.close()
	
	fout=open(path+'similar_author_comment_'+postname+'.txt','w')
	for idx in range(len(communities)):
		#print len(c)
		comment_cnt=[]
		tmp_authors=communities[idx]
		for author in tmp_authors:
			if author=='***': continue
			if author not in author_comm_cnt:
				author_comm_cnt[author]=0
			fout.write(str(idx)+'\t'+author+'\t'+str(author_comm_cnt[author])+'\n')
			comment_cnt.append(author_comm_cnt[author])
		aver=np.mean(comment_cnt)
		std=np.std(comment_cnt)
		idx_info[idx]['comm']=[aver,std,max(comment_cnt),min(comment_cnt)]
	fout.close()

	stock_cnt=0.0
	burst_cnt=0.0

	for idx in range(len(communities)):
		info=idx_info[idx]
		stock_info=info['stock']
		length_info=info['length']
		if stock_info/length_info >0.5:
			stock_cnt+=1
		burst_info=info['burst']
		if burst_info[-1]<1:
			if burst_info[1]/(1-burst_info[-1])>0.5:
				burst_cnt+=1
	flog.write('shared stock cluster:\t'+str(stock_cnt)+'\n')
	flog.write('half burst author cluster:\t'+str(burst_cnt)+'\n')
	for idx in range(len(communities)):
		info=idx_info[idx]
		flog.write(str(idx)+'\t'+str(info))
		flog.write('\n')

	'''
	for idx in range(len(communities)):
		nodes=communities[idx]
		subG=nx.Graph()
		for e in G.edges():
			if e[0] in nodes and e[1] in nodes:
				subG.add_edge(e[0],e[1])
		cliques=list(nx.find_cliques(subG))
		#print cliques
		max_size=max([len(clique) for clique in cliques])
		print max_size
		for clique in cliques:
			if len(clique)==max_size:
				print clique
		cliques=set(nx.k_clique_communities(subG,max(2,max_size)))
		for clique in cliques:
			print clique
	'''
	flog.close()



if __name__ == '__main__':
	main()