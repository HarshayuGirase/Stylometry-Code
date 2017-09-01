import sys,os
import string
#from bs4 import BeautifulSoup
#import nltk
import subprocess

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

def get_syntactic_from_trees(lines):
	#lines=['(ROOT (SBARQ (WHNP (WHNP (WDT Which))(PP (IN of) (NP (DT these) (NNS people))))(SQ (VP (VBD wrote)(NP (DT this) (VBG blog) (NN post))))(. ?)))']
	syntactic_pair_count={}
	for l in lines:
		l=l.replace(' (','(')
		path_list=[]
		curr_depth=0
		tmp_str=''
		for t in l:
			if t=='(':
				if tmp_str!='': path_list.append(tmp_str)
				#print path_list
				tmp_str=''
			elif t==')':
				if tmp_str!='': path_list.append(tmp_str)
				tmp_str=''
				if len(path_list)<2: break
				parent=path_list[-2].split()[0]
				child=path_list[-1].split()[0]
				try:
					syntactic_pair_count[parent+'-'+child]+=1
				except KeyError:
					syntactic_pair_count[parent+'-'+child]=1
				#print path_list[-2].split()[0],path_list[-1].split()[0]
				path_list.pop()
			#elif t==' ': continue
			else:
				tmp_str+=t
	print syntactic_pair_count
	return syntactic_pair_count

def get_feature(text,server):
	tmp_write=open(path+server+'_tmp.txt','w')
	tmp_write.write(text)
	tmp_write.close()
	command='java -mx500m -cp "../stanford_parser/stanford-parser-full-2014-08-27/*" edu.stanford.nlp.parser.lexparser.LexicalizedParser -outputFormat "oneline" edu/stanford/nlp/models/lexparser/englishPCFG.ser.gz'
	command+= ' '+path+server+'_tmp.txt'
	print command
	try:
		p=subprocess.Popen(command, shell=True,stdout=subprocess.PIPE)
		(output,err)=p.communicate()
		lines=output.split('\n')
		feature=get_syntactic_from_trees(lines)

	except:
		print 'failed to parse'
		sys.exit(1)

	return str(feature)

def get_id(server,idx):
	server_id={}
	server_id['antman']=0
	server_id['blackwidow']=1
	server_id['captainamerica']=2
	server_id['drstrange']=3
	server_id['hawkeye']=4
	server_id['namor']=5
	server_id['quicksilver']=6
	server_id['ultron']=7
	server_id['colossus']=8
	server_id['jeanerey']=9
	server_id['beast']=10
	server_id['gambit']=11
	server_id['nightcrawler']=12
	server_id['bishop']=13
	server_id['havok']=14
	server_id['marrow']=15
	#return server_id[server]*6+int(idx)
	
	if server_id[server]<=7:
		tmp=(server_id[server]*8+int(idx))*2
		return [tmp,tmp+1]
	else:
		tmp=128+(server_id[server]-8)*4+int(idx)
		return [tmp]
	

def main():
	fin=open(path+'slice_aid_text_sample.txt','r')
	fout=open(path+'syntactic_features/syntactic_feature_sample_'+sys.argv[1]+sys.argv[2]+'.csv','w')
	flog=open(path+'syntactic_features/syntactic_feature_sample_'+sys.argv[1]+sys.argv[2]+'.log','w')
	server=sys.argv[1]
	idx=sys.argv[2]
	ID=get_id(server,idx)
	count=1
	for l in fin:
		count+=1
		tmp=count%160
		if tmp not in ID: continue
		#if not count%96==ID: continue
		split_str=l.rstrip('\n').split('\t')
		key=split_str[0]+'_p'+split_str[1]
		text=split_str[2]
		#feature=get_feature(text)
		try:
			feature=get_feature(text,server+idx)
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