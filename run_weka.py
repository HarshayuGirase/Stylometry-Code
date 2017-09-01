import string
import sys,os
import subprocess
import random
import datetime

path='slice500/'

def run(author):
	train_dir=path+'training_testing/'+author+'_training.csv'
	test_dir=path+'training_testing/'+'all_testing.arff'
	output_dir=path+'training_testing2/'+author+'_training.arff'
	result_dir=path+'training_testing2/'+author+'_SVM.txt'

	Filter='weka.filters.unsupervised.attribute.Remove -R 1'
	classifier='weka.classifiers.functions.LibSVM -S 0 -K 0 -D 3 -G 1.0 -R 0.0 -N 0.5 -M 40.0 -C 1.0 -E 0.0010 -P 0.1 -Z -seed 1'
	#classifier='weka.classifiers.meta.AttributeSelectedClassifier'+' -t '+output_dir+' -i '+' -E "weka.attributeSelection.CfsSubsetEval" -S "weka.attributeSelection.BestFirst -D 1 -N 5" -W weka.classifiers.trees.RandomForest -- -I 10 -K 0 -S 1'
	command_line = 'java -XX:-UseGCOverheadLimit -Xmx64g -cp /cs/avenger/gangw/lib/weka-3-6-10/weka.jar:/cs/avenger/gangw/lib/weka-3-6-10/libsvm.jar '+Filter+' -i '+train_dir+' -o ' +output_dir
	print command_line
	try:
		p = subprocess.Popen(command_line, stdout=subprocess.PIPE, shell=True)
		(output, err) = p.communicate()
	except:
		print 'failed run the weka filter...'
		exit(1)
	command_line = 'java -XX:-UseGCOverheadLimit -Xmx64g -cp /cs/avenger/gangw/lib/weka-3-6-10/weka.jar:/cs/avenger/gangw/lib/weka-3-6-10/libsvm.jar '+classifier +' -t '+output_dir+' -T '+test_dir+' -p 0 ' +' > '+result_dir
	print command_line
	try:
		p = subprocess.Popen(command_line, stdout=subprocess.PIPE, shell=True)
		(output, err) = p.communicate()
	except:
		print 'failed run the weka classification...'
		exit(1)

def run2(author):
	train_dir=path+'training_testing2/'+author+'_training.csv'
	test_dir=path+'training_testing2/'+'all_testing.arff'
	output_dir=path+'training_testing2/'+author+'_training.arff'
	result_dir=path+'training_testing2/'+author+'_BN.txt'

	Filter='weka.filters.unsupervised.attribute.Remove -R 1'
	classifier='weka.classifiers.bayes.BayesNet'
	classifier_option='-D -Q "weka.classifiers.bayes.net.search.local.K2" -- -P 1 -S BAYES -E "weka.classifiers.bayes.net.estimate.SimpleEstimator" -- -A 0.5'
	#classifier='weka.classifiers.meta.AttributeSelectedClassifier'+' -t '+output_dir+' -i '+' -E "weka.attributeSelection.CfsSubsetEval" -S "weka.attributeSelection.BestFirst -D 1 -N 5" -W weka.classifiers.trees.RandomForest -- -I 10 -K 0 -S 1'
	command_line = 'java -XX:-UseGCOverheadLimit -Xmx64g -cp /cs/avenger/gangw/lib/weka-3-6-10/weka.jar:/cs/avenger/gangw/lib/weka-3-6-10/libsvm.jar '+Filter+' -i '+train_dir+' -o ' +output_dir
	print command_line
	'''
	try:
		p = subprocess.Popen(command_line, stdout=subprocess.PIPE, shell=True)
		(output, err) = p.communicate()
	except:
		print 'failed run the weka filter...'
		exit(1)
	'''
	command_line = 'java -XX:-UseGCOverheadLimit -Xmx64g -cp /cs/avenger/gangw/lib/weka-3-6-10/weka.jar:/cs/avenger/gangw/lib/weka-3-6-10/libsvm.jar '+classifier +' -t '+output_dir+' -T '+test_dir+' -p 0 ' +classifier_option +' > '+result_dir
	print command_line
	try:
		p = subprocess.Popen(command_line, stdout=subprocess.PIPE, shell=True)
		(output, err) = p.communicate()
	except:
		print 'failed run the weka classification...'
		exit(1)


def main():
	authors=[]
	'''
	fin=open(path+'unfinished_authors.txt','r')
	for l in fin:
		authors.append(l.rstrip('\n'))
	fin.close()
	
	author_all_count={}
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
	#print author_all_count['dan-ahrens']>10
	for author in author_all_count:
		if author=='': continue
		if author_all_count[author]>10.0:
			authors.append(author)
			#if author=='dan-ahrens':
			#	print author_all_count['dan-ahrens']
	#print len(author_all_count)
	'''
	fin=open('author_aid_map.txt','r')
	for l in fin:
		author=l.rstrip('\n').split('\t')[0]
		#if author_all_count[author]<10: continue
		authors.append(author)
	fin.close()
	'''
	if sys.argv[1]=='0':
		Filter='weka.filters.unsupervised.attribute.Remove -R 1'
		train_dir=path+'training_testing/'+'all_testing.csv'
		output_dir=path+'training_testing/'+'all_testing.arff'
		command_line = 'java -XX:-UseGCOverheadLimit -Xmx64g -cp /cs/avenger/gangw/lib/weka-3-6-10/weka.jar:/cs/avenger/gangw/lib/weka-3-6-10/libsvm.jar '+Filter+' -i '+train_dir+' -o ' +output_dir
		print command_line
		try:
			p = subprocess.Popen(command_line, stdout=subprocess.PIPE, shell=True)
			(output, err) = p.communicate()
		except:
			print 'failed run the weka filter...'
			exit(1)
	'''
	#authors=['ted-kavadas']
	#print datetime.datetime.now()
	authors=list(set(authors))
	#print len(authors)
	#sys.exit(0)
	start=int(sys.argv[1])
	for author in authors[start::5]:
		if author=='http://seekingalpha.com/srch': continue
		run2(author)
	print datetime.datetime.now()
if __name__ == '__main__':
	main()