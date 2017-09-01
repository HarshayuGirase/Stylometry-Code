import sys,os
import string

path='all/'

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
	filenames=os.listdir(path+'training_testing/')
	for author in set(authors):
		if author_all_count[author]<=10: continue
		if author=='http://seekingalpha.com/srch': continue
		if author+'_SVM.txt' not in filenames: 
			print author

'''
def main():
	#count=0
	unfinished_authors=[]
	finished=[]
	fout=open(path+'unfinished_authors.txt','w')
	for k in range(160):
		fin=open(path+'torun_'+str(k)+'.txt','r')
		authors=[]
		for l in fin:
			authors.append(l.rstrip('\n'))
		fin.close()
		fin=open(path+'run_weka_'+str(k)+'.log','r')
		for l in fin:
			finished.append(l.rstrip('\n'))
		fin.close()
		#if len(authors)==len(finished):
		#	count+=1
		#if len(authors)-len(finished)>=7:
		#	unfinished_authors+=authors[-8:-1]
		unfinished_authors+=list(set(authors))
	#print len(unfinished_authors)
	#print count
	#for author in unfinished_authors:
	#	fout.write(author+'\n')
	#fout.close()
	for k in range(88):
		fin=open(path+'2torun_'+str(k)+'.txt','r')
		authors=[]
		for l in fin:
			authors.append(l.rstrip('\n'))
		fin.close()
		fin=open(path+'2run_weka_'+str(k)+'.log','r')
		for l in fin:
			finished.append(l.rstrip('\n'))
		fin.close()
		unfinished_authors+=list(set(authors))
	print len(set(finished))
	print len(set(unfinished_authors)-set(finished))
	for author in set(unfinished_authors)-set(finished):
		fout.write(author+'\n')
	fout.close()
'''
if __name__ == '__main__':
	main()