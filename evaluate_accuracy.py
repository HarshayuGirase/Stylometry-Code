import sys,os
import string

path='slice500/'
def check_accuracy(author,test_aids,aid_author,author_all_count,fout):
	fin=open(path+'training_testing2/'+author+'_BN.txt')
	flag=1
	idx_pre={}
	for l in fin.readlines():
		l = l.strip()
		if '===' in l:
			flag=0
			continue
		if flag: continue
		if l =='':continue
		if 'inst#' in l: continue
		tos = l.rsplit()
		ID=int(tos[0])
		act=tos[1]
		pre=tos[2]
		idx_pre[ID]=pre
	fin.close()
	author_similarity={}
	#if len(idx_pre)==0: 
	#	return
	for idx in range(1,len(test_aids)-1):
		aid=test_aids[idx]
		tmp_author=aid_author[aid]
		pre=idx_pre[idx]
		act=False
		if tmp_author.split('_')[0]==author.split('_')[0]:
			act=True
		if 'True' in pre:
			try:
				author_similarity[tmp_author]+=1.0/author_all_count[tmp_author]
			except KeyError:
				author_similarity[tmp_author]=1.0/author_all_count[tmp_author]
	for tmp_author in author_similarity:
		fout.write(author+'\t'+tmp_author+'\t'+str(author_similarity[tmp_author])+'\n')

def evaluation(author_all_count):
	fin=open(path+'author_similarity_by_BN.txt','r')
	authors_prob={}
	for l in fin:
		split_str=l.rstrip('\n').split('\t')
		author1=split_str[0]
		author2=split_str[1]
		prob=float(split_str[2])
		authors_prob[author1+','+author2]=prob
	fin.close()
	sorted_final = [(k,v) for v,k in sorted([(v,k) for k,v in authors_prob.items()],reverse=True)]
	tp=0
	fp=0
	all_p=100.0
	reject_author=0.0
	fout=open(path+'author_count.txt','w')
	for author in author_all_count:
		fout.write(author+'\t'+str(author_all_count[author])+'\n')
		if author_all_count[author]<10:
			reject_author+=1
			if 's0' in author or 's1' in author:
				all_p=all_p-1
	print all_p
	print reject_author
	print len(author_all_count)
	fout.close()
	all_n=(200-reject_author)*199-all_p
	fout=open(path+'author_accuracy_by_BN.txt','w')
	#fout2=open(path+'similar_author_pairs2.txt','w')
	for it in sorted_final:
		author1=it[0].split(',')[0]
		if author_all_count[author1]<10: continue
		author2=it[0].split(',')[1]
		if author1==author2: continue
		aver=it[1]
		if author1.split('_')[0]==author2.split('_')[0]:
			tp+=1
			flag='tp'
		else:
			fp+=1
			flag='fp'
		fout.write(str(tp/all_p)+'\t'+str(fp/all_n)+'\t'+str(aver)+'\n')
		#if aver>=0.4:
		#	fout2.write(author1+'\t'+author2+'\t'+str(aver)+'\t'+flag+'\n')
	fout.close()
	#fout2.close()

def main():
	authors=[]
	aid_author={}
	author_all_count={}
	fin=open(path+'author_keys.txt','r')
	for l in fin:
		author=l.rstrip('\n').split('\t')[0]
		authors.append(author)
		aid=l.rstrip('\n').split('\t')[1]
		aid_author[aid]=author
		try:
			author_all_count[author]+=1.0
		except KeyError:
			author_all_count[author]=1.0
	fin.close()
	
	test_aids=[]
	fin=open(path+'training_testing2/'+'testing_keys.txt','r')
	for l in fin:
		aid=l.rstrip('\n')
		test_aids.append(aid)
	fin.close()
	#authors=['santosh-sankar','imfdirect_s1']
	#idx=int(sys.argv[1])
	#count=0
	fout=open(path+'author_similarity_by_BN.txt','w')
	#filenames=os.listdir(path+'training_testing/')
	for author in set(authors):
		#count+=1
		#if author=='': continue
		#if author=='***': continue
		#if author_all_count[author]<=10: continue
		#if author=='http://seekingalpha.com/srch': continue
		#if author+'_SVM.txt' not in filenames: continue
		#if not count%8==idx: continue
		check_accuracy(author,test_aids,aid_author,author_all_count,fout)
	fout.close()
	evaluation(author_all_count)

if __name__ == '__main__':
	main()