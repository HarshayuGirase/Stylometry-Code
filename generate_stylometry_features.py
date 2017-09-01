import sys,os
import string
from bs4 import BeautifulSoup
import nltk

path='all/'

def Clean(text):
    format='ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz '
    for t in text:
        if not t in format:
			if t=='-':
				text=text.replace(t,' ')
			else:
				text=text.replace(t,'')
    return text

def get_text(html):
	soup=BeautifulSoup(html)
	text=soup.find('div',id='article_body')
	#print text
	text=nltk.clean_html(str(text))
	return text


def get_length(text):
	word_length=len(text.split())
	character_length=len(text)
	return str(word_length)+','+str(character_length)

def get_vocabulary_richness(text):
	text=Clean(text)
	text=text.lower()
	words=text.split()
	word_count={}
	for word in words:
		try:
			word_count[word]+=1
		except KeyError:
			word_count[word]=1
	max_v=max(word_count.values())
	#print max_v
	V=[0 for i in range(1,max(max_v+1,11))]
	for v in word_count.values():
		V[v-1]+=1
	N=len(word_count)*1.0
	sum_v=0.0
	for i in range(1,max_v+1):
		sum_v+=i*i*V[i-1]
	K=10000.0*(sum_v-N)
	K=K/(N*N)
	richness=str(K)
	for i in range(1,11):
		richness=richness+','+str(V[i-1])
	return richness

def get_word_shape(text):
	text=Clean(text)
	words=text.split()
	shape=[0,0,0,0,0]
	for word in words:
		if word.islower():
			shape[0]+=1
		elif word.isupper():
			shape[1]+=1
		elif word[0].isupper() and word[1:-1].islower(): 
			shape[2]+=1
		elif word[0].isupper() and word[1:-1].lower()!=word[1:-1]:
			shape[3]+=1
		else:
			shape[4]+=1
	return str(shape[0])+','+str(shape[1])+','+str(shape[2])+','+str(shape[3])+','+str(shape[4])

def get_word_length(text):
	text=Clean(text)
	words=text.split()
	length=[0 for i in range(1,21)]
	for word in words:
		tmp_length=len(word)
		if tmp_length<21:length[tmp_length-1]+=1
	word_length=''
	for l in length:
		word_length=word_length+','+str(l)
	return word_length

def get_letters(text):
	text=Clean(text)
	text=text.lower()
	letter_count={}
	for tmp in 'abcdefghijklmnopqrstuvwxyz':
		letter_count[tmp]=0
	for t in text:
		if t in 'abcdefghijklmnopqrstuvwxyz':
			try:
				letter_count[t]+=1
			except KeyError:
				letter_count[t]=1
	letter=''
	for l in letter_count:
		letter+=','+str(letter_count[l])
	return letter

def get_digits(text):
	text=Clean(text)
	text=text.lower()
	digit_count={}
	for tmp in '0123456789':
		digit_count[tmp]=0
	for t in text:
		if t in '0123456789':
			try:
				digit_count[t]+=1
			except KeyError:
				digit_count[t]=1
	digit=''
	for d in digit_count:
		digit+=','+str(digit_count[d])
	return digit

def get_punctuation(text):
	punctuation_set='.?!,;:()"-\''
	punc_count={}
	for tmp in punctuation_set:
		punc_count[tmp]=0
	for t in text:
		if t in punctuation_set:
			try:
				punc_count[t]+=1
			except KeyError:
				punc_count[t]=1
	punc=''
	for p in punc_count:
		punc+=','+str(punc_count[p])
	return punc

def get_special(text):
	special_character='`~@#$%^&*_+=[]{}\|/<>'
	spec_count={}
	for tmp in special_character:
		spec_count[tmp]=0
	for t in text:
		if t in special_character:
			try:
				spec_count[t]+=1
			except KeyError:
				spec_count[t]=1
	special=''
	for s in spec_count:
		special+=','+str(spec_count[s])
	return special

def get_function_words(text):
	fin=open('function_words.txt','r')
	l=fin.readline()
	fin.close()
	function_words=l.rstrip('\n').split(', ')
	func_word_count={}
	for word in function_words:
		func_word_count[word]=0
	text=Clean(text)
	text=text.lower()
	words=text.split()
	for word in words:
		if word in function_words:
			try:
				func_word_count[word]+=1
			except:
				func_word_count[word]=1
	func=''
	for word in function_words:
		func+=','+str(func_word_count[word])
	return func

def get_feature(text):
	length_info=get_length(text)
	richness=get_vocabulary_richness(text)
	word_shape=get_word_shape(text)
	word_length=get_word_length(text)
	letter=get_letters(text)
	digit=get_digits(text)
	punc=get_punctuation(text)
	special=get_special(text)
	func=get_function_words(text)
	feature=length_info+','+richness
	feature+=','+word_shape
	feature+=word_length
	feature+=letter
	feature+=digit
	feature+=punc
	feature+=special
	feature+=func
	return feature

def main():
	fin=open(path+'slice_aid_text_sample.txt','r')
	fout=open(path+'stylometry_feature_sample.csv','w')
	flog=open(path+'stylometry_feature_sample.log','w')
	for l in fin:
		split_str=l.rstrip('\n').split('\t')
		key=split_str[0]+'_p'+split_str[1]
		text=split_str[2]
		#feature=get_feature(text)
		try:
			feature=get_feature(text)
			fout.write(key+','+feature+'\n')
			fout.flush()
		except:
			flog.write(key+'\n')
			flog.flush()
			continue
	fin.close()
	fout.close()
	flog.close()
if __name__ == '__main__':
	main()