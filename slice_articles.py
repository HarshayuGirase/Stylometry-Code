import sys,os
import string
from bs4 import BeautifulSoup
import nltk

path='all/'
slice_size=500
def get_text(html):
	soup=BeautifulSoup(html)
	text=soup.find('div',id='article_body')
	#print text
	text=nltk.clean_html(str(text))
	return text

def main():
	fin=open('author_aid_map.txt','r')
	valid_aids=[]
	for l in fin:
		aid=l.rstrip('\n').split('\t')[1]
		valid_aids.append(aid)
	fin.close()
	valid_aids=set(valid_aids)
	fin=open('../supervised_ML/deleted_article_text.txt','r')
	deleted_aids=[]
	fout=open(path+'slice_aid_text_sample.txt','w')
	#flog=open('slice_aid_text.log','w')
	for l in fin:
		split_str=l.rstrip('\n').split('||||',1)
		aid=split_str[0]
		#if aid not in valid_aids: continue
		#html=split_str[1]
		text=split_str[1]
		text=text.replace('@@@@','')
		split_text=text.split()
		length=len(split_text)
		if length<50: continue
		cnt=length/slice_size
		deleted_aids.append(aid)
		#slice_length=length/cnt
		idx=[]
		idx.append(0)
		for i in range(cnt-1):
			#if start>=length: break
			start=idx[i]+slice_size
			if start>=length:
				break
			while True:
				start+=1
				if start>=length:
					idx.append(length)
					break
				if '.' in split_text[start] or '!' in split_text[start] or '?' in split_text[start]:
					idx.append(start+1)
					break
		if len(idx)==1:
			idx.append(length)
		elif length-idx[-1]>slice_size:
			idx.append(length)
		else:
			idx[-1]=length
		for i in range(len(idx)-1):
			fout.write(aid+'\t'+str(i)+'\t'+' '.join(split_text[idx[i]: idx[i+1]])+'\n')
	fin.close()
	#sys.exit(0)
	deleted_aids=set(deleted_aids)
	fin=open('../recrawl_SA/article_pages.txt','r')
	for l in fin:
		split_str=l.rstrip('\n').split('\t',1)
		aid=split_str[0]
		#if aid not in valid_aids: continue
		html=split_str[1]
		text=get_text(split_str[1])
		if aid in deleted_aids:
			continue
		split_text=text.split()
		length=len(split_text)
		if length<50: continue
		cnt=length/slice_size
		#slice_length=length/cnt
		idx=[]
		idx.append(0)
		for i in range(cnt-1):
			#if start>=length: break
			start=idx[i]+slice_size
			if start>=length:
				break
			while True:
				start+=1
				if start>=length:
					idx.append(length)
					break
				if '.' in split_text[start] or '!' in split_text[start] or '?' in split_text[start]:
					idx.append(start+1)
					break
		if len(idx)==1:
			idx.append(length)
		elif length-idx[-1]>slice_size:
			idx.append(length)
		else:
			idx[-1]=length
		for i in range(len(idx)-1):
			fout.write(aid+'\t'+str(i)+'\t'+' '.join(split_text[idx[i]: idx[i+1]])+'\n')
	fout.close()

if __name__ == '__main__':
	main()